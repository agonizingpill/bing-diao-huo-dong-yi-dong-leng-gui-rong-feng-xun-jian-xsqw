import json
from pathlib import Path
from traceback import print_exc

from core import jobs
from core.db import engine, metadata
from core.queueing import PROCESSING, QUEUE, broker, requeue
from domain.learning import calculate

pulse = Path('/tmp/compute-heartbeat')
STALE_SECONDS = 300

def recover():
    """worker 重启：上次中断在 running 的任务按原样本放回队列。"""
    metadata.create_all(engine)
    jobs.reset_running()
    broker.delete(PROCESSING)
    requeue()

def run(item):
    try:
        token = json.loads(item)['token']
    except (ValueError, KeyError, TypeError):
        broker.lrem(PROCESSING, 1, item)
        return
    try:
        job = jobs.claim(token)
        if job is None:
            return
        try:
            jobs.complete(token, 'ready', result=calculate(job['payload']))
        except ValueError as exc:
            jobs.complete(token, 'rejected', detail=str(exc)[:255])
        except Exception:
            print_exc()
            jobs.complete(token, 'rejected', detail='计算失败，请检查输入和 worker 日志')
    finally:
        broker.lrem(PROCESSING, 1, item)

def serve():
    recover()
    while True:
        broker.ping()
        pulse.touch()
        jobs.reset_running(STALE_SECONDS)
        requeue()
        item = broker.blmove(QUEUE, PROCESSING, timeout=2, src='LEFT', dest='RIGHT')
        if item is None:
            continue
        run(item)
        pulse.touch()

if __name__ == '__main__':
    serve()

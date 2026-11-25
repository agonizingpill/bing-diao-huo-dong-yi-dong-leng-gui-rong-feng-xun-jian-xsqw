import json
from uuid import uuid4

from fastapi import HTTPException
from redis import Redis
from sqlalchemy import select

from core import jobs
from core.config import REDIS_URL
from core.db import transaction
from domain.seam_maps_model import seam_maps

broker = Redis.from_url(REDIS_URL, decode_responses=True)
QUEUE = 'compute_requests'
PROCESSING = f'{QUEUE}:processing'

def submit(user, payload, sample):
    """受理即把冰雕实测和当时的带载参照写入 SQL；Redis 只投递任务号。"""
    token = uuid4().hex
    with transaction() as conn:
        jobs.create(conn, token, user['sub'], sample, payload)
    broker.rpush(QUEUE, json.dumps({'token': token}))
    return {'token': token, 'status': 'queued'}

def _queued():
    tokens = set()
    for raw in broker.lrange(QUEUE, 0, -1):
        try:
            tokens.add(json.loads(raw)['token'])
        except (ValueError, KeyError, TypeError):
            continue
    return tokens

def requeue():
    """补投已落库却不在队列中的任务；投递失败或 Redis 重启后自愈。"""
    waiting = jobs.queued_tokens()
    if not waiting:
        return 0
    present = _queued()
    missing = [token for token in waiting if token not in present]
    if missing:
        broker.rpush(QUEUE, *[json.dumps({'token': token}) for token in missing])
    return len(missing)

def _visible(user, record):
    if record is None:
        raise HTTPException(404, detail='计算任务不存在或已过期')
    if record['owner'] != user['sub'] and user['role'] != 'reviewer':
        raise HTTPException(403, detail='仅提交人和复核员可查看计算')
    return record

def _ready(record):
    if record['status'] == 'rejected':
        raise HTTPException(409, detail=record['detail'] or '计算被拒绝')
    if record['status'] != 'ready':
        raise HTTPException(409, detail='等待计算完成后再提交')
    return record

def _public(record):
    return {'token': record['token'], 'sample': record['sample'], 'status': record['status'],
            'result': record['result'], 'detail': record['detail'], 'created_at': record['created_at']}

def view(user, token):
    with transaction() as conn:
        record = jobs.fetch(conn, token)
    record = _visible(user, record)
    return {'status': record['status'], 'result': record['result'], 'detail': record['detail'],
            'sample': record['sample'], 'input': record['payload']}

def result(user, token):
    data = view(user, token)
    _ready(data)
    return data

def locked(user, token, conn):
    """签认时锁住凭据行：同一计算的两路重试只能有一路落库。"""
    record = jobs.lock(conn, token)
    return _ready(_visible(user, record))

def open_for(user):
    """复核员在融缝页找回未办完的单；非复核员只看自己的。"""
    with transaction() as conn:
        settled_tokens = {row[0] for row in conn.execute(select(seam_maps.c.token))}
        settled_samples = {row[0] for row in conn.execute(select(seam_maps.c.sample))}
        rows = jobs.open_jobs(conn, settled_tokens, settled_samples)
    if user['role'] != 'reviewer':
        rows = [row for row in rows if row['owner'] == user['sub']]
    return [_public(row) for row in rows]

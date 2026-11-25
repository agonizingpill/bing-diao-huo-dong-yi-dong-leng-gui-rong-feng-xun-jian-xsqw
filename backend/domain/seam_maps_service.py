from sqlalchemy import select

from core.queueing import locked, submit
from core.records import find, get, insert, need, scan
from domain.thaw_samples_model import thaw_samples
from domain.seam_maps_model import seam_maps


def score_seam(conn, user, data):
    source=get(conn,thaw_samples,data.sample)
    need(not source['empty_test'],'空载测试不评估冰雕融缝')
    pool=[r for r in scan(conn,thaw_samples) if r['cell']==source['cell'] and
        not r['empty_test'] and r['code']!=data.sample]
    need(len(pool)>=20,'此柜格带载基线不足二十条')
    return submit(user,{'source':source,'pool':pool},source['code'])


def record_seam(conn, user, data):
    run=locked(user,data.token,conn)
    metrics=run['result']
    # 同一冰雕样只在样例行锁上并发签认一次：换凭据重算也不得重复登记。
    get(conn,thaw_samples,run['sample'],lock=True)
    existing=find(conn,seam_maps,data.code)
    if existing is not None:
        # 同一凭据的重试取回原签认，不同凭据占用同一单号则拒绝。
        need(existing['token']==data.token,'融缝单号已被另一份计算占用')
        return existing
    settled=conn.execute(select(seam_maps.c.token).where(seam_maps.c.token==data.token)).scalar()
    need(settled is None,f'该计算已登记为 {settled}，请勿重复签认')
    signed=conn.execute(select(seam_maps.c.code).where(seam_maps.c.sample==run['sample'])).scalar()
    need(signed is None,f'该冰雕实测已签认为 {signed}，请勿重复评分')
    return insert(conn,seam_maps,code=data.code,sample=run['sample'],
       density=metrics['density'],threshold=metrics['threshold'],token=data.token,
       decision='建议换格' if metrics['density']<metrics['threshold'] else '同档可留')

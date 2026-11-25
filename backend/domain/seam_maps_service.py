from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.cold_cells_model import cold_cells
from domain.thaw_samples_model import thaw_samples
from domain.seam_maps_model import seam_maps
from domain.cell_swaps_model import cell_swaps


def score_seam(conn, user, data):
    source=get(conn,thaw_samples,data.sample)
    need(not source['empty_test'],'空载测试不评估冰雕融缝')
    pool=[r for r in scan(conn,thaw_samples) if r['cell']==source['cell'] and
        not r['empty_test'] and r['code']!=data.sample]
    need(len(pool)>=20,'此柜格带载基线不足二十条')
    return submit(user,{'source':source,'pool':pool})


def record_seam(conn, user, data):
    run=result(user,data.token); metrics=run['result']
    return insert(conn,seam_maps,code=data.code,sample=run['input']['source']['code'],
       density=metrics['density'],threshold=metrics['threshold'],token=data.token,
       decision='建议换格' if metrics['density']<metrics['threshold'] else '同档可留')

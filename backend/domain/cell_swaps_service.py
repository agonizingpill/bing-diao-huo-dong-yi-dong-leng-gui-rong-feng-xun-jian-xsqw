from sqlalchemy import select

from core.records import find, get, insert, need, update
from domain.cold_cells_model import cold_cells
from domain.thaw_samples_model import thaw_samples
from domain.seam_maps_model import seam_maps
from domain.cell_swaps_model import cell_swaps


def settle(conn, table, key, requested):
    """同号重试取回原单；若原单内容不同则拒绝。"""
    existing=find(conn,table,key,lock=True)
    if existing is None:
        return None
    need(all(existing[field]==value for field,value in requested.items()),'单号已被另一份内容占用')
    return existing


def reserve_swap(conn, user, data):
    # 先在融缝单行上排队，同号/同凭据的并发重试不会各自落一张新单。
    assessment=get(conn,seam_maps,data.seam,lock=True)
    existing=settle(conn,cell_swaps,data.code,data.model_dump())
    if existing is not None:
        return existing
    prior=conn.execute(select(cell_swaps).where(cell_swaps.c.seam==data.seam)).mappings().first()
    need(prior is None,f'该融缝单已有互换单 {prior["code"] if prior else ""}，请取回原单')
    row=get(conn,thaw_samples,assessment['sample'])
    need(assessment['decision']=='建议换格' and row['cell']!=data.target,'没有异格换位依据')
    ids=sorted({row['cell'],data.target})
    cells={id_:get(conn,cold_cells,id_,lock=True) for id_ in ids}
    original,destination=cells[row['cell']],cells[data.target]
    need(original['duty']==destination['duty'],'旧模脱模区不得占用成品转运格')
    agents=[p.strip() for p in data.handover.split('/')]
    need(len(agents)==2 and all(agents) and len(set(agents))==2,'需要两名不同搬移人签认')
    need(destination['authorized'] and not destination['closed'] and destination['free_slots']>0,'目标柜格不可用')
    output=insert(conn,cell_swaps,**data.model_dump(),state='已预留')
    update(conn,cold_cells,data.target,free_slots=destination['free_slots']-1)
    return output


def confirm_swap(conn, user, data):
    order=get(conn,cell_swaps,data.swap,lock=True)
    if order['state']==f'已交换 {data.stamp}':
        # 回执重试：原签认已入账，直接取回，不再返还余位。
        return order
    need(order['state']=='已预留','互换单已按其他格签入账，请核对回执')
    need(data.stamp.startswith(order['target']+'/'),'格签与目标柜格不匹配')
    assessment=get(conn,seam_maps,order['seam'])
    origin=get(conn,thaw_samples,assessment['sample'])['cell']
    lock={key:get(conn,cold_cells,key,lock=True) for key in sorted({origin,order['target']})}
    need(not lock[order['target']]['closed'],'目标柜格已经暂停，须复核')
    update(conn,cold_cells,origin,free_slots=lock[origin]['free_slots']+1)
    return update(conn,cell_swaps,data.swap,state='已交换 '+data.stamp)

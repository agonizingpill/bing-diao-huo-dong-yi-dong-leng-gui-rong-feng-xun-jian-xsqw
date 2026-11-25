from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.cold_cells_model import cold_cells
from domain.thaw_samples_model import thaw_samples
from domain.seam_maps_model import seam_maps
from domain.cell_swaps_model import cell_swaps


def reserve_swap(conn, user, data):
    assessment=get(conn,seam_maps,data.seam,lock=True)
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
    assessment=get(conn,seam_maps,order['seam'])
    origin=get(conn,thaw_samples,assessment['sample'])['cell']
    lock={key:get(conn,cold_cells,key,lock=True) for key in sorted({origin,order['target']})}
    need(order['state']=='已预留' and data.stamp.startswith(order['target']+'/'),'状态或格签不匹配')
    need(not lock[order['target']]['closed'],'目标柜格已经暂停，须复核')
    update(conn,cold_cells,origin,free_slots=lock[origin]['free_slots']+1)
    return update(conn,cell_swaps,data.swap,state='已交换 '+data.stamp)

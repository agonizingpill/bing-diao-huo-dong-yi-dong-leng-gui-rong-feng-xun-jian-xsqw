from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.cold_cells_model import cold_cells
from domain.thaw_samples_model import thaw_samples
from domain.seam_maps_model import seam_maps
from domain.cell_swaps_model import cell_swaps


def observe_seam(conn, user, data):
    cell=get(conn,cold_cells,data.cell,lock=True)
    need(cell['authorized'] and not cell['closed'],'柜格当前不开放测量')
    need(0<=data.mass_kg<=350 and 0<=data.melt<=30 and -30<=data.drift<=30,'柜格观测值越界')
    need((data.mass_kg==0)==data.empty_test,'空载凭单要求零质量')
    return insert(conn,thaw_samples,**data.model_dump())

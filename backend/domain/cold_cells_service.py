from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.cold_cells_model import cold_cells
from domain.thaw_samples_model import thaw_samples
from domain.seam_maps_model import seam_maps
from domain.cell_swaps_model import cell_swaps


def set_cell_state(conn, user, data):
    get(conn,cold_cells,data.cell,lock=True)
    return update(conn,cold_cells,data.cell,closed=data.closed)

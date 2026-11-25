from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import cold_cells_service as service
from domain.cold_cells_model import cold_cells
from domain.cold_cells_schemas import SetCellState

router = APIRouter()

@router.get('/cold_cells')
def list_cold_cells(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, cold_cells)


@router.post('/cold_cells/set-cell-state')
def set_cell_state(data: SetCellState, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.set_cell_state(conn, user, data)
        record(conn, user, 'cold_cells.set_cell_state')
        return output

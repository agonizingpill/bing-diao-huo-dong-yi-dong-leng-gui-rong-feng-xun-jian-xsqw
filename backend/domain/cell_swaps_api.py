from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import cell_swaps_service as service
from domain.cell_swaps_model import cell_swaps
from domain.cell_swaps_schemas import ReserveSwap, ConfirmSwap

router = APIRouter()

@router.get('/cell_swaps')
def list_cell_swaps(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, cell_swaps)


@router.post('/cell_swaps/reserve-swap')
def reserve_swap(data: ReserveSwap, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.reserve_swap(conn, user, data)
        record(conn, user, 'cell_swaps.reserve_swap')
        return output


@router.post('/cell_swaps/confirm-swap')
def confirm_swap(data: ConfirmSwap, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.confirm_swap(conn, user, data)
        record(conn, user, 'cell_swaps.confirm_swap')
        return output

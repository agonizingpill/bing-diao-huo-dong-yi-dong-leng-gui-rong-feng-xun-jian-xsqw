from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import thaw_samples_service as service
from domain.thaw_samples_model import thaw_samples
from domain.thaw_samples_schemas import ObserveSeam

router = APIRouter()

@router.get('/thaw_samples')
def list_thaw_samples(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, thaw_samples)


@router.post('/thaw_samples/observe-seam')
def observe_seam(data: ObserveSeam, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.observe_seam(conn, user, data)
        record(conn, user, 'thaw_samples.observe_seam')
        return output

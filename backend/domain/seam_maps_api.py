from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import seam_maps_service as service
from domain.seam_maps_model import seam_maps
from domain.seam_maps_schemas import ScoreSeam, RecordSeam

router = APIRouter()

@router.get('/seam_maps')
def list_seam_maps(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, seam_maps)


@router.post('/seam_maps/score-seam')
def score_seam(data: ScoreSeam, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.score_seam(conn, user, data)
        record(conn, user, 'seam_maps.score_seam')
        return output


@router.post('/seam_maps/record-seam')
def record_seam(data: RecordSeam, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.record_seam(conn, user, data)
        record(conn, user, 'seam_maps.record_seam')
        return output

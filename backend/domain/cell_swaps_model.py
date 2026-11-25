from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


cell_swaps = Table('cell_swaps', metadata,
    Column('code', String(64), primary_key=True),
    Column('seam', String(160), ForeignKey('seam_maps.code'), nullable=False, unique=True),
    Column('target', String(160), ForeignKey('cold_cells.code'), nullable=False),
    Column('handover', String(160), nullable=False),
    Column('state', String(160), nullable=False),
)

from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


seam_maps = Table('seam_maps', metadata,
    Column('code', String(64), primary_key=True),
    Column('sample', String(160), ForeignKey('thaw_samples.code'), nullable=False),
    Column('density', Float, nullable=False),
    Column('threshold', Float, nullable=False),
    Column('decision', String(160), nullable=False),
    Column('token', String(64), nullable=False, unique=True),
)

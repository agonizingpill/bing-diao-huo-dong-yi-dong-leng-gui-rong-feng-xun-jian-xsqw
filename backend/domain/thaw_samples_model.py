from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


thaw_samples = Table('thaw_samples', metadata,
    Column('code', String(64), primary_key=True),
    Column('cell', String(160), ForeignKey('cold_cells.code'), nullable=False),
    Column('mass_kg', Float, nullable=False),
    Column('melt', Float, nullable=False),
    Column('drift', Float, nullable=False),
    Column('empty_test', Boolean, nullable=False),
    Column('piece', String(160), nullable=False),
    CheckConstraint('mass_kg >= 0'),
    CheckConstraint('melt >= 0'),
)

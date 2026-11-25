from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


cold_cells = Table('cold_cells', metadata,
    Column('code', String(64), primary_key=True),
    Column('duty', String(160), nullable=False),
    Column('authorized', Boolean, nullable=False),
    Column('free_slots', Integer, nullable=False),
    Column('closed', Boolean, nullable=False),
    CheckConstraint('free_slots >= 0'),
)

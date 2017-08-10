from __future__ import absolute_import

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PrimaryKeyConstraint


# this is metrics definition class. For very table, both alembic
# and core app need to define its schema, one for migration, the
# other for ORM data operations, so copy and paste the same code
Base = declarative_base()

class DailyPrice(Base):
    __tablename__ = "daily_price"
    
    ind = sa.Column(sa.String(15), primary_key=True)
    symbol = sa.Column(sa.String(10), primary_key=True)
    date = sa.Column(sa.Date, primary_key=True)
    
    high = sa.Column(sa.Float)
    low = sa.Column(sa.Float)
    open = sa.Column(sa.Float)
    close = sa.Column(sa.Float)
    volume = sa.Column(sa.BigInteger)

class WeeklyPrice(Base):
    __tablename__ = "weekly_price"
    
    ind = sa.Column(sa.String(15), primary_key=True)
    symbol = sa.Column(sa.String(10), primary_key=True)
    date = sa.Column(sa.Date, primary_key=True)
    
    high = sa.Column(sa.Float)
    low = sa.Column(sa.Float)
    open = sa.Column(sa.Float)
    close = sa.Column(sa.Float)
    volume = sa.Column(sa.BigInteger)

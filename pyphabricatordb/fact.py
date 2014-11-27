# coding: utf-8
from sqlalchemy import BigInteger, Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class FactAggregate(Base):
    __tablename__ = 'fact_aggregate'
    __table_args__ = (
        Index('factType', 'factType', 'objectPHID', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    factType = Column(Unicode(32), nullable=False)
    objectPHID = Column(String, nullable=False)
    valueX = Column(BigInteger, nullable=False)


class FactCursor(Base):
    __tablename__ = 'fact_cursor'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(64), nullable=False, unique=True)
    position = Column(Unicode(64), nullable=False)


class FactRaw(Base):
    __tablename__ = 'fact_raw'
    __table_args__ = (
        Index('factType_2', 'factType', 'objectA'),
        Index('factType', 'factType', 'epoch')
    )

    id = Column(BigInteger, primary_key=True)
    factType = Column(Unicode(32), nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    objectA = Column(String, nullable=False)
    valueX = Column(BigInteger, nullable=False)
    valueY = Column(BigInteger, nullable=False)
    epoch = Column(Integer, nullable=False)
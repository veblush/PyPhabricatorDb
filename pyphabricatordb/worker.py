# coding: utf-8
from sqlalchemy import BigInteger, Column, Index, Integer, String
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class LiskCounter(Base):
    __tablename__ = 'lisk_counter'

    counterName = Column(Unicode(32), primary_key=True)
    counterValue = Column(BigInteger, nullable=False)


class WorkerActivetask(Base):
    __tablename__ = 'worker_activetask'
    __table_args__ = (
        Index('leaseOwner_2', 'leaseOwner', 'priority', 'id'),
    )

    id = Column(Integer, primary_key=True)
    taskClass = Column(Unicode(64), nullable=False, index=True)
    leaseOwner = Column(Unicode(64), index=True)
    leaseExpires = Column(Integer, index=True)
    failureCount = Column(Integer, nullable=False)
    dataID = Column(Integer, unique=True)
    failureTime = Column(Integer, index=True)
    priority = Column(Integer, nullable=False)


class WorkerArchivetask(Base):
    __tablename__ = 'worker_archivetask'
    __table_args__ = (
        Index('leaseOwner', 'leaseOwner', 'priority', 'id'),
    )

    id = Column(Integer, primary_key=True)
    taskClass = Column(Unicode(64), nullable=False)
    leaseOwner = Column(Unicode(64))
    leaseExpires = Column(Integer)
    failureCount = Column(Integer, nullable=False)
    dataID = Column(Integer, nullable=False)
    result = Column(Integer, nullable=False)
    duration = Column(BigInteger, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)
    priority = Column(Integer, nullable=False)


class WorkerTaskDatum(Base):
    __tablename__ = 'worker_taskdata'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode, nullable=False)
# coding: utf-8
from sqlalchemy import BigInteger, Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Edge(Base):
    __tablename__ = 'edge'
    __table_args__ = (
        Index('key_dst', 'dst', 'type', 'src', unique=True),
        Index('src', 'src', 'type', 'dateCreated', 'seq')
    )

    src = Column(String, primary_key=True, nullable=False)
    type = Column(Integer, primary_key=True, nullable=False)
    dst = Column(String, primary_key=True, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    seq = Column(Integer, nullable=False)
    dataID = Column(Integer)


class EdgeData(Base):
    __tablename__ = 'edgedata'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode, nullable=False)


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
    objectPHID = Column(String, index=True)


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
    objectPHID = Column(String, index=True)


class WorkerBulkJob(Base):
    __tablename__ = 'worker_bulkjob'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False, index=True)
    jobTypeKey = Column(Unicode(32), nullable=False, index=True)
    status = Column(Unicode(32), nullable=False, index=True)
    parameters = Column(Unicode, nullable=False)
    size = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class WorkerBulkJobTransaction(Base):
    __tablename__ = 'worker_bulkjobtransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class WorkerBulkTask(Base):
    __tablename__ = 'worker_bulktask'
    __table_args__ = (
        Index('key_job', 'bulkJobPHID', 'status'),
    )

    id = Column(Integer, primary_key=True)
    bulkJobPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    status = Column(Unicode(32), nullable=False)
    data = Column(Unicode, nullable=False)


class WorkerTaskData(Base):
    __tablename__ = 'worker_taskdata'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode, nullable=False)


class WorkerTrigger(Base):
    __tablename__ = 'worker_trigger'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    triggerVersion = Column(Integer, nullable=False, unique=True)
    clockClass = Column(Unicode(64), nullable=False)
    clockProperties = Column(Unicode, nullable=False)
    actionClass = Column(Unicode(64), nullable=False)
    actionProperties = Column(Unicode, nullable=False)


class WorkerTriggerevent(Base):
    __tablename__ = 'worker_triggerevent'

    id = Column(Integer, primary_key=True)
    triggerID = Column(Integer, nullable=False, unique=True)
    lastEventEpoch = Column(Integer)
    nextEventEpoch = Column(Integer, index=True)
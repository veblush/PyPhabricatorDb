# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class DrydockBlueprint(Base):
    __tablename__ = 'drydock_blueprint'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    className = Column(Unicode(255), nullable=False)
    blueprintName = Column(Unicode(255), nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    details = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class DrydockBlueprintTransaction(Base):
    __tablename__ = 'drydock_blueprinttransaction'

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


class DrydockLease(Base):
    __tablename__ = 'drydock_lease'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    resourceID = Column(Integer)
    status = Column(Integer, nullable=False)
    until = Column(Integer)
    ownerPHID = Column(String)
    attributes = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    taskID = Column(Integer)
    resourceType = Column(Unicode(128), nullable=False)


class DrydockLog(Base):
    __tablename__ = 'drydock_log'
    __table_args__ = (
        Index('resourceID', 'resourceID', 'epoch'),
        Index('leaseID', 'leaseID', 'epoch')
    )

    id = Column(Integer, primary_key=True)
    resourceID = Column(Integer)
    leaseID = Column(Integer)
    epoch = Column(Integer, nullable=False, index=True)
    message = Column(Unicode, nullable=False)


class DrydockReSource(Base):
    __tablename__ = 'drydock_resource'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)
    ownerPHID = Column(String)
    status = Column(Integer, nullable=False)
    type = Column(Unicode(64), nullable=False)
    attributes = Column(Unicode, nullable=False)
    capabilities = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    blueprintPHID = Column(String, nullable=False)
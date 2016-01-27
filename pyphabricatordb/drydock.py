# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.dialects.mysql.base import LONGBLOB
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class DrydockAuthorization(Base):
    __tablename__ = 'drydock_authorization'
    __table_args__ = (
        Index('key_object', 'objectPHID', 'objectAuthorizationState'),
        Index('key_blueprint', 'blueprintPHID', 'blueprintAuthorizationState'),
        Index('key_unique', 'objectPHID', 'blueprintPHID', unique=True)
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    blueprintPHID = Column(String, nullable=False)
    blueprintAuthorizationState = Column(Unicode(32), nullable=False)
    objectPHID = Column(String, nullable=False)
    objectAuthorizationState = Column(Unicode(32), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


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
    isDisabled = Column(Integer, nullable=False)


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


class DrydockCommand(Base):
    __tablename__ = 'drydock_command'
    __table_args__ = (
        Index('key_target', 'targetPHID', 'isConsumed'),
    )

    id = Column(Integer, primary_key=True)
    authorPHID = Column(String, nullable=False)
    targetPHID = Column(String, nullable=False)
    command = Column(Unicode(32), nullable=False)
    isConsumed = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class DrydockLease(Base):
    __tablename__ = 'drydock_lease'
    __table_args__ = (
        Index('key_resource', 'resourcePHID', 'status'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    status = Column(Unicode(32), nullable=False)
    until = Column(Integer)
    ownerPHID = Column(String)
    attributes = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    resourceType = Column(Unicode(128), nullable=False)
    resourcePHID = Column(String)
    authorizingPHID = Column(String, nullable=False)


class DrydockLog(Base):
    __tablename__ = 'drydock_log'
    __table_args__ = (
        Index('key_blueprint', 'blueprintPHID', 'type'),
        Index('key_lease', 'leasePHID', 'type'),
        Index('key_resource', 'resourcePHID', 'type')
    )

    id = Column(Integer, primary_key=True)
    epoch = Column(Integer, nullable=False, index=True)
    blueprintPHID = Column(String)
    resourcePHID = Column(String)
    leasePHID = Column(String)
    type = Column(Unicode(64), nullable=False)
    data = Column(Unicode, nullable=False)


class DrydockRepositoryoperation(Base):
    __tablename__ = 'drydock_repositoryoperation'
    __table_args__ = (
        Index('key_repository', 'repositoryPHID', 'operationState'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    repositoryPHID = Column(String, nullable=False)
    repositoryTarget = Column(LONGBLOB, nullable=False)
    operationType = Column(Unicode(32), nullable=False)
    operationState = Column(Unicode(32), nullable=False)
    properties = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    isDismissed = Column(Integer, nullable=False)


class DrydockResource(Base):
    __tablename__ = 'drydock_resource'
    __table_args__ = (
        Index('key_type', 'type', 'status'),
        Index('key_blueprint', 'blueprintPHID', 'status')
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    ownerPHID = Column(String)
    status = Column(Unicode(32), nullable=False)
    type = Column(Unicode(64), nullable=False)
    attributes = Column(Unicode, nullable=False)
    capabilities = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    blueprintPHID = Column(String, nullable=False)
    until = Column(Integer)


class DrydockSlotLock(Base):
    __tablename__ = 'drydock_slotlock'

    id = Column(Integer, primary_key=True)
    ownerPHID = Column(String, nullable=False, index=True)
    lockIndex = Column(BINARY(12), nullable=False, unique=True)
    lockKey = Column(Unicode, nullable=False)
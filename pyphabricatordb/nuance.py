# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY
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


class NuanceItem(Base):
    __tablename__ = 'nuance_item'
    __table_args__ = (
        Index('key_contacter', 'requestorPHID', 'status', 'dateNuanced', 'id'),
        Index('key_owner', 'ownerPHID', 'status', 'dateNuanced', 'id'),
        Index('key_source', 'sourcePHID', 'status', 'dateNuanced', 'id')
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    ownerPHID = Column(String)
    requestorPHID = Column(String, nullable=False)
    sourcePHID = Column(String, nullable=False)
    sourceLabel = Column(Unicode(255))
    status = Column(Integer, nullable=False)
    data = Column(Unicode, nullable=False)
    mailKey = Column(BINARY(20), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    dateNuanced = Column(dbdatetime, nullable=False)


class NuanceItemTransaction(Base):
    __tablename__ = 'nuance_itemtransaction'

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


class NuanceItemTransactionComment(Base):
    __tablename__ = 'nuance_itemtransaction_comment'
    __table_args__ = (
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    transactionPHID = Column(String)
    authorPHID = Column(String, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentVersion = Column(Integer, nullable=False)
    content = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    isDeleted = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class NuanceQueue(Base):
    __tablename__ = 'nuance_queue'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255))
    mailKey = Column(BINARY(20), nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class NuanceQueueItem(Base):
    __tablename__ = 'nuance_queueitem'
    __table_args__ = (
        Index('key_one_per_queue', 'itemPHID', 'queuePHID', unique=True),
        Index('key_queue', 'queuePHID', 'itemStatus', 'itemDateNuanced', 'id')
    )

    id = Column(Integer, primary_key=True)
    queuePHID = Column(String, nullable=False)
    itemPHID = Column(String, nullable=False)
    itemStatus = Column(Integer, nullable=False)
    itemDateNuanced = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class NuanceQueueTransaction(Base):
    __tablename__ = 'nuance_queuetransaction'

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


class NuanceQueueTransactionComment(Base):
    __tablename__ = 'nuance_queuetransaction_comment'
    __table_args__ = (
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    transactionPHID = Column(String)
    authorPHID = Column(String, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentVersion = Column(Integer, nullable=False)
    content = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    isDeleted = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class NuanceRequestor(Base):
    __tablename__ = 'nuance_requestor'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    data = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class NuanceRequestorSource(Base):
    __tablename__ = 'nuance_requestorsource'
    __table_args__ = (
        Index('key_source_key', 'sourcePHID', 'sourceKey', unique=True),
        Index('key_source', 'sourcePHID', 'id'),
        Index('key_requestor', 'requestorPHID', 'id')
    )

    id = Column(Integer, primary_key=True)
    requestorPHID = Column(String, nullable=False)
    sourcePHID = Column(String, nullable=False)
    sourceKey = Column(Unicode(128), nullable=False)
    data = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class NuanceRequestorTransaction(Base):
    __tablename__ = 'nuance_requestortransaction'

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


class NuanceRequestorTransactionComment(Base):
    __tablename__ = 'nuance_requestortransaction_comment'
    __table_args__ = (
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    transactionPHID = Column(String)
    authorPHID = Column(String, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentVersion = Column(Integer, nullable=False)
    content = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    isDeleted = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class NuanceSource(Base):
    __tablename__ = 'nuance_source'
    __table_args__ = (
        Index('key_type', 'type', 'dateModified'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255))
    type = Column(Unicode(32), nullable=False)
    data = Column(Unicode, nullable=False)
    mailKey = Column(BINARY(20), nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class NuanceSourceTransaction(Base):
    __tablename__ = 'nuance_sourcetransaction'

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


class NuanceSourceTransactionComment(Base):
    __tablename__ = 'nuance_sourcetransaction_comment'
    __table_args__ = (
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    transactionPHID = Column(String)
    authorPHID = Column(String, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentVersion = Column(Integer, nullable=False)
    content = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    isDeleted = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
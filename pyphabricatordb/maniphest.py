# coding: utf-8
from sqlalchemy import BINARY, BigInteger, Column, Float, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Edge(Base):
    __tablename__ = 'edge'
    __table_args__ = (
        Index('src', 'src', 'type', 'dateCreated', 'seq'),
        Index('key_dst', 'dst', 'type', 'src', unique=True)
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


class CustomFieldNumericIndex(Base):
    __tablename__ = 'maniphest_customfieldnumericindex'
    __table_args__ = (
        Index('key_find', 'indexKey', 'indexValue'),
        Index('key_join', 'objectPHID', 'indexKey', 'indexValue')
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    indexKey = Column(BINARY(12), nullable=False)
    indexValue = Column(BigInteger, nullable=False)


class CustomFieldStorage(Base):
    __tablename__ = 'maniphest_customfieldstorage'
    __table_args__ = (
        Index('objectPHID', 'objectPHID', 'fieldIndex', unique=True),
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, ForeignKey("maniphest_task.phid"), nullable=False)
    fieldIndex = Column(BINARY(12), nullable=False)
    fieldValue = Column(Unicode, nullable=False)


class CustomFieldStringIndex(Base):
    __tablename__ = 'maniphest_customfieldstringindex'
    __table_args__ = (
        Index('key_find', 'indexKey', 'indexValue'),
        Index('key_join', 'objectPHID', 'indexKey', 'indexValue')
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    indexKey = Column(BINARY(12), nullable=False)
    indexValue = Column(Unicode, nullable=False)


class NameIndex(Base):
    __tablename__ = 'maniphest_nameindex'

    id = Column(Integer, primary_key=True)
    indexedObjectPHID = Column(String, nullable=False, unique=True)
    indexedObjectName = Column(Unicode(128), nullable=False, index=True)


class Task(Base):
    __tablename__ = 'maniphest_task'
    __table_args__ = (
        Index('ownerPHID', 'ownerPHID', 'status'),
        Index('priority_2', 'priority', 'subpriority'),
        Index('authorPHID', 'authorPHID', 'status'),
        Index('priority', 'priority', 'status')
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    ownerPHID = Column(String)
    attached = Column(Unicode, nullable=False)
    status = Column(Unicode(12), nullable=False, index=True)
    priority = Column(Integer, nullable=False)
    title = Column(Unicode, nullable=False, index=True)
    originalTitle = Column(Unicode, nullable=False)
    description = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False, index=True)
    projectPHIDs = Column(Unicode, nullable=False)
    mailKey = Column(BINARY(20), nullable=False)
    ownerOrdering = Column(Unicode(64), index=True)
    originalEmailSource = Column(Unicode(255))
    subpriority = Column(Float(asdecimal=True), nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)

    subscribers = relationship('TaskSubscriber', backref='task')
    transactions = relationship('Transaction', backref='task')
    customFieldStorages = relationship('CustomFieldStorage', backref='task')


class TaskSubscriber(Base):
    __tablename__ = 'maniphest_tasksubscriber'
    __table_args__ = (
        Index('taskPHID', 'taskPHID', 'subscriberPHID', unique=True),
    )

    taskPHID = Column(String, ForeignKey("maniphest_task.phid"), primary_key=True, nullable=False)
    subscriberPHID = Column(String, primary_key=True, nullable=False)


class Transaction(Base):
    __tablename__ = 'maniphest_transaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, ForeignKey("maniphest_task.phid"), nullable=False, index=True)
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

    comment = relationship('TransactionComment', uselist=False, backref='transaction')


class TransactionComment(Base):
    __tablename__ = 'maniphest_transaction_comment'
    __table_args__ = (
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    transactionPHID = Column(String, ForeignKey("maniphest_transaction.phid"))
    authorPHID = Column(String, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentVersion = Column(Integer, nullable=False)
    content = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    isDeleted = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
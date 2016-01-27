# coding: utf-8
from sqlalchemy import BigInteger, Column, Index, Integer, String, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class ConpherenceIndex(Base):
    __tablename__ = 'conpherence_index'

    id = Column(Integer, primary_key=True)
    threadPHID = Column(String, nullable=False, index=True)
    transactionPHID = Column(String, nullable=False, unique=True)
    previousTransactionPHID = Column(String, unique=True)
    corpus = Column(Unicode, nullable=False, index=True)


class ConpherenceParticipant(Base):
    __tablename__ = 'conpherence_participant'
    __table_args__ = (
        Index('conpherencePHID', 'conpherencePHID', 'participantPHID', unique=True),
        Index('unreadCount', 'participantPHID', 'participationStatus'),
        Index('participationIndex', 'participantPHID', 'dateTouched', 'id')
    )

    id = Column(Integer, primary_key=True)
    participantPHID = Column(String, nullable=False)
    conpherencePHID = Column(String, nullable=False)
    participationStatus = Column(Integer, nullable=False, server_default=text("'0'"))
    dateTouched = Column(dbdatetime, nullable=False)
    behindTransactionPHID = Column(String, nullable=False)
    seenMessageCount = Column(BigInteger, nullable=False)
    settings = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class ConpherenceThread(Base):
    __tablename__ = 'conpherence_thread'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    title = Column(Unicode(255))
    imagePHIDs = Column(Unicode, nullable=False)
    messageCount = Column(BigInteger, nullable=False)
    recentParticipantPHIDs = Column(Unicode, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    joinPolicy = Column(String, nullable=False)
    mailKey = Column(Unicode(20), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class ConpherenceTransaction(Base):
    __tablename__ = 'conpherence_transaction'

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
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)


class ConpherenceTransactionComment(Base):
    __tablename__ = 'conpherence_transaction_comment'
    __table_args__ = (
        Index('key_draft', 'authorPHID', 'conpherencePHID', 'transactionPHID', unique=True),
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True)
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
    conpherencePHID = Column(String)


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
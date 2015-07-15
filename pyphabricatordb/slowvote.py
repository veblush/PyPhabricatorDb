# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY
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


class SlowvoteChoice(Base):
    __tablename__ = 'slowvote_choice'

    id = Column(Integer, primary_key=True)
    pollID = Column(Integer, nullable=False, index=True)
    optionID = Column(Integer, nullable=False)
    authorPHID = Column(String, nullable=False, index=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class SlowvoteOption(Base):
    __tablename__ = 'slowvote_option'

    id = Column(Integer, primary_key=True)
    pollID = Column(Integer, nullable=False, index=True)
    name = Column(Unicode(255), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class SlowvotePoll(Base):
    __tablename__ = 'slowvote_poll'

    id = Column(Integer, primary_key=True)
    question = Column(Unicode(255), nullable=False)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    responseVisibility = Column(Integer, nullable=False)
    shuffle = Column(Integer, nullable=False)
    method = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    description = Column(Unicode, nullable=False)
    viewPolicy = Column(String, nullable=False)
    isClosed = Column(Integer, nullable=False)
    spacePHID = Column(String, index=True)


class SlowvoteTransaction(Base):
    __tablename__ = 'slowvote_transaction'

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


class SlowvoteTransactionComment(Base):
    __tablename__ = 'slowvote_transaction_comment'
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
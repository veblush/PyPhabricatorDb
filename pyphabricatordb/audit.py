# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AuditTransaction(Base):
    __tablename__ = 'audit_transaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String, ForeignKey("audit_transaction_comment.phid"))
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)

    comment = relationship('AuditTransactionComment', uselist=False, backref='transaction')


class AuditTransactionComment(Base):
    __tablename__ = 'audit_transaction_comment'
    __table_args__ = (
        Index('key_draft', 'authorPHID', 'transactionPHID'),
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
    commitPHID = Column(String, index=True)
    pathID = Column(Integer, index=True)
    isNewFile = Column(Integer, nullable=False)
    lineNumber = Column(Integer, nullable=False)
    lineLength = Column(Integer, nullable=False)
    fixedState = Column(Unicode(12))
    hasReplies = Column(Integer, nullable=False)
    replyToCommentPHID = Column(String)
    legacyCommentID = Column(Integer, index=True)
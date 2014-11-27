# coding: utf-8
from sqlalchemy import Column, Float, Index, Integer, String, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.dialects.mysql.base import LONGBLOB
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class HeraldAction(Base):
    __tablename__ = 'herald_action'

    id = Column(Integer, primary_key=True)
    ruleID = Column(Integer, nullable=False, index=True)
    action = Column(Unicode(255), nullable=False)
    target = Column(Unicode, nullable=False)


class HeraldCondition(Base):
    __tablename__ = 'herald_condition'

    id = Column(Integer, primary_key=True)
    ruleID = Column(Integer, nullable=False, index=True)
    fieldName = Column(Unicode(255), nullable=False)
    fieldCondition = Column(Unicode(255), nullable=False)
    value = Column(Unicode, nullable=False)


class HeraldRule(Base):
    __tablename__ = 'herald_rule'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    authorPHID = Column(String, nullable=False, index=True)
    contentType = Column(Unicode(255), nullable=False)
    mustMatchAll = Column(Integer, nullable=False)
    configVersion = Column(Integer, nullable=False, server_default=text("'1'"))
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    repetitionPolicy = Column(Integer)
    ruleType = Column(Unicode(32), nullable=False, index=True)
    phid = Column(String, nullable=False, unique=True)
    isDisabled = Column(Integer, nullable=False, server_default=text("'0'"))
    triggerObjectPHID = Column(String, index=True)


class HeraldRuleApplied(Base):
    __tablename__ = 'herald_ruleapplied'

    ruleID = Column(Integer, primary_key=True, nullable=False)
    phid = Column(String, primary_key=True, nullable=False, index=True)


class HeraldRuleEdit(Base):
    __tablename__ = 'herald_ruleedit'
    __table_args__ = (
        Index('ruleID', 'ruleID', 'dateCreated'),
    )

    id = Column(Integer, primary_key=True)
    ruleID = Column(Integer, nullable=False)
    editorPHID = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    ruleName = Column(Unicode(255), nullable=False)
    action = Column(Unicode(32), nullable=False)


class HeraldRuleTransaction(Base):
    __tablename__ = 'herald_ruletransaction'

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


class HeraldRuleTransactionComment(Base):
    __tablename__ = 'herald_ruletransaction_comment'
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


class HeraldSavedHeader(Base):
    __tablename__ = 'herald_savedheader'

    phid = Column(String, primary_key=True)
    header = Column(Unicode, nullable=False)


class HeraldTranscript(Base):
    __tablename__ = 'herald_transcript'
    __table_args__ = (
        Index('garbageCollected', 'garbageCollected', 'time'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    time = Column(Integer, nullable=False)
    host = Column(Unicode(255), nullable=False)
    duration = Column(Float(asdecimal=True), nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    dryRun = Column(Integer, nullable=False)
    objectTranscript = Column(LONGBLOB, nullable=False)
    ruleTranscripts = Column(LONGBLOB, nullable=False)
    conditionTranscripts = Column(LONGBLOB, nullable=False)
    applyTranscripts = Column(LONGBLOB, nullable=False)
    garbageCollected = Column(Integer, nullable=False, server_default=text("'0'"))
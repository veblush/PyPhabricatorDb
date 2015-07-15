# coding: utf-8
from sqlalchemy import BINARY, Column, Date, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class CalendarEvent(Base):
    __tablename__ = 'calendar_event'
    __table_args__ = (
        Index('userPHID_dateFrom', 'userPHID', 'dateTo'),
        Index('key_instance', 'instanceOfEventPHID', 'sequenceIndex', unique=True)
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    userPHID = Column(String, nullable=False)
    dateFrom = Column(dbdatetime, nullable=False)
    dateTo = Column(dbdatetime, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    description = Column(Unicode, nullable=False)
    isCancelled = Column(Integer, nullable=False)
    name = Column(Unicode, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    mailKey = Column(BINARY(20), nullable=False)
    isAllDay = Column(Integer, nullable=False)
    icon = Column(Unicode(32), nullable=False)
    isRecurring = Column(Integer, nullable=False)
    recurrenceFrequency = Column(Unicode, nullable=False)
    recurrenceEndDate = Column(Integer)
    instanceOfEventPHID = Column(String)
    sequenceIndex = Column(Integer)
    spacePHID = Column(String, index=True)


class CalendarEventInvitee(Base):
    __tablename__ = 'calendar_eventinvitee'
    __table_args__ = (
        Index('key_event', 'eventPHID', 'inviteePHID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    eventPHID = Column(String, nullable=False)
    inviteePHID = Column(String, nullable=False, index=True)
    inviterPHID = Column(String, nullable=False)
    status = Column(Unicode(64), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class CalendarEventTransaction(Base):
    __tablename__ = 'calendar_eventtransaction'

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


class CalendarEventTransactionComment(Base):
    __tablename__ = 'calendar_eventtransaction_comment'
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


class CalendarHoliday(Base):
    __tablename__ = 'calendar_holiday'

    id = Column(Integer, primary_key=True)
    day = Column(Date, nullable=False, unique=True)
    name = Column(Unicode(64), nullable=False)


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
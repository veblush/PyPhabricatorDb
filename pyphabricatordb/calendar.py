# coding: utf-8
from sqlalchemy import Column, Date, Index, Integer, String, VARBINARY
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
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    userPHID = Column(String, nullable=False)
    dateFrom = Column(dbdatetime, nullable=False)
    dateTo = Column(dbdatetime, nullable=False)
    status = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    description = Column(Unicode, nullable=False)


class CalendarHoliday(Base):
    __tablename__ = 'calendar_holiday'

    id = Column(Integer, primary_key=True)
    day = Column(Date, nullable=False, unique=True)
    name = Column(Unicode(64), nullable=False)
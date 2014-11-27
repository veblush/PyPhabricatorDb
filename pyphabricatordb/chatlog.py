# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class ChatLogChannel(Base):
    __tablename__ = 'chatlog_channel'
    __table_args__ = (
        Index('key_channel', 'channelName', 'serviceType', 'serviceName', unique=True),
    )

    id = Column(Integer, primary_key=True)
    serviceName = Column(Unicode(64), nullable=False)
    serviceType = Column(Unicode(32), nullable=False)
    channelName = Column(Unicode(64), nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class ChatLogEvent(Base):
    __tablename__ = 'chatlog_event'

    id = Column(Integer, primary_key=True)
    epoch = Column(Integer, nullable=False, index=True)
    author = Column(Unicode(64), nullable=False)
    type = Column(Unicode(4), nullable=False)
    message = Column(Unicode, nullable=False)
    loggedByPHID = Column(String, nullable=False)
    channelID = Column(Integer, nullable=False)
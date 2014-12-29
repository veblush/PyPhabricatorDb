# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class DaemonLog(Base):
    __tablename__ = 'daemon_log'

    id = Column(Integer, primary_key=True)
    daemon = Column(Unicode(255), nullable=False)
    host = Column(Unicode(255), nullable=False)
    pid = Column(Integer, nullable=False)
    argv = Column(Unicode, nullable=False)
    explicitArgv = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)
    envHash = Column(BINARY(40), nullable=False)
    status = Column(Unicode(8), nullable=False, index=True)
    runningAsUser = Column(Unicode(255))


class DaemonLogEvent(Base):
    __tablename__ = 'daemon_logevent'
    __table_args__ = (
        Index('logID', 'logID', 'epoch'),
    )

    id = Column(Integer, primary_key=True)
    logID = Column(Integer, nullable=False)
    logType = Column(Unicode(4), nullable=False)
    message = Column(Unicode, nullable=False)
    epoch = Column(Integer, nullable=False)
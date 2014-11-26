# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class XhprofSample(Base):
    __tablename__ = 'xhprof_sample'

    id = Column(Integer, primary_key=True)
    filePHID = Column(String, nullable=False, unique=True)
    sampleRate = Column(Integer, nullable=False)
    usTotal = Column(BigInteger, nullable=False)
    hostname = Column(Unicode(255))
    requestPath = Column(Unicode(255))
    controller = Column(Unicode(255))
    userPHID = Column(String)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
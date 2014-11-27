# coding: utf-8
from sqlalchemy import Column, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class PhrequentUserTime(Base):
    __tablename__ = 'phrequent_usertime'

    id = Column(Integer, primary_key=True)
    userPHID = Column(String, nullable=False)
    objectPHID = Column(String)
    note = Column(Unicode)
    dateStarted = Column(dbdatetime, nullable=False)
    dateEnded = Column(Integer)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
# coding: utf-8
from sqlalchemy import Column, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class CountDown(Base):
    __tablename__ = 'countdown'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    title = Column(Unicode(255), nullable=False)
    authorPHID = Column(String, nullable=False)
    epoch = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    viewPolicy = Column(String, nullable=False)
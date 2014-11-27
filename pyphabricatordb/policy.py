# coding: utf-8
from sqlalchemy import Column, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Policy(Base):
    __tablename__ = 'policy'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    rules = Column(Unicode, nullable=False)
    defaultAction = Column(Unicode(32), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
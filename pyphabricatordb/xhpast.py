# coding: utf-8
from sqlalchemy import Column, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class XhpastParsetree(Base):
    __tablename__ = 'xhpast_parsetree'

    id = Column(Integer, primary_key=True)
    authorPHID = Column(String)
    input = Column(Unicode, nullable=False)
    returnCode = Column(Integer, nullable=False)
    stdout = Column(Unicode, nullable=False)
    stderr = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
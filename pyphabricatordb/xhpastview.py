# coding: utf-8
from sqlalchemy import Column, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class XhpastviewParseTree(Base):
    __tablename__ = 'xhpastview_parsetree'

    id = Column(Integer, primary_key=True)
    authorPHID = Column(String)
    input = Column(Unicode, nullable=False)
    stdout = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
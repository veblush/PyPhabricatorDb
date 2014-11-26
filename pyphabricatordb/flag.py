# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Flag(Base):
    __tablename__ = 'flag'
    __table_args__ = (
        Index('ownerPHID', 'ownerPHID', 'type', 'objectPHID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    ownerPHID = Column(String, nullable=False)
    type = Column(Unicode(4), nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    reasonPHID = Column(String, nullable=False)
    color = Column(Integer, nullable=False)
    note = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
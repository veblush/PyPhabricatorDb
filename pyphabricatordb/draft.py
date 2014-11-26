# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Draft(Base):
    __tablename__ = 'draft'
    __table_args__ = (
        Index('authorPHID', 'authorPHID', 'draftKey', unique=True),
    )

    id = Column(Integer, primary_key=True)
    authorPHID = Column(String, nullable=False)
    draftKey = Column(Unicode(64), nullable=False)
    draft = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
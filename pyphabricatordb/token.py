# coding: utf-8
from sqlalchemy import Column, Index, Integer, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class TokenCount(Base):
    __tablename__ = 'token_count'

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False, unique=True)
    tokenCount = Column(Integer, nullable=False, index=True)


class TokenGiven(Base):
    __tablename__ = 'token_given'
    __table_args__ = (
        Index('key_all', 'objectPHID', 'authorPHID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    authorPHID = Column(String, nullable=False, index=True)
    tokenPHID = Column(String, nullable=False, index=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
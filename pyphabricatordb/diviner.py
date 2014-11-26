# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class DivinerLiveAtom(Base):
    __tablename__ = 'diviner_liveatom'

    id = Column(Integer, primary_key=True)
    symbolPHID = Column(String, nullable=False, unique=True)
    content = Column(Unicode, nullable=False)
    atomData = Column(Unicode, nullable=False)


class DivinerLiveBook(Base):
    __tablename__ = 'diviner_livebook'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(64), nullable=False, unique=True)
    viewPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    configurationData = Column(Unicode, nullable=False)


class DivinerLiveSymbol(Base):
    __tablename__ = 'diviner_livesymbol'
    __table_args__ = (
        Index('bookPHID', 'bookPHID', 'type', 'name', 'context', 'atomIndex'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    bookPHID = Column(String, nullable=False)
    context = Column(Unicode(255))
    type = Column(Unicode(32), nullable=False)
    name = Column(Unicode(255), nullable=False, index=True)
    atomIndex = Column(Integer, nullable=False)
    identityHash = Column(BINARY(12), nullable=False, unique=True)
    graphHash = Column(Unicode(64), unique=True)
    title = Column(Unicode)
    titleSlugHash = Column(BINARY(12), index=True)
    groupName = Column(Unicode(255))
    summary = Column(Unicode)
    isDocumentable = Column(Integer, nullable=False)
    nodeHash = Column(Unicode(64), unique=True)
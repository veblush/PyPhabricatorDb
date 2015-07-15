# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
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
    repositoryPHID = Column(String)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    configurationData = Column(Unicode, nullable=False)


class DivinerLiveBookTransaction(Base):
    __tablename__ = 'diviner_livebooktransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class DivinerLiveSymbol(Base):
    __tablename__ = 'diviner_livesymbol'
    __table_args__ = (
        Index('bookPHID', 'bookPHID', 'type', 'name', 'context', 'atomIndex'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    bookPHID = Column(String, nullable=False)
    repositoryPHID = Column(String)
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


class Edge(Base):
    __tablename__ = 'edge'
    __table_args__ = (
        Index('src', 'src', 'type', 'dateCreated', 'seq'),
        Index('key_dst', 'dst', 'type', 'src', unique=True)
    )

    src = Column(String, primary_key=True, nullable=False)
    type = Column(Integer, primary_key=True, nullable=False)
    dst = Column(String, primary_key=True, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    seq = Column(Integer, nullable=False)
    dataID = Column(Integer)


class EdgeData(Base):
    __tablename__ = 'edgedata'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode, nullable=False)
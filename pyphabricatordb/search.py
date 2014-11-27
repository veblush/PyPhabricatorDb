# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, Table, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class SearchDocument(Base):
    __tablename__ = 'search_document'

    phid = Column(String, primary_key=True)
    documentType = Column(Unicode(4), nullable=False)
    documentTitle = Column(Unicode(255), nullable=False)
    documentCreated = Column(Integer, nullable=False, index=True)
    documentModified = Column(Integer, nullable=False)


t_search_documentfield = Table(
    'search_documentfield', metadata,
    Column('phid', String, nullable=False, index=True),
    Column('phidType', Unicode(4), nullable=False),
    Column('field', Unicode(4), nullable=False),
    Column('auxPHID', String),
    Column('corpus', Unicode, index=True)
)


t_search_documentrelationship = Table(
    'search_documentrelationship', metadata,
    Column('phid', String, nullable=False, index=True),
    Column('relatedPHID', String, nullable=False),
    Column('relation', Unicode(4), nullable=False),
    Column('relatedType', Unicode(4), nullable=False),
    Column('relatedTime', Integer, nullable=False),
    Index('relatedPHID', 'relatedPHID', 'relation'),
    Index('relation', 'relation', 'relatedPHID')
)


class SearchNamedQuery(Base):
    __tablename__ = 'search_namedquery'
    __table_args__ = (
        Index('key_userquery', 'userPHID', 'engineClassName', 'queryKey', unique=True),
    )

    id = Column(Integer, primary_key=True)
    userPHID = Column(String, nullable=False)
    engineClassName = Column(Unicode(128), nullable=False)
    queryName = Column(Unicode(255), nullable=False)
    queryKey = Column(Unicode(12), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    isBuiltin = Column(Integer, nullable=False, server_default=text("'0'"))
    isDisabled = Column(Integer, nullable=False, server_default=text("'0'"))
    sequence = Column(Integer, nullable=False, server_default=text("'0'"))


class SearchSavedQuery(Base):
    __tablename__ = 'search_savedquery'

    id = Column(Integer, primary_key=True)
    engineClassName = Column(Unicode(255), nullable=False)
    parameters = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    queryKey = Column(Unicode(12), nullable=False, unique=True)
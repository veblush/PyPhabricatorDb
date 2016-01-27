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
    Index('relation', 'relation', 'relatedPHID'),
    Index('relatedPHID', 'relatedPHID', 'relation')
)


class SearchEditEngineConfiguration(Base):
    __tablename__ = 'search_editengineconfiguration'
    __table_args__ = (
        Index('key_edit', 'engineKey', 'isEdit', 'isDisabled'),
        Index('key_default', 'engineKey', 'isDefault', 'isDisabled'),
        Index('key_engine', 'engineKey', 'builtinKey', unique=True)
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    engineKey = Column(Unicode(64), nullable=False)
    builtinKey = Column(Unicode(64))
    name = Column(Unicode(255), nullable=False)
    viewPolicy = Column(String, nullable=False)
    properties = Column(Unicode, nullable=False)
    isDisabled = Column(Integer, nullable=False, server_default=text("'0'"))
    isDefault = Column(Integer, nullable=False, server_default=text("'0'"))
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    isEdit = Column(Integer, nullable=False)
    createOrder = Column(Integer, nullable=False)
    editOrder = Column(Integer, nullable=False)


class SearchEditEngineConfigurationTransaction(Base):
    __tablename__ = 'search_editengineconfigurationtransaction'

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


class SearchIndexVersion(Base):
    __tablename__ = 'search_indexversion'
    __table_args__ = (
        Index('key_object', 'objectPHID', 'extensionKey', unique=True),
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    extensionKey = Column(Unicode(64), nullable=False)
    version = Column(Unicode(128), nullable=False)


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


class SearchProfilePanelConfiguration(Base):
    __tablename__ = 'search_profilepanelconfiguration'
    __table_args__ = (
        Index('key_profile', 'profilePHID', 'panelOrder'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    profilePHID = Column(String, nullable=False)
    panelKey = Column(Unicode(64), nullable=False)
    builtinKey = Column(Unicode(64))
    panelOrder = Column(Integer)
    visibility = Column(Unicode(32), nullable=False)
    panelProperties = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class SearchProfilePanelConfigurationTransaction(Base):
    __tablename__ = 'search_profilepanelconfigurationtransaction'

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


class SearchSavedQuery(Base):
    __tablename__ = 'search_savedquery'

    id = Column(Integer, primary_key=True)
    engineClassName = Column(Unicode(255), nullable=False)
    parameters = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    queryKey = Column(Unicode(12), nullable=False, unique=True)
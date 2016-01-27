# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AuthFactorConfig(Base):
    __tablename__ = 'auth_factorconfig'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    userPHID = Column(String, nullable=False, index=True)
    factorKey = Column(Unicode(64), nullable=False)
    factorName = Column(Unicode, nullable=False)
    factorSecret = Column(Unicode, nullable=False)
    properties = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class AuthProviderConfig(Base):
    __tablename__ = 'auth_providerconfig'
    __table_args__ = (
        Index('key_provider', 'providerType', 'providerDomain', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    providerClass = Column(Unicode(128), nullable=False, index=True)
    providerType = Column(Unicode(32), nullable=False)
    providerDomain = Column(Unicode(128), nullable=False)
    isEnabled = Column(Integer, nullable=False)
    shouldAllowLogin = Column(Integer, nullable=False)
    shouldAllowRegistration = Column(Integer, nullable=False)
    shouldAllowLink = Column(Integer, nullable=False)
    shouldAllowUnlink = Column(Integer, nullable=False)
    shouldTrustEmails = Column(Integer, nullable=False, server_default=text("'0'"))
    properties = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    shouldAutoLogin = Column(Integer, nullable=False, server_default=text("'0'"))


class AuthProviderConfigTransaction(Base):
    __tablename__ = 'auth_providerconfigtransaction'

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
    usermetadata = Column('metadata', Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class AuthSSHkey(Base):
    __tablename__ = 'auth_sshkey'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    objectPHID = Column(String, nullable=False, index=True)
    name = Column(Unicode(255), nullable=False)
    keyType = Column(Unicode(255), nullable=False)
    keyBody = Column(Unicode, nullable=False)
    keyComment = Column(Unicode(255), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    keyIndex = Column(BINARY(12), nullable=False, unique=True)
    isTrusted = Column(Integer, nullable=False)


class AuthTemporaryToken(Base):
    __tablename__ = 'auth_temporarytoken'
    __table_args__ = (
        Index('key_token', 'objectPHID', 'tokenType', 'tokenCode', unique=True),
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    tokenType = Column(Unicode(64), nullable=False)
    tokenExpires = Column(Integer, nullable=False, index=True)
    tokenCode = Column(Unicode(64), nullable=False)
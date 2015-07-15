# coding: utf-8
from sqlalchemy import BINARY, BigInteger, Column, Index, Integer, String, Table, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


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


class PhabricatorSession(Base):
    __tablename__ = 'phabricator_session'
    __table_args__ = (
        Index('key_identity', 'userPHID', 'type'),
    )

    id = Column(Integer, primary_key=True)
    userPHID = Column(String, nullable=False)
    type = Column(Unicode(32), nullable=False)
    sessionKey = Column(BINARY(40), nullable=False, unique=True)
    sessionStart = Column(Integer, nullable=False)
    sessionExpires = Column(Integer, nullable=False, index=True)
    highSecurityUntil = Column(Integer)
    isPartial = Column(Integer, nullable=False, server_default=text("'0'"))
    signedLegalpadDocuments = Column(Integer, nullable=False, server_default=text("'0'"))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    userName = Column(Unicode(64), nullable=False, unique=True)
    realName = Column(Unicode(128), nullable=False, index=True)
    sex = Column(Unicode(4))
    translation = Column(Unicode(64))
    passwordSalt = Column(Unicode(32))
    passwordHash = Column(Unicode(128))
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    profileImagePHID = Column(String)
    consoleEnabled = Column(Integer, nullable=False)
    consoleVisible = Column(Integer, nullable=False)
    consoleTab = Column(Unicode(64), nullable=False)
    conduitCertificate = Column(Unicode(255), nullable=False)
    isSystemAgent = Column(Integer, nullable=False, server_default=text("'0'"))
    isDisabled = Column(Integer, nullable=False)
    isAdmin = Column(Integer, nullable=False)
    timezoneIdentifier = Column(Unicode(255), nullable=False)
    isEmailVerified = Column(Integer, nullable=False)
    isApproved = Column(Integer, nullable=False, index=True)
    accountSecret = Column(BINARY(64), nullable=False)
    isEnrolledInMultiFactor = Column(Integer, nullable=False, server_default=text("'0'"))
    profileImageCache = Column(Unicode(255))
    availabilityCache = Column(Unicode(255))
    availabilityCacheTTL = Column(Integer)
    isMailingList = Column(Integer, nullable=False)

    emails = relationship('UserEmail', backref='user')
    externalAccounts = relationship('UserExternalAccount', backref='user')
    logs = relationship('UserLog', backref='user')
    preferences = relationship('UserPreferences', uselist=False, backref='user')
    profile = relationship('UserProfile', uselist=False, backref='user')
    transactions = relationship('UserTransaction', backref='user')


class UserAuthInvite(Base):
    __tablename__ = 'user_authinvite'

    id = Column(Integer, primary_key=True)
    authorPHID = Column(String, nullable=False)
    emailAddress = Column(Unicode(128), nullable=False, unique=True)
    verificationHash = Column(BINARY(12), nullable=False, unique=True)
    acceptedByPHID = Column(String)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    phid = Column(String, nullable=False, unique=True)


class UserConfiguredCustomFieldStorage(Base):
    __tablename__ = 'user_configuredcustomfieldstorage'
    __table_args__ = (
        Index('objectPHID', 'objectPHID', 'fieldIndex', unique=True),
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    fieldIndex = Column(BINARY(12), nullable=False)
    fieldValue = Column(Unicode, nullable=False)


class UserCustomFieldNumericIndex(Base):
    __tablename__ = 'user_customfieldnumericindex'
    __table_args__ = (
        Index('key_join', 'objectPHID', 'indexKey', 'indexValue'),
        Index('key_find', 'indexKey', 'indexValue')
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    indexKey = Column(BINARY(12), nullable=False)
    indexValue = Column(BigInteger, nullable=False)


class UserCustomFieldStringIndex(Base):
    __tablename__ = 'user_customfieldstringindex'
    __table_args__ = (
        Index('key_find', 'indexKey', 'indexValue'),
        Index('key_join', 'objectPHID', 'indexKey', 'indexValue')
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    indexKey = Column(BINARY(12), nullable=False)
    indexValue = Column(Unicode, nullable=False)


class UserEmail(Base):
    __tablename__ = 'user_email'
    __table_args__ = (
        Index('userPHID', 'userPHID', 'isPrimary'),
    )

    id = Column(Integer, primary_key=True)
    userPHID = Column(String, ForeignKey("user.phid"), nullable=False)
    address = Column(Unicode(128), nullable=False, unique=True)
    isVerified = Column(Integer, nullable=False, server_default=text("'0'"))
    isPrimary = Column(Integer, nullable=False, server_default=text("'0'"))
    verificationCode = Column(Unicode(64))
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class UserExternalAccount(Base):
    __tablename__ = 'user_externalaccount'
    __table_args__ = (
        Index('account_details', 'accountType', 'accountDomain', 'accountID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    userPHID = Column(String, ForeignKey("user.phid"))
    accountType = Column(Unicode(16), nullable=False)
    accountDomain = Column(Unicode(64), nullable=False)
    accountSecret = Column(Unicode)
    accountID = Column(Unicode(64), nullable=False)
    displayName = Column(Unicode(255))
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    username = Column(Unicode(255))
    realName = Column(Unicode(255))
    email = Column(Unicode(255))
    emailVerified = Column(Integer, nullable=False)
    accountURI = Column(Unicode(255))
    profileImagePHID = Column(String)
    properties = Column(Unicode, nullable=False)


class UserLog(Base):
    __tablename__ = 'user_log'
    __table_args__ = (
        Index('action', 'action', 'dateCreated'),
        Index('remoteAddr', 'remoteAddr', 'dateCreated'),
        Index('session', 'session', 'dateCreated'),
        Index('actorPHID', 'actorPHID', 'dateCreated'),
        Index('userPHID', 'userPHID', 'dateCreated')
    )

    id = Column(Integer, primary_key=True)
    actorPHID = Column(String)
    userPHID = Column(String, ForeignKey("user.phid"), nullable=False)
    action = Column(Unicode(64), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    details = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)
    remoteAddr = Column(Unicode(64), nullable=False)
    session = Column(BINARY(40))


t_user_nametoken = Table(
    'user_nametoken', metadata,
    Column('token', Unicode(255), nullable=False, index=True),
    Column('userID', Integer, nullable=False, index=True)
)


class UserPreferences(Base):
    __tablename__ = 'user_preferences'

    id = Column(Integer, primary_key=True)
    userPHID = Column(String, ForeignKey("user.phid"), nullable=False, unique=True)
    preferences = Column(Unicode, nullable=False)


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id = Column(Integer, primary_key=True)
    userPHID = Column(String, ForeignKey("user.phid"), nullable=False, unique=True)
    title = Column(Unicode(255), nullable=False)
    blurb = Column(Unicode, nullable=False)
    profileImagePHID = Column(String)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class UserTransaction(Base):
    __tablename__ = 'user_transaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, ForeignKey("user.phid"), nullable=False)
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
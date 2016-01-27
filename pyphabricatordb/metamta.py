# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY
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


class MetaMtaApplicationeMail(Base):
    __tablename__ = 'metamta_applicationemail'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    applicationPHID = Column(String, nullable=False, index=True)
    address = Column(Unicode(128), nullable=False, unique=True)
    configData = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    spacePHID = Column(String, index=True)


class MetaMtaApplicationeMailTransaction(Base):
    __tablename__ = 'metamta_applicationemailtransaction'

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


class MetaMtaMail(Base):
    __tablename__ = 'metamta_mail'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    actorPHID = Column(String, index=True)
    parameters = Column(Unicode, nullable=False)
    status = Column(Unicode(32), nullable=False, index=True)
    message = Column(Unicode)
    relatedPHID = Column(String, index=True)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)


class MetaMtaReceivedMail(Base):
    __tablename__ = 'metamta_receivedmail'

    id = Column(Integer, primary_key=True)
    headers = Column(Unicode, nullable=False)
    bodies = Column(Unicode, nullable=False)
    attachments = Column(Unicode, nullable=False)
    relatedPHID = Column(String, index=True)
    authorPHID = Column(String, index=True)
    message = Column(Unicode)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)
    messageIDHash = Column(BINARY(12), nullable=False, index=True)
    status = Column(Unicode(32), nullable=False)


class SMS(Base):
    __tablename__ = 'sms'
    __table_args__ = (
        Index('key_provider', 'providerSMSID', 'providerShortName', unique=True),
    )

    id = Column(Integer, primary_key=True)
    providerShortName = Column(Unicode(16), nullable=False)
    providerSMSID = Column(Unicode(40), nullable=False)
    toNumber = Column(Unicode(20), nullable=False)
    fromNumber = Column(Unicode(20))
    body = Column(Unicode, nullable=False)
    sendStatus = Column(Unicode(16))
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
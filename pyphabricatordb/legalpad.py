# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY, text
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


class LegalpadDocument(Base):
    __tablename__ = 'legalpad_document'
    __table_args__ = (
        Index('key_creator', 'creatorPHID', 'dateModified'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    title = Column(Unicode(255), nullable=False)
    contributorCount = Column(Integer, nullable=False, server_default=text("'0'"))
    recentContributorPHIDs = Column(Unicode, nullable=False)
    creatorPHID = Column(String, nullable=False)
    versions = Column(Integer, nullable=False, server_default=text("'0'"))
    documentBodyPHID = Column(String, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    mailKey = Column(BINARY(20), nullable=False)
    signatureType = Column(Unicode(4), nullable=False)
    preamble = Column(Unicode, nullable=False)


class LegalpadDocumentBody(Base):
    __tablename__ = 'legalpad_documentbody'
    __table_args__ = (
        Index('key_document', 'documentPHID', 'version', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    creatorPHID = Column(String, nullable=False)
    documentPHID = Column(String, nullable=False)
    version = Column(Integer, nullable=False, server_default=text("'0'"))
    title = Column(Unicode(255), nullable=False)
    text = Column(Unicode)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class LegalpadDocumentSignature(Base):
    __tablename__ = 'legalpad_documentsignature'
    __table_args__ = (
        Index('key_signer', 'signerPHID', 'dateModified'),
        Index('key_document', 'documentPHID', 'signerPHID', 'documentVersion')
    )

    id = Column(Integer, primary_key=True)
    documentPHID = Column(String, nullable=False)
    documentVersion = Column(Integer, nullable=False, server_default=text("'0'"))
    signatureType = Column(Unicode(4), nullable=False)
    signerPHID = Column(String)
    signerName = Column(Unicode(255), nullable=False)
    signerEmail = Column(Unicode(255), nullable=False)
    signatureData = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    secretKey = Column(BINARY(20), nullable=False, index=True)
    verified = Column(Integer, server_default=text("'0'"))
    isExemption = Column(Integer, nullable=False, server_default=text("'0'"))
    exemptionPHID = Column(String)


class LegalpadTransaction(Base):
    __tablename__ = 'legalpad_transaction'

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


class LegalpadTransactionComment(Base):
    __tablename__ = 'legalpad_transaction_comment'
    __table_args__ = (
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True),
        Index('key_draft', 'authorPHID', 'documentID', 'transactionPHID', unique=True)
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    transactionPHID = Column(String)
    authorPHID = Column(String, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentVersion = Column(Integer, nullable=False)
    content = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    isDeleted = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    documentID = Column(Integer)
    lineNumber = Column(Integer, nullable=False)
    lineLength = Column(Integer, nullable=False)
    fixedState = Column(Unicode(12))
    hasReplies = Column(Integer, nullable=False)
    replyToCommentPHID = Column(String)
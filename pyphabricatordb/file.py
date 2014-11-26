# coding: utf-8
from sqlalchemy import BINARY, BigInteger, Column, Index, Integer, String, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.dialects.mysql.base import LONGBLOB
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


class EdgeDatum(Base):
    __tablename__ = 'edgedata'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode, nullable=False)


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255))
    mimeType = Column(Unicode(255))
    byteSize = Column(BigInteger, nullable=False)
    storageEngine = Column(Unicode(32), nullable=False)
    storageFormat = Column(Unicode(32), nullable=False)
    storageHandle = Column(Unicode(255), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)
    authorPHID = Column(String, index=True)
    secretKey = Column(BINARY(20))
    contentHash = Column(BINARY(40), index=True)
    usermetadata = Column('metadata', Unicode, nullable=False)
    ttl = Column(Integer, index=True)
    isExplicitUpload = Column(Integer, server_default=text("'1'"))
    mailKey = Column(BINARY(20), nullable=False)
    viewPolicy = Column(String, nullable=False)


class FileImageMacro(Base):
    __tablename__ = 'file_imagemacro'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String)
    filePHID = Column(String, nullable=False)
    name = Column(Unicode(128), nullable=False, unique=True)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)
    isDisabled = Column(Integer, nullable=False, index=True)
    audioPHID = Column(String)
    audioBehavior = Column(Unicode(64), nullable=False)
    mailKey = Column(BINARY(20), nullable=False)


class FileStorageBlob(Base):
    __tablename__ = 'file_storageblob'

    id = Column(Integer, primary_key=True)
    data = Column(LONGBLOB, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class FileTransaction(Base):
    __tablename__ = 'file_transaction'

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


class FileTransactionComment(Base):
    __tablename__ = 'file_transaction_comment'
    __table_args__ = (
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True),
        Index('key_draft', 'authorPHID', 'transactionPHID', unique=True)
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


class FileTransformedFile(Base):
    __tablename__ = 'file_transformedfile'
    __table_args__ = (
        Index('originalPHID', 'originalPHID', 'transform', unique=True),
    )

    id = Column(Integer, primary_key=True)
    originalPHID = Column(String, nullable=False)
    transform = Column(Unicode(128), nullable=False)
    transformedPHID = Column(String, nullable=False, index=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class MacroTransaction(Base):
    __tablename__ = 'macro_transaction'

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
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)


class MacroTransactionComment(Base):
    __tablename__ = 'macro_transaction_comment'
    __table_args__ = (
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True),
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
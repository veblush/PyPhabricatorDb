# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class ReleephBranch(Base):
    __tablename__ = 'releeph_branch'
    __table_args__ = (
        Index('releephProjectID', 'releephProjectID', 'symbolicName', unique=True),
        Index('releephProjectID_2', 'releephProjectID', 'basename', unique=True),
        Index('releephProjectID_name', 'releephProjectID', 'name', unique=True)
    )

    id = Column(Integer, primary_key=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    basename = Column(Unicode(64), nullable=False)
    releephProjectID = Column(Integer, nullable=False)
    createdByUserPHID = Column(String, nullable=False)
    cutPointCommitPHID = Column(String, nullable=False)
    isActive = Column(Integer, nullable=False, server_default=text("'1'"))
    symbolicName = Column(Unicode(64))
    details = Column(Unicode, nullable=False)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(128), nullable=False)


class ReleephBranchTransaction(Base):
    __tablename__ = 'releeph_branchtransaction'

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


class ReleephProductTransaction(Base):
    __tablename__ = 'releeph_producttransaction'

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


class ReleephProject(Base):
    __tablename__ = 'releeph_project'

    id = Column(Integer, primary_key=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(128), nullable=False, unique=True)
    trunkBranch = Column(Unicode(255), nullable=False)
    repositoryPHID = Column(String, nullable=False)
    createdByUserPHID = Column(String, nullable=False)
    isActive = Column(Integer, nullable=False, server_default=text("'1'"))
    details = Column(Unicode, nullable=False)


class ReleephRequest(Base):
    __tablename__ = 'releeph_request'
    __table_args__ = (
        Index('requestIdentifierBranch', 'requestCommitPHID', 'branchID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    phid = Column(String, nullable=False, unique=True)
    branchID = Column(Integer, nullable=False, index=True)
    requestUserPHID = Column(String, nullable=False)
    requestCommitPHID = Column(String)
    commitIdentifier = Column(Unicode(40))
    commitPHID = Column(String)
    pickStatus = Column(Integer)
    details = Column(Unicode, nullable=False)
    userIntents = Column(Unicode)
    inBranch = Column(Integer, nullable=False, server_default=text("'0'"))
    mailKey = Column(BINARY(20), nullable=False)
    requestedObjectPHID = Column(String, nullable=False, index=True)


class ReleephRequestTransaction(Base):
    __tablename__ = 'releeph_requesttransaction'

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


class ReleephRequestTransactionComment(Base):
    __tablename__ = 'releeph_requesttransaction_comment'
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
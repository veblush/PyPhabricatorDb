# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class OwnersOwner(Base):
    __tablename__ = 'owners_owner'
    __table_args__ = (
        Index('packageID', 'packageID', 'userPHID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    packageID = Column(Integer, nullable=False)
    userPHID = Column(String, nullable=False, index=True)


class OwnersPackage(Base):
    __tablename__ = 'owners_package'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(128), nullable=False, unique=True)
    originalName = Column(Unicode(255), nullable=False)
    description = Column(Unicode, nullable=False)
    primaryOwnerPHID = Column(String)
    auditingEnabled = Column(Integer, nullable=False, server_default=text("'0'"))
    mailKey = Column(BINARY(20), nullable=False)


class OwnersPackageTransaction(Base):
    __tablename__ = 'owners_packagetransaction'

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


class OwnersPath(Base):
    __tablename__ = 'owners_path'

    id = Column(Integer, primary_key=True)
    packageID = Column(Integer, nullable=False, index=True)
    repositoryPHID = Column(String, nullable=False)
    path = Column(Unicode(255), nullable=False)
    excluded = Column(Integer, nullable=False, server_default=text("'0'"))
# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY, text
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


class OwnersPath(Base):
    __tablename__ = 'owners_path'

    id = Column(Integer, primary_key=True)
    packageID = Column(Integer, nullable=False, index=True)
    repositoryPHID = Column(String, nullable=False)
    path = Column(Unicode(255), nullable=False)
    excluded = Column(Integer, nullable=False, server_default=text("'0'"))
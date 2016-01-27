# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class DoorkeeperExternalObject(Base):
    __tablename__ = 'doorkeeper_externalobject'
    __table_args__ = (
        Index('key_full', 'applicationType', 'applicationDomain', 'objectType', 'objectID'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    objectKey = Column(BINARY(12), nullable=False, unique=True)
    applicationType = Column(Unicode(32), nullable=False)
    applicationDomain = Column(Unicode(32), nullable=False)
    objectType = Column(Unicode(32), nullable=False)
    objectID = Column(Unicode(64), nullable=False)
    objectURI = Column(Unicode(128))
    importerPHID = Column(String)
    properties = Column(Unicode, nullable=False)
    viewPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class Edge(Base):
    __tablename__ = 'edge'
    __table_args__ = (
        Index('key_dst', 'dst', 'type', 'src', unique=True),
        Index('src', 'src', 'type', 'dateCreated', 'seq')
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
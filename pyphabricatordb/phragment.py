# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


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


class EdgeDatum(Base):
    __tablename__ = 'edgedata'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode, nullable=False)


class PhragmentFragment(Base):
    __tablename__ = 'phragment_fragment'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    path = Column(Unicode(128), nullable=False, unique=True)
    depth = Column(Integer, nullable=False)
    latestVersionPHID = Column(String)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class PhragmentFragmentVersion(Base):
    __tablename__ = 'phragment_fragmentversion'
    __table_args__ = (
        Index('key_version', 'fragmentPHID', 'sequence', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    sequence = Column(Integer, nullable=False)
    fragmentPHID = Column(String, nullable=False)
    filePHID = Column(String)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class PhragmentSnapshot(Base):
    __tablename__ = 'phragment_snapshot'
    __table_args__ = (
        Index('key_name', 'primaryFragmentPHID', 'name', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    primaryFragmentPHID = Column(String, nullable=False)
    name = Column(Unicode(128), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class PhragmentSnapshotChild(Base):
    __tablename__ = 'phragment_snapshotchild'
    __table_args__ = (
        Index('key_child', 'snapshotPHID', 'fragmentPHID', 'fragmentVersionPHID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    snapshotPHID = Column(String, nullable=False)
    fragmentPHID = Column(String, nullable=False)
    fragmentVersionPHID = Column(String)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
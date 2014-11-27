# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY, text
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


class PhameBLog(Base):
    __tablename__ = 'phame_blog'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(64), nullable=False)
    description = Column(Unicode, nullable=False)
    domain = Column(Unicode(128), unique=True)
    configData = Column(Unicode, nullable=False)
    creatorPHID = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    viewPolicy = Column(String)
    editPolicy = Column(String)
    joinPolicy = Column(String)


class PhamePost(Base):
    __tablename__ = 'phame_post'
    __table_args__ = (
        Index('bloggerPosts', 'bloggerPHID', 'visibility', 'datePublished', 'id'),
        Index('phameTitle', 'bloggerPHID', 'phameTitle', unique=True)
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    bloggerPHID = Column(String, nullable=False)
    title = Column(Unicode(255), nullable=False)
    phameTitle = Column(Unicode(64), nullable=False)
    body = Column(Unicode)
    visibility = Column(Integer, nullable=False, server_default=text("'0'"))
    configData = Column(Unicode)
    datePublished = Column(dbdatetime, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    blogPHID = Column(String)
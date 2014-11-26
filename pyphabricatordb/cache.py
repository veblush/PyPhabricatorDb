# coding: utf-8
from sqlalchemy import BINARY, BigInteger, Column, Integer, String
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.dialects.mysql.base import LONGBLOB
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class CacheGeneral(Base):
    __tablename__ = 'cache_general'

    id = Column(BigInteger, primary_key=True)
    cacheKeyHash = Column(BINARY(12), nullable=False, unique=True)
    cacheKey = Column(Unicode(128), nullable=False)
    cacheFormat = Column(Unicode(16), nullable=False)
    cacheData = Column(LONGBLOB, nullable=False)
    cacheCreated = Column(Integer, nullable=False, index=True)
    cacheExpires = Column(Integer, index=True)


class CacheMarkupCache(Base):
    __tablename__ = 'cache_markupcache'

    id = Column(Integer, primary_key=True)
    cacheKey = Column(Unicode(128), nullable=False, unique=True)
    cacheData = Column(LONGBLOB, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)
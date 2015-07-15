# coding: utf-8
from sqlalchemy import BigInteger, Column, Index, Integer, String, Table, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class FeedStoryData(Base):
    __tablename__ = 'feed_storydata'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    chronologicalKey = Column(BigInteger, nullable=False, unique=True)
    storyType = Column(Unicode(64), nullable=False)
    storyData = Column(Unicode, nullable=False)
    authorPHID = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


t_feed_storynotification = Table(
    'feed_storynotification', metadata,
    Column('userPHID', String, nullable=False),
    Column('primaryObjectPHID', String, nullable=False, index=True),
    Column('chronologicalKey', BigInteger, nullable=False, index=True),
    Column('hasViewed', Integer, nullable=False),
    Index('userPHID_2', 'userPHID', 'hasViewed', 'primaryObjectPHID'),
    Index('userPHID', 'userPHID', 'chronologicalKey', unique=True)
)


t_feed_storyreference = Table(
    'feed_storyreference', metadata,
    Column('objectPHID', String, nullable=False),
    Column('chronologicalKey', BigInteger, nullable=False, index=True),
    Index('objectPHID', 'objectPHID', 'chronologicalKey', unique=True)
)
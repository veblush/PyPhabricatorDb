# coding: utf-8
from sqlalchemy import BINARY, Column, Float, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class SystemActionLog(Base):
    __tablename__ = 'system_actionlog'
    __table_args__ = (
        Index('key_action', 'actorHash', 'action', 'epoch'),
    )

    id = Column(Integer, primary_key=True)
    actorHash = Column(BINARY(12), nullable=False)
    actorIdentity = Column(Unicode(255), nullable=False)
    action = Column(Unicode(32), nullable=False)
    score = Column(Float(asdecimal=True), nullable=False)
    epoch = Column(Integer, nullable=False, index=True)


class SystemDestructionLog(Base):
    __tablename__ = 'system_destructionlog'

    id = Column(Integer, primary_key=True)
    objectClass = Column(Unicode(128), nullable=False)
    rootLogID = Column(Integer)
    objectPHID = Column(String)
    objectMonogram = Column(Unicode(64))
    epoch = Column(Integer, nullable=False, index=True)
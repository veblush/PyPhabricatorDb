# coding: utf-8
from sqlalchemy import BigInteger, Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class ConduitCertificateToken(Base):
    __tablename__ = 'conduit_certificatetoken'

    id = Column(Integer, primary_key=True)
    userPHID = Column(String, nullable=False, unique=True)
    token = Column(Unicode(64), unique=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class ConduitConnectionLog(Base):
    __tablename__ = 'conduit_connectionlog'

    id = Column(Integer, primary_key=True)
    client = Column(Unicode(255))
    clientVersion = Column(Unicode(255))
    clientDescription = Column(Unicode(255))
    username = Column(Unicode(255))
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)


class ConduitMethodCallLog(Base):
    __tablename__ = 'conduit_methodcalllog'
    __table_args__ = (
        Index('key_callermethod', 'callerPHID', 'method'),
    )

    id = Column(BigInteger, primary_key=True)
    connectionID = Column(BigInteger)
    method = Column(Unicode(64), nullable=False, index=True)
    error = Column(Unicode(255), nullable=False)
    duration = Column(BigInteger, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)
    callerPHID = Column(String)
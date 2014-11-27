# coding: utf-8
from sqlalchemy import Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class OAuthServerOAuthClientAuthorization(Base):
    __tablename__ = 'oauth_server_oauthclientauthorization'
    __table_args__ = (
        Index('userPHID', 'userPHID', 'clientPHID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    userPHID = Column(String, nullable=False)
    clientPHID = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    scope = Column(Unicode, nullable=False)


class OAuthServerOAuthServerAccessToken(Base):
    __tablename__ = 'oauth_server_oauthserveraccesstoken'

    id = Column(Integer, primary_key=True)
    token = Column(Unicode(32), nullable=False, unique=True)
    userPHID = Column(String, nullable=False)
    clientPHID = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class OAuthServerOAuthServerAuthorizationcode(Base):
    __tablename__ = 'oauth_server_oauthserverauthorizationcode'

    id = Column(Integer, primary_key=True)
    code = Column(Unicode(32), nullable=False, unique=True)
    clientPHID = Column(String, nullable=False)
    clientSecret = Column(Unicode(32), nullable=False)
    userPHID = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    redirectURI = Column(Unicode(255), nullable=False)


class OAuthServerOAuthServerClient(Base):
    __tablename__ = 'oauth_server_oauthserverclient'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)
    secret = Column(Unicode(32), nullable=False)
    redirectURI = Column(Unicode(255), nullable=False)
    creatorPHID = Column(String, nullable=False, index=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
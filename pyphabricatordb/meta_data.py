# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class PatchStatus(Base):
    __tablename__ = 'patch_status'

    patch = Column(Unicode(128), primary_key=True)
    applied = Column(Integer, nullable=False)
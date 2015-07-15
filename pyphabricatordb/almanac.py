# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AlmanacBinding(Base):
    __tablename__ = 'almanac_binding'
    __table_args__ = (
        Index('key_service', 'servicePHID', 'interfacePHID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    servicePHID = Column(String, nullable=False)
    devicePHID = Column(String, nullable=False, index=True)
    interfacePHID = Column(String, nullable=False, index=True)
    mailKey = Column(BINARY(20), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class AlmanacBindingTransaction(Base):
    __tablename__ = 'almanac_bindingtransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class AlmanacDevice(Base):
    __tablename__ = 'almanac_device'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(128), nullable=False, index=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    nameIndex = Column(BINARY(12), nullable=False, unique=True)
    mailKey = Column(BINARY(20), nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    isLocked = Column(Integer, nullable=False)


class AlmanacDeviceTransaction(Base):
    __tablename__ = 'almanac_devicetransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class AlmanacInterface(Base):
    __tablename__ = 'almanac_interface'
    __table_args__ = (
        Index('key_location', 'networkPHID', 'address', 'port'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    devicePHID = Column(String, nullable=False, index=True)
    networkPHID = Column(String, nullable=False)
    address = Column(Unicode(64), nullable=False)
    port = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class AlmanacNetwork(Base):
    __tablename__ = 'almanac_network'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(128), nullable=False)
    mailKey = Column(BINARY(20), nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class AlmanacNetworkTransaction(Base):
    __tablename__ = 'almanac_networktransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class AlmanacProperty(Base):
    __tablename__ = 'almanac_property'
    __table_args__ = (
        Index('objectPHID', 'objectPHID', 'fieldIndex', unique=True),
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    fieldIndex = Column(BINARY(12), nullable=False)
    fieldName = Column(Unicode(128), nullable=False)
    fieldValue = Column(Unicode, nullable=False)


class AlmanacService(Base):
    __tablename__ = 'almanac_service'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(128), nullable=False, index=True)
    nameIndex = Column(BINARY(12), nullable=False, unique=True)
    mailKey = Column(BINARY(20), nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    serviceClass = Column(Unicode(64), nullable=False, index=True)
    isLocked = Column(Integer, nullable=False)


class AlmanacServiceTransaction(Base):
    __tablename__ = 'almanac_servicetransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


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
# coding: utf-8
from sqlalchemy import BINARY, BigInteger, Column, Index, Integer, String, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.dialects.mysql.base import LONGBLOB
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


class HarbormasterBuild(Base):
    __tablename__ = 'harbormaster_build'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    buildablePHID = Column(String, nullable=False, index=True)
    buildPlanPHID = Column(String, nullable=False, index=True)
    buildStatus = Column(Unicode(32), nullable=False, index=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    buildGeneration = Column(Integer, nullable=False, server_default=text("'0'"))


class HarbormasterBuildable(Base):
    __tablename__ = 'harbormaster_buildable'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    buildablePHID = Column(String, nullable=False, index=True)
    containerPHID = Column(String, index=True)
    buildableStatus = Column(Unicode(32), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    isManualBuildable = Column(Integer, nullable=False, index=True)


class HarbormasterBuildableTransaction(Base):
    __tablename__ = 'harbormaster_buildabletransaction'

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


class HarbormasterBuildArtifact(Base):
    __tablename__ = 'harbormaster_buildartifact'
    __table_args__ = (
        Index('key_garbagecollect', 'artifactType', 'dateCreated'),
        Index('key_artifact', 'artifactType', 'artifactIndex', unique=True)
    )

    id = Column(Integer, primary_key=True)
    artifactType = Column(Unicode(32), nullable=False)
    artifactIndex = Column(BINARY(12), nullable=False)
    artifactKey = Column(Unicode(255), nullable=False)
    artifactData = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    buildTargetPHID = Column(String, nullable=False)


class HarbormasterBuildCommand(Base):
    __tablename__ = 'harbormaster_buildcommand'

    id = Column(Integer, primary_key=True)
    authorPHID = Column(String, nullable=False)
    targetPHID = Column(String, nullable=False, index=True)
    command = Column(Unicode(128), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class HarbormasterBuildLog(Base):
    __tablename__ = 'harbormaster_buildlog'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    logSource = Column(Unicode(255))
    logType = Column(Unicode(255))
    duration = Column(Integer)
    live = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    buildTargetPHID = Column(String, nullable=False, index=True)


class HarbormasterBuildLogchunk(Base):
    __tablename__ = 'harbormaster_buildlogchunk'

    id = Column(Integer, primary_key=True)
    logID = Column(Integer, nullable=False, index=True)
    encoding = Column(Unicode(32), nullable=False)
    size = Column(Integer)
    chunk = Column(LONGBLOB, nullable=False)


class HarbormasterBuildMessage(Base):
    __tablename__ = 'harbormaster_buildmessage'

    id = Column(Integer, primary_key=True)
    authorPHID = Column(String, nullable=False)
    buildTargetPHID = Column(String, nullable=False, index=True)
    type = Column(Unicode(16), nullable=False)
    isConsumed = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class HarbormasterBuildPlan(Base):
    __tablename__ = 'harbormaster_buildplan'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)
    planStatus = Column(Unicode(32), nullable=False, index=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class HarbormasterBuildPlanTransaction(Base):
    __tablename__ = 'harbormaster_buildplantransaction'

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


class HarbormasterBuildStep(Base):
    __tablename__ = 'harbormaster_buildstep'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    buildPlanPHID = Column(String, nullable=False, index=True)
    className = Column(Unicode(255), nullable=False)
    details = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    sequence = Column(Integer, nullable=False)
    name = Column(Unicode(255))
    description = Column(Unicode, nullable=False)


class HarbormasterBuildStepTransaction(Base):
    __tablename__ = 'harbormaster_buildsteptransaction'

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


class HarbormasterBuildTarget(Base):
    __tablename__ = 'harbormaster_buildtarget'
    __table_args__ = (
        Index('key_build', 'buildPHID', 'buildStepPHID'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    buildPHID = Column(String, nullable=False)
    buildStepPHID = Column(String, nullable=False)
    className = Column(Unicode(255), nullable=False)
    details = Column(Unicode, nullable=False)
    variables = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    targetStatus = Column(Unicode(64), nullable=False)
    name = Column(Unicode(255))
    dateStarted = Column(Integer)
    dateCompleted = Column(Integer)
    buildGeneration = Column(Integer, nullable=False, server_default=text("'0'"))


class HarbormasterBuildTransaction(Base):
    __tablename__ = 'harbormaster_buildtransaction'

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


class HarbormasterObject(Base):
    __tablename__ = 'harbormaster_object'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255))
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class HarbormasterScratchTable(Base):
    __tablename__ = 'harbormaster_scratchtable'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode(64), nullable=False, index=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    bigData = Column(Unicode)


class LiskCounter(Base):
    __tablename__ = 'lisk_counter'

    counterName = Column(Unicode(32), primary_key=True)
    counterValue = Column(BigInteger, nullable=False)
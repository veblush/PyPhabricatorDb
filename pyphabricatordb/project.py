# coding: utf-8
from sqlalchemy import BINARY, BigInteger, Column, Index, Integer, String, VARBINARY, text
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
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


class EdgeData(Base):
    __tablename__ = 'edgedata'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode, nullable=False)


class Project(Base):
    __tablename__ = 'project'
    __table_args__ = (
        Index('key_path', 'projectPath', 'projectDepth'),
        Index('key_milestone', 'parentProjectPHID', 'milestoneNumber', unique=True)
    )

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(128), nullable=False)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    status = Column(Unicode(32), nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    joinPolicy = Column(String, nullable=False)
    isMembershipLocked = Column(Integer, nullable=False, server_default=text("'0'"))
    profileImagePHID = Column(String)
    icon = Column(Unicode(32), nullable=False, index=True)
    color = Column(Unicode(32), nullable=False, index=True)
    mailKey = Column(BINARY(20), nullable=False)
    primarySlug = Column(Unicode(128), unique=True)
    parentProjectPHID = Column(String)
    hasWorkboard = Column(Integer, nullable=False)
    hasMilestones = Column(Integer, nullable=False)
    hasSubprojects = Column(Integer, nullable=False)
    milestoneNumber = Column(Integer)
    projectPath = Column(String, nullable=False)
    projectDepth = Column(Integer, nullable=False)
    projectPathKey = Column(BINARY(4), nullable=False, unique=True)

    columns = relationship('ProjectColumn', backref='project')


class ProjectColumn(Base):
    __tablename__ = 'project_column'
    __table_args__ = (
        Index('key_status', 'projectPHID', 'status', 'sequence'),
        Index('key_sequence', 'projectPHID', 'sequence')
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)
    status = Column(Integer, nullable=False)
    sequence = Column(Integer, nullable=False)
    projectPHID = Column(String, ForeignKey("project.phid"), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    properties = Column(Unicode, nullable=False)

    positions = relationship('ProjectColumnPosition', backref='column')


class ProjectColumnPosition(Base):
    __tablename__ = 'project_columnposition'
    __table_args__ = (
        Index('objectPHID', 'objectPHID', 'boardPHID'),
        Index('boardPHID_2', 'boardPHID', 'columnPHID', 'sequence'),
        Index('boardPHID', 'boardPHID', 'columnPHID', 'objectPHID', unique=True)
    )

    id = Column(Integer, primary_key=True)
    boardPHID = Column(String, nullable=False)
    columnPHID = Column(String, ForeignKey("project_column.phid"), nullable=False)
    objectPHID = Column(String, nullable=False)
    sequence = Column(Integer, nullable=False)


class ProjectColumnTransaction(Base):
    __tablename__ = 'project_columntransaction'

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


class ProjectCustomFieldNumericIndex(Base):
    __tablename__ = 'project_customfieldnumericindex'
    __table_args__ = (
        Index('key_join', 'objectPHID', 'indexKey', 'indexValue'),
        Index('key_find', 'indexKey', 'indexValue')
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    indexKey = Column(BINARY(12), nullable=False)
    indexValue = Column(BigInteger, nullable=False)


class ProjectCustomFieldStorage(Base):
    __tablename__ = 'project_customfieldstorage'
    __table_args__ = (
        Index('objectPHID', 'objectPHID', 'fieldIndex', unique=True),
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    fieldIndex = Column(BINARY(12), nullable=False)
    fieldValue = Column(Unicode, nullable=False)


class ProjectCustomFieldstringIndex(Base):
    __tablename__ = 'project_customfieldstringindex'
    __table_args__ = (
        Index('key_find', 'indexKey', 'indexValue'),
        Index('key_join', 'objectPHID', 'indexKey', 'indexValue')
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    indexKey = Column(BINARY(12), nullable=False)
    indexValue = Column(Unicode, nullable=False)


class ProjectDataSourceToken(Base):
    __tablename__ = 'project_datasourcetoken'
    __table_args__ = (
        Index('token', 'token', 'projectID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    projectID = Column(Integer, nullable=False, index=True)
    token = Column(Unicode(128), nullable=False)


class ProjectSlug(Base):
    __tablename__ = 'project_slug'

    id = Column(Integer, primary_key=True)
    projectPHID = Column(String, nullable=False, index=True)
    slug = Column(Unicode(128), nullable=False, unique=True)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class ProjectTransaction(Base):
    __tablename__ = 'project_transaction'

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
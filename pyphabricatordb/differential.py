# coding: utf-8
from sqlalchemy import BINARY, BigInteger, Column, Index, Integer, String, Table, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.dialects.mysql.base import LONGBLOB
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


t_differential_affectedpath = Table(
    'differential_affectedpath', metadata,
    Column('repositoryID', Integer, nullable=False),
    Column('pathID', Integer, nullable=False),
    Column('epoch', Integer, nullable=False),
    Column('revisionID', Integer, nullable=False, index=True),
    Index('repositoryID', 'repositoryID', 'pathID', 'epoch')
)


class DifferentialChangeset(Base):
    __tablename__ = 'differential_changeset'

    id = Column(Integer, primary_key=True)
    diffID = Column(Integer, nullable=False, index=True)
    oldFile = Column(Unicode(255))
    filename = Column(Unicode(255), nullable=False)
    awayPaths = Column(Unicode)
    changeType = Column(Integer, nullable=False)
    fileType = Column(Integer, nullable=False)
    usermetadata = Column('metadata', Unicode)
    oldProperties = Column(Unicode)
    newProperties = Column(Unicode)
    addLines = Column(Integer, nullable=False)
    delLines = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class DifferentialChangesetParseCache(Base):
    __tablename__ = 'differential_changeset_parse_cache'

    id = Column(Integer, primary_key=True)
    cache = Column(LONGBLOB, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False, index=True)


class DifferentialCommit(Base):
    __tablename__ = 'differential_commit'

    revisionID = Column(Integer, primary_key=True, nullable=False)
    commitPHID = Column(String, primary_key=True, nullable=False, unique=True)


class DifferentialCustomFieldNumericIndex(Base):
    __tablename__ = 'differential_customfieldnumericindex'
    __table_args__ = (
        Index('key_find', 'indexKey', 'indexValue'),
        Index('key_join', 'objectPHID', 'indexKey', 'indexValue')
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    indexKey = Column(BINARY(12), nullable=False)
    indexValue = Column(BigInteger, nullable=False)


class DifferentialCustomFieldStorage(Base):
    __tablename__ = 'differential_customfieldstorage'
    __table_args__ = (
        Index('objectPHID', 'objectPHID', 'fieldIndex', unique=True),
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    fieldIndex = Column(BINARY(12), nullable=False)
    fieldValue = Column(Unicode, nullable=False)


class DifferentialCustomFieldStringIndex(Base):
    __tablename__ = 'differential_customfieldstringindex'
    __table_args__ = (
        Index('key_join', 'objectPHID', 'indexKey', 'indexValue'),
        Index('key_find', 'indexKey', 'indexValue')
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    indexKey = Column(BINARY(12), nullable=False)
    indexValue = Column(Unicode, nullable=False)


class DifferentialDiff(Base):
    __tablename__ = 'differential_diff'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    revisionID = Column(Integer, index=True)
    authorPHID = Column(String)
    repositoryPHID = Column(String)
    sourceMachine = Column(Unicode(255))
    sourcePath = Column(Unicode(255))
    sourceControlSystem = Column(Unicode(64))
    sourceControlBaseRevision = Column(Unicode(255))
    sourceControlPath = Column(Unicode(255))
    lintStatus = Column(Integer, nullable=False)
    unitStatus = Column(Integer, nullable=False)
    lineCount = Column(Integer, nullable=False)
    branch = Column(Unicode(255))
    bookmark = Column(Unicode(255))
    creationMethod = Column(Unicode(255))
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    description = Column(Unicode(255))
    repositoryUUID = Column(Unicode(64))
    viewPolicy = Column(String, nullable=False)


class DifferentialDiffProperty(Base):
    __tablename__ = 'differential_diffproperty'
    __table_args__ = (
        Index('diffID', 'diffID', 'name', unique=True),
    )

    id = Column(Integer, primary_key=True)
    diffID = Column(Integer, nullable=False)
    name = Column(Unicode(128), nullable=False)
    data = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class DifferentialDifftransaction(Base):
    __tablename__ = 'differential_difftransaction'

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


class DifferentialDraft(Base):
    __tablename__ = 'differential_draft'
    __table_args__ = (
        Index('key_unique', 'objectPHID', 'authorPHID', 'draftKey', unique=True),
    )

    id = Column(Integer, primary_key=True)
    objectPHID = Column(String, nullable=False)
    authorPHID = Column(String, nullable=False)
    draftKey = Column(Unicode(64), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class DifferentialHiddenComment(Base):
    __tablename__ = 'differential_hiddencomment'
    __table_args__ = (
        Index('key_user', 'userPHID', 'commentID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    userPHID = Column(String, nullable=False)
    commentID = Column(Integer, nullable=False, index=True)


class DifferentialHunk(Base):
    __tablename__ = 'differential_hunk'

    id = Column(Integer, primary_key=True)
    changesetID = Column(Integer, nullable=False, index=True)
    changes = Column(Unicode)
    oldOffset = Column(Integer, nullable=False)
    oldLen = Column(Integer, nullable=False)
    newOffset = Column(Integer, nullable=False)
    newLen = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class DifferentialHunkModern(Base):
    __tablename__ = 'differential_hunk_modern'

    id = Column(Integer, primary_key=True)
    changesetID = Column(Integer, nullable=False, index=True)
    oldOffset = Column(Integer, nullable=False)
    oldLen = Column(Integer, nullable=False)
    newOffset = Column(Integer, nullable=False)
    newLen = Column(Integer, nullable=False)
    dataType = Column(BINARY(4), nullable=False)
    dataEncoding = Column(Unicode(16))
    dataFormat = Column(BINARY(4), nullable=False)
    data = Column(LONGBLOB, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False, index=True)
    dateModified = Column(dbdatetime, nullable=False)


class DifferentialRevision(Base):
    __tablename__ = 'differential_revision'
    __table_args__ = (
        Index('key_status', 'status', 'phid'),
        Index('authorPHID', 'authorPHID', 'status')
    )

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    originalTitle = Column(Unicode(255), nullable=False)
    phid = Column(String, nullable=False, unique=True)
    status = Column(Unicode(32), nullable=False)
    summary = Column(Unicode, nullable=False)
    testPlan = Column(Unicode, nullable=False)
    authorPHID = Column(String)
    lastReviewerPHID = Column(String)
    lineCount = Column(Integer)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    attached = Column(Unicode, nullable=False)
    mailKey = Column(BINARY(40), nullable=False)
    branchName = Column(Unicode(255))
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    repositoryPHID = Column(String, index=True)


t_differential_revisionhash = Table(
    'differential_revisionhash', metadata,
    Column('revisionID', Integer, nullable=False, index=True),
    Column('type', BINARY(4), nullable=False),
    Column('hash', BINARY(40), nullable=False),
    Index('type', 'type', 'hash')
)


class DifferentialTransaction(Base):
    __tablename__ = 'differential_transaction'

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


class DifferentialTransactionComment(Base):
    __tablename__ = 'differential_transaction_comment'
    __table_args__ = (
        Index('key_draft', 'authorPHID', 'transactionPHID'),
        Index('key_version', 'transactionPHID', 'commentVersion', unique=True)
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    transactionPHID = Column(String)
    authorPHID = Column(String, nullable=False)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentVersion = Column(Integer, nullable=False)
    content = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    isDeleted = Column(Integer, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    revisionPHID = Column(String, index=True)
    changesetID = Column(Integer, index=True)
    isNewFile = Column(Integer, nullable=False)
    lineNumber = Column(Integer, nullable=False)
    lineLength = Column(Integer, nullable=False)
    fixedState = Column(Unicode(12))
    hasReplies = Column(Integer, nullable=False)
    replyToCommentPHID = Column(String)


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
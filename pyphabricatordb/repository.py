# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, Table, VARBINARY
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


class Repository(Base):
    __tablename__ = 'repository'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False, index=True)
    callsign = Column(Unicode(32), nullable=False, unique=True)
    versionControlSystem = Column(Unicode(32), nullable=False, index=True)
    details = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    uuid = Column(Unicode(64))
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    pushPolicy = Column(String, nullable=False)
    credentialPHID = Column(String)
    almanacServicePHID = Column(String)
    spacePHID = Column(String, index=True)
    repositorySlug = Column(Unicode(64), unique=True)


class RepositoryAuditRequest(Base):
    __tablename__ = 'repository_auditrequest'
    __table_args__ = (
        Index('auditorPHID', 'auditorPHID', 'auditStatus'),
        Index('key_unique', 'commitPHID', 'auditorPHID', unique=True)
    )

    id = Column(Integer, primary_key=True)
    auditorPHID = Column(String, nullable=False)
    commitPHID = Column(String, ForeignKey("repository_commit.phid"), nullable=False, index=True)
    auditStatus = Column(Unicode(64), nullable=False)
    auditReasons = Column(Unicode, nullable=False)

    commit = relationship('RepositoryCommit', uselist=False)


class RepositoryBadCommit(Base):
    __tablename__ = 'repository_badcommit'

    fullCommitName = Column(Unicode(64), primary_key=True)
    description = Column(Unicode, nullable=False)


class RepositoryBranch(Base):
    __tablename__ = 'repository_branch'
    __table_args__ = (
        Index('repositoryID', 'repositoryID', 'name', unique=True),
    )

    id = Column(Integer, primary_key=True)
    repositoryID = Column(Integer, nullable=False)
    name = Column(Unicode(128), nullable=False)
    lintCommit = Column(Unicode(40))
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class RepositoryCommit(Base):
    __tablename__ = 'repository_commit'
    __table_args__ = (
        Index('key_commit_identity', 'commitIdentifier', 'repositoryID', unique=True),
        Index('authorPHID', 'authorPHID', 'auditStatus', 'epoch'),
        Index('repositoryID', 'repositoryID', 'importStatus'),
        Index('repositoryID_2', 'repositoryID', 'epoch'),
        Index('key_author', 'authorPHID', 'epoch')
    )

    id = Column(Integer, primary_key=True)
    repositoryID = Column(Integer, nullable=False)
    phid = Column(String, nullable=False, unique=True)
    commitIdentifier = Column(Unicode(40), nullable=False)
    epoch = Column(Integer, nullable=False, index=True)
    mailKey = Column(BINARY(20), nullable=False)
    authorPHID = Column(String)
    auditStatus = Column(Integer, nullable=False)
    summary = Column(Unicode(80), nullable=False)
    importStatus = Column(Integer, nullable=False)


class RepositoryCommitData(Base):
    __tablename__ = 'repository_commitdata'

    id = Column(Integer, primary_key=True)
    commitID = Column(Integer, ForeignKey("repository_commit.id"), nullable=False, unique=True)
    authorName = Column(Unicode, nullable=False)
    commitMessage = Column(Unicode, nullable=False)
    commitDetails = Column(Unicode, nullable=False)

    commit = relationship('RepositoryCommit', backref=backref('data', uselist=False))


class RepositoryCoverage(Base):
    __tablename__ = 'repository_coverage'
    __table_args__ = (
        Index('key_path', 'branchID', 'pathID', 'commitID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    branchID = Column(Integer, nullable=False)
    commitID = Column(Integer, nullable=False)
    pathID = Column(Integer, nullable=False)
    coverage = Column(LONGBLOB, nullable=False)


class RepositoryFileSystem(Base):
    __tablename__ = 'repository_filesystem'
    __table_args__ = (
        Index('repositoryID', 'repositoryID', 'svnCommit'),
    )

    repositoryID = Column(Integer, primary_key=True, nullable=False)
    parentID = Column(Integer, primary_key=True, nullable=False)
    svnCommit = Column(Integer, primary_key=True, nullable=False)
    pathID = Column(Integer, primary_key=True, nullable=False)
    existed = Column(Integer, nullable=False)
    fileType = Column(Integer, nullable=False)


class RepositoryLintMessage(Base):
    __tablename__ = 'repository_lintmessage'
    __table_args__ = (
        Index('branchID', 'branchID', 'path'),
        Index('branchID_2', 'branchID', 'code', 'path')
    )

    id = Column(Integer, primary_key=True)
    branchID = Column(Integer, nullable=False)
    path = Column(Unicode, nullable=False)
    line = Column(Integer, nullable=False)
    authorPHID = Column(String, index=True)
    code = Column(Unicode(32), nullable=False)
    severity = Column(Unicode(16), nullable=False)
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode, nullable=False)


class RepositoryMirror(Base):
    __tablename__ = 'repository_mirror'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    repositoryPHID = Column(String, nullable=False, index=True)
    remoteURI = Column(Unicode(255), nullable=False)
    credentialPHID = Column(String)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class RepositoryParents(Base):
    __tablename__ = 'repository_parents'
    __table_args__ = (
        Index('key_child', 'childCommitID', 'parentCommitID', unique=True),
    )

    id = Column(Integer, primary_key=True)
    childCommitID = Column(Integer, nullable=False)
    parentCommitID = Column(Integer, nullable=False, index=True)


class RepositoryPath(Base):
    __tablename__ = 'repository_path'

    id = Column(Integer, primary_key=True)
    path = Column(Unicode, nullable=False)
    pathHash = Column(BINARY(32), nullable=False, unique=True)


class RepositoryPathChange(Base):
    __tablename__ = 'repository_pathchange'
    __table_args__ = (
        Index('repositoryID', 'repositoryID', 'pathID', 'commitSequence'),
    )

    repositoryID = Column(Integer, nullable=False)
    pathID = Column(Integer, primary_key=True, nullable=False)
    commitID = Column(Integer, primary_key=True, nullable=False)
    targetPathID = Column(Integer)
    targetCommitID = Column(Integer)
    changeType = Column(Integer, nullable=False)
    fileType = Column(Integer, nullable=False)
    isDirect = Column(Integer, nullable=False)
    commitSequence = Column(Integer, nullable=False)


class RepositoryPushEvent(Base):
    __tablename__ = 'repository_pushevent'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    repositoryPHID = Column(String, nullable=False, index=True)
    epoch = Column(Integer, nullable=False)
    pusherPHID = Column(String, nullable=False)
    remoteAddress = Column(Integer)
    remoteProtocol = Column(Unicode(32))
    rejectCode = Column(Integer, nullable=False)
    rejectDetails = Column(Unicode(64))


class RepositoryPushLog(Base):
    __tablename__ = 'repository_pushlog'
    __table_args__ = (
        Index('key_ref', 'repositoryPHID', 'refNew'),
        Index('key_name', 'repositoryPHID', 'refNameHash')
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    epoch = Column(Integer, nullable=False)
    pushEventPHID = Column(String, nullable=False, index=True)
    repositoryPHID = Column(String, nullable=False, index=True)
    pusherPHID = Column(String, nullable=False, index=True)
    refType = Column(Unicode(12), nullable=False)
    refNameHash = Column(BINARY(12))
    refNameRaw = Column(LONGBLOB)
    refNameEncoding = Column(Unicode(16))
    refOld = Column(Unicode(40))
    refNew = Column(Unicode(40), nullable=False)
    mergeBase = Column(Unicode(40))
    changeFlags = Column(Integer, nullable=False)


class RepositoryRefCursor(Base):
    __tablename__ = 'repository_refcursor'
    __table_args__ = (
        Index('key_cursor', 'repositoryPHID', 'refType', 'refNameHash'),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    repositoryPHID = Column(String, nullable=False)
    refType = Column(Unicode(32), nullable=False)
    refNameHash = Column(BINARY(12), nullable=False)
    refNameRaw = Column(LONGBLOB, nullable=False)
    refNameEncoding = Column(Unicode(16))
    commitIdentifier = Column(Unicode(40), nullable=False)
    isClosed = Column(Integer, nullable=False)


class RepositoryStatusMessage(Base):
    __tablename__ = 'repository_statusmessage'
    __table_args__ = (
        Index('repositoryID', 'repositoryID', 'statusType', unique=True),
    )

    id = Column(Integer, primary_key=True)
    repositoryID = Column(Integer, nullable=False)
    statusType = Column(Unicode(32), nullable=False)
    statusCode = Column(Unicode(32), nullable=False)
    parameters = Column(Unicode, nullable=False)
    epoch = Column(Integer, nullable=False)


class RepositorySummary(Base):
    __tablename__ = 'repository_summary'

    repositoryID = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False)
    lastCommitID = Column(Integer, nullable=False)
    epoch = Column(Integer, index=True)


t_repository_symbol = Table(
    'repository_symbol', metadata,
    Column('repositoryPHID', String, nullable=False),
    Column('symbolContext', Unicode(128), nullable=False),
    Column('symbolName', Unicode(128), nullable=False, index=True),
    Column('symbolType', Unicode(12), nullable=False),
    Column('symbolLanguage', Unicode(32), nullable=False),
    Column('pathID', Integer, nullable=False),
    Column('lineNumber', Integer, nullable=False)
)


class RepositoryTransaction(Base):
    __tablename__ = 'repository_transaction'

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
    usermetadata = Column('metadata', Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class RepositoryUriIndex(Base):
    __tablename__ = 'repository_uriindex'

    id = Column(Integer, primary_key=True)
    repositoryPHID = Column(String, nullable=False, index=True)
    repositoryURI = Column(Unicode, nullable=False, index=True)


class RepositoryVCSPassword(Base):
    __tablename__ = 'repository_vcspassword'

    id = Column(Integer, primary_key=True)
    userPHID = Column(String, nullable=False, unique=True)
    passwordHash = Column(Unicode(128), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
import sys
from pyphabricatordb import *
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker

def get_user(session, phid):
    return session.query(user.User).filter(user.User.phid == phid).first()

def dump_active_audits(session):
    for req in session.query(repository.RepositoryAuditRequest).filter(and_(repository.RepositoryAuditRequest.auditStatus != u"accepted",
                                                                            repository.RepositoryAuditRequest.auditStatus != u"audit-not-required")):
        author = get_user(session, req.commit.authorPHID)
        auditor = get_user(session, req.auditorPHID)
        print u"#{0} Author:{1} Auditor:{2} Status={3} Message={4}".format(
            req.commit.commitIdentifier,
            author.realName if author else "",
            auditor.realName if auditor else "",
            req.auditStatus,
            req.commit.data.commitMessage.splitlines()[0])

def dump_past_concerned_audits(session):
    commits = set()
    for a in session.query(audit.AuditTransaction).filter(and_(audit.AuditTransaction.transactionType == u"audit:action",
                                                               audit.AuditTransaction.newValue == u'"concern"')).all():
        commit = session.query(repository.RepositoryCommit).filter(repository.RepositoryCommit.phid == a.objectPHID).one()
        commit.auditor = get_user(session, a.authorPHID)
        if commit.auditStatus == 4:
            commits.add(commit)
        commit.inline_and_comment_count = \
            session.query(audit.AuditTransaction).filter(and_(audit.AuditTransaction.objectPHID == a.objectPHID,
                                                              or_(audit.AuditTransaction.transactionType == u"core:comment",
                                                                  audit.AuditTransaction.transactionType == u"audit:inline"))).count()
    for commit in sorted(commits, key=lambda x: x.id):
        author = get_user(session, commit.authorPHID);
        print u"#{0} Author:{1} Auditor:{2} I_C:{3} Message={4}".format(
            commit.commitIdentifier, 
            get_user(session, commit.authorPHID).realName,
            commit.auditor.realName if commit.auditor else "",
            commit.inline_and_comment_count,
            commit.data.commitMessage.splitlines()[0])

def main():
    db_url = sys.argv[1] if len(sys.argv) >= 2 else 'mysql://localhost'
    connector.connect_all(db_url)
    session = sessionmaker()()
    
    print "***** Active List ******"
    dump_active_audits(session)
    print ""

    print "***** Past-Concerned List ******"
    dump_past_concerned_audits(session)

if __name__ == "__main__":
    main()

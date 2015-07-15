import sys
import codecs
import datetime
from pyphabricatordb import *
from sqlalchemy.orm import sessionmaker

def create_session():
    DBSession = sessionmaker()
    return DBSession()

def get_user(session, phid):
    return session.query(user.User).filter(user.User.phid == phid).first()

def create_task_range_summary(session, file, start_date, end_date):
    tasks = []
    for t in session.query(maniphest.Task).filter(maniphest.Task.dateModified >= start_date).all():
        t.status_last_modified_date = t.dateCreated
        t.last_commit_date = None
        for trx in t.transactions:
            if trx.transactionType == u"status":
                t.status_last_modified_date = max(t.status_last_modified_date, trx.dateModified)
            if trx.transactionType == u"core:edge":
                t.last_commit_date = trx.dateModified if t.last_commit_date is None else max(t.last_commit_date, trx.dateModified)

        if t.status_last_modified_date >= start_date and t.status_last_modified_date < end_date:
            tasks.append(t)

    user_tasks = {}
    for t in tasks:
        owner = get_user(session, t.ownerPHID)
        owner_name = owner.realName if owner else ""
        user_tasks.setdefault(owner_name, [])
        user_tasks[owner_name].append(t)

    for user_name, tasks in user_tasks.iteritems():
        print "[", user_name, "]"
        for t in tasks:
            if t.last_commit_date and t.last_commit_date >= start_date and t.last_commit_date < end_date:
                print "  ", t.id, t.title

def main():
    db_url = sys.argv[1] if len(sys.argv) >= 2 else 'mysql://localhost'
    file = codecs.open(sys.argv[2], "wb", "utf-8") if len(sys.argv) >= 3 else sys.stdout
    connector.connect_all(db_url)
    session = create_session()
    create_task_range_summary(session, file, datetime.datetime(2014, 12, 1), datetime.datetime(2014, 12, 8))

if __name__ == "__main__":
    main()

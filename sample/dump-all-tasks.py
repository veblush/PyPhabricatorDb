import sys
from pyphabricatordb import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def init_db(db_url):
    db_url_format = db_url + "/{0}?charset=utf8&use_unicode=0"
    engine1 = create_engine(db_url_format.format('phabricator_maniphest'), pool_recycle=3600)
    engine2 = create_engine(db_url_format.format('phabricator_user'), pool_recycle=3600)
    engine3 = create_engine(db_url_format.format('phabricator_project'), pool_recycle=3600)
    maniphest.Base.metadata.bind = engine1
    user.Base.metadata.bind = engine2
    project.Base.metadata.bind = engine3

def create_session():
    DBSession = sessionmaker()
    return DBSession()

def get_user(session, phid):
    return session.query(user.User).filter(user.User.phid == phid).first()

def get_project(session, phid):
    return session.query(project.Project).filter(project.Project.phid == phid).first()

def dump_all_tasks(session):
    for task in session.query(maniphest.Task).all():
        print u"T{0}: {1}".format(task.id, task.title)
        print u"  Status: {0}".format(task.status)
        owner = get_user(session, task.ownerPHID)
        if owner:
            print u"  Owner: {0}".format(owner.realName)
        columnPositions = session.query(project.ProjectColumnPosition).filter(project.ProjectColumnPosition.objectPHID == task.phid).all()
        for columnPosition in columnPositions:
            column = session.query(project.ProjectColumn).filter(project.ProjectColumn.phid == columnPosition.columnPHID).first()
            if column:
                proj = get_project(session, column.projectPHID)
                if proj:
                    print u"  Project: {0} ({1})".format(proj.name, column.name)

def main():
    db_url = 'mysql://localhost'
    if len(sys.argv) >= 2:
        db_url = sys.argv[1]
    init_db(db_url)
    session = create_session()
    dump_all_tasks(session)

if __name__ == "__main__":
    main()

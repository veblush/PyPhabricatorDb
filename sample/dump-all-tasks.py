import sys
from pyphabricatordb import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def get_user(session, phid):
    return session.query(user.User).filter(user.User.phid == phid).first()

def get_project(session, phid):
    return session.query(project.Project).filter(project.Project.phid == phid).first()

def dump_all_tasks(session):
    for task in session.query(maniphest.Task).all():
        print u"T{0} {1}".format(task.id, task.title)
        print u"- status: {0}".format(task.status)
        owner = get_user(session, task.ownerPHID)
        if owner:
            print u"- owner: {0}".format(owner.realName)
        columnPositions = session.query(project.ProjectColumnPosition).filter(project.ProjectColumnPosition.objectPHID == task.phid).all()
        for columnPosition in columnPositions:
            column = columnPosition.column
            if column:
                proj = get_project(session, column.projectPHID)
                if proj:
                    print u"- project: {0}; {1}".format(proj.name, column.name)

def main():
    db_url = sys.argv[1] if len(sys.argv) >= 2 else 'mysql://localhost'
    connector.connect_all(db_url)
    session = sessionmaker()()
    dump_all_tasks(session)

if __name__ == "__main__":
    main()

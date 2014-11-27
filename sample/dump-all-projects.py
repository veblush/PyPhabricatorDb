import sys
from pyphabricatordb import *
from sqlalchemy.orm import sessionmaker

def dump_all_projects(session):
    for p in session.query(project.Project).all():
        print u"#{0} {1}".format(p.id, p.name)
        for c in sorted(p.columns, key=lambda x: x.id):
            print u"- #{0} {1} status={2}".format(c.id, c.name, c.status)

def main():
    db_url = sys.argv[1] if len(sys.argv) >= 2 else 'mysql://localhost'
    connector.connect_all(db_url)
    session = sessionmaker()()
    dump_all_projects(session)

if __name__ == "__main__":
    main()

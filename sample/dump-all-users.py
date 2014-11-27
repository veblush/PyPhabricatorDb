import sys
from pyphabricatordb import *
from sqlalchemy.orm import sessionmaker

def dump_all_users(session):
    for u in session.query(user.User).all():
        print u"#{0} {1} RealName={2} Created={3}".format(u.id, u.userName, u.realName, u.dateCreated)

def main():
    db_url = sys.argv[1] if len(sys.argv) >= 2 else 'mysql://localhost'
    connector.connect_all(db_url)
    session = sessionmaker()()
    dump_all_users(session)

if __name__ == "__main__":
    main()

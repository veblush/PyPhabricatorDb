import sys
import codecs
import json
from pyphabricatordb import *
from sqlalchemy.orm import sessionmaker

def main():
    db_url = sys.argv[1] if len(sys.argv) >= 2 else 'mysql://localhost'
    panel_name = unicode(sys.argv[2]) if len(sys.argv) >= 3 else u'Test Panel'
    panel_text = codecs.open(sys.argv[3], "rb", "utf-8").read() if len(sys.argv) >= 4 else u'Test Text'

    connector.connect_all(db_url)
    session = sessionmaker()()
    panel = session.query(dashboard.DashboardPanel).filter(dashboard.DashboardPanel.name == panel_name).first()
    if panel is None:
        print u"Cannot find {0} panel.".format(panel_name)
        return
    if panel.panelType != "text":
        print u"Panel {0} is {1} type. It should be text.".format(panel_name, panel.panelType)
        return

    panel_prop = json.dumps({u"text": panel_text})
    panel.properties = panel_prop
    session.commit()

if __name__ == "__main__":
    main()

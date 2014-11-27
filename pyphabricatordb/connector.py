from sqlalchemy import create_engine
from . import almanac
from . import audit
from . import auth
from . import cache
from . import calendar
from . import chatlog
from . import conduit
from . import config
from . import conpherence
from . import countdown
from . import daemon
from . import dashboard
from . import differential
from . import diviner
from . import doorkeeper
from . import draft
from . import drydock
from . import fact
from . import feed
from . import file
from . import flag
from . import fund
from . import harbormaster
from . import herald
from . import legalpad
from . import maniphest
from . import metamta
from . import meta_data
from . import nuance
from . import oauth_server
from . import owners
from . import passphrase
from . import pastebin
from . import phame
from . import phlux
from . import pholio
from . import phortune
from . import phragment
from . import phrequent
from . import phriction
from . import policy
from . import ponder
from . import project
from . import releeph
from . import repository
from . import search
from . import slowvote
from . import system
from . import token
from . import user
from . import worker
from . import xhpastview
from . import xhprof

db_tables = {
    'almanac': almanac.Base.metadata,
    'audit': audit.Base.metadata,
    'auth': auth.Base.metadata,
    'cache': cache.Base.metadata,
    'calendar': calendar.Base.metadata,
    'chatlog': chatlog.Base.metadata,
    'conduit': conduit.Base.metadata,
    'config': config.Base.metadata,
    'conpherence': conpherence.Base.metadata,
    'countdown': countdown.Base.metadata,
    'daemon': daemon.Base.metadata,
    'dashboard': dashboard.Base.metadata,
    'differential': differential.Base.metadata,
    'diviner': diviner.Base.metadata,
    'doorkeeper': doorkeeper.Base.metadata,
    'draft': draft.Base.metadata,
    'drydock': drydock.Base.metadata,
    'fact': fact.Base.metadata,
    'feed': feed.Base.metadata,
    'file': file.Base.metadata,
    'flag': flag.Base.metadata,
    'fund': fund.Base.metadata,
    'harbormaster': harbormaster.Base.metadata,
    'herald': herald.Base.metadata,
    'legalpad': legalpad.Base.metadata,
    'maniphest': maniphest.Base.metadata,
    'metamta': metamta.Base.metadata,
    'meta_data': meta_data.Base.metadata,
    'nuance': nuance.Base.metadata,
    'oauth_server': oauth_server.Base.metadata,
    'owners': owners.Base.metadata,
    'passphrase': passphrase.Base.metadata,
    'pastebin': pastebin.Base.metadata,
    'phame': phame.Base.metadata,
    'phlux': phlux.Base.metadata,
    'pholio': pholio.Base.metadata,
    'phortune': phortune.Base.metadata,
    'phragment': phragment.Base.metadata,
    'phrequent': phrequent.Base.metadata,
    'phriction': phriction.Base.metadata,
    'policy': policy.Base.metadata,
    'ponder': ponder.Base.metadata,
    'project': project.Base.metadata,
    'releeph': releeph.Base.metadata,
    'repository': repository.Base.metadata,
    'search': search.Base.metadata,
    'slowvote': slowvote.Base.metadata,
    'system': system.Base.metadata,
    'token': token.Base.metadata,
    'user': user.Base.metadata,
    'worker': worker.Base.metadata,
    'xhpastview': xhpastview.Base.metadata,
    'xhprof': xhprof.Base.metadata
}

def connect(db_url, keys):
    db_url_format = db_url + "/{0}?charset=utf8&use_unicode=0"
    for key in keys:
        if key not in db_tables:
            raise Exception("No DB matched with " + key)
        url = db_url_format.format("phabricator_" + key)
        db_tables[key].bind = create_engine(url)

def connect_all(db_url):
    connect(db_url, db_tables.keys())

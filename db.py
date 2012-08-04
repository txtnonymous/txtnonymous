"""Database module"""

from exceptions import RuntimeError
from datetime import datetime, timedelta
from pymongo import Connection
connection = Connection()

# Get your DB
db = connection['txtnonymous-dev']

class NotFoundException(RuntimeError):
    """Database record not found"""

def create_user(gid):
    oid = db.users.insert({
        'gid': gid,
        'tag': None,
        'expires': datetime.now()+timedelta(days=1)})
    print oid
    # FIXME: use the first 7 characters from the uid as the tag
    tag = str(oid)[:8]
    db.test.update({"_id": oid}, {"$set": {"tag": tag}})
    return db.users.find_one(oid)

def find_or_create(gid):
    u = db.users.find_one({"gid": gid})
    return u or create_user(gid)

def find(gid):
    u = db.users.find_one({"gid": gid})
    if not u:
        raise
    return u

def extend_timestamp(user):
    pass

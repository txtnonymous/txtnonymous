"""Database module"""

import os
from urllib.parse import urlsplit
from datetime import datetime, timedelta
from pymongo import MongoClient

url = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/txtnonymous-dev')
db = MongoClient(url)[urlsplit(url).path[1:]]

class NotFoundException(RuntimeError):
    """Database record not found"""

def find_user(gid=None, tag=None):
    if gid and tag:
        return db.users.find_one({"$or": [{"gid": gid}, {"tag": tag}]})
    elif gid:
        return db.users.find_one({"gid": gid})
    elif tag:
        return db.users.find_one({"tag": tag})
    else:
        return db.users.find_one()

def create_user(gid=None, tag=None):
    oid = db.users.insert({
        'gid': gid,
        'tag': tag,
        'expires': datetime.now()+timedelta(days=1)})
    if not tag:
        # FIXME: use the first 7 characters from the uid as the tag
        tag = str(oid)[:8]
        db.users.update({"_id": oid}, {"$set": {"tag": tag}})
    return db.users.find_one(oid)

def delete_user(user):
    db.users.remove(user)

def find_or_create(gid=None, tag=None):
    u = find_user(gid, tag)
    return u or create_user(gid)

def find(gid=None, tag=None):
    u = find_user(gid, tag)
    if not u:
        raise NotFoundException()
    return u

def extend_timestamp(user):
    pass

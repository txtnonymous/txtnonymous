"""Database module"""

from pymongo import Connection
connection = Connection()

# Get your DB
db = connection['default']

def find_or_create(gid):
    return None

def find(gid):
    return None

def extend_timestamp(user):
    pass

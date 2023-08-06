# -*- coding: utf-8 -*-
import re
import sys

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from pymongo.cursor import CursorType

from ipylib.idebug import *

from dataengineer.conf import Database


__all__ = [
    'get_db',
]


if hasattr(Database, 'name'):
    try:
        client = MongoClient(**Database.params())
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure:
        logger.error(['ConnectionFailure:', ConnectionFailure])
        raise
else:
    logger.error(['DB-Name을 설정하십시오', Database.__dict__])
    raise

def get_db(): return client[Database.name]

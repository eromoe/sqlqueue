#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2016-01-19 17:14:39
# @Last Modified by:   mithril
# @Last Modified time: 2016-01-20 10:23:18


import os


try:
    import cPickle as pickle
except ImportError:
    import pickle

from time import sleep
import threading

# try:
#     from thread import get_ident
# except ImportError:
#     from dummy_thread import get_ident

# thread is deprecated
# But there seems to be a bug where threading.current_thread().ident is inappropriately None. Probably makes sense just to use thread.get_ident() in Python 2 and threading.current_thread().ident in Python 3

import sqlite3
#from pysqlite2 import dbapi2 as sqlite3

# The pysqlite2 installer you probably got from here contains sqlite3 compiled into _sqlite.pyd, it doesn't use the dll found in the DLLs directory (that one is only uset by the sqlite3 module).

print sqlite3.sqlite_version

# sqlite 3.7 + support  Write Ahead Logging” (WAL)
# http://stackoverflow.com/questions/10325683/read-and-write-sqlite-database-data-concurrently-from-multiple-connections


def get_ident():
    return threading.current_thread().ident


class SqliteQueue(object):

    _create = (
            'CREATE TABLE IF NOT EXISTS queue '
            '('
            '  id INTEGER PRIMARY KEY AUTOINCREMENT,'
            '  item BLOB'
            ')'

            )
    _count = 'SELECT COUNT(*) FROM queue'
    _iterate = 'SELECT id, item FROM queue'
    _append = 'INSERT INTO queue (item) VALUES (?)'
    _write_lock = 'BEGIN IMMEDIATE'
    _popleft_get = (
            'SELECT id, item FROM queue '
            'ORDER BY id LIMIT 1'
            )
    _popleft_del = 'DELETE FROM queue WHERE id = ?'
    _peek = (
            'SELECT item FROM queue '
            'ORDER BY id LIMIT 1'
            )

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self._connection_cache = {}
        with self._get_conn() as conn:
            conn.execute(self._create)

    def __len__(self):
        with self._get_conn() as conn:
            l = conn.execute(self._count).next()[0]
        return l

    def __iter__(self):
        with self._get_conn() as conn:
            for id, obj_buffer in conn.execute(self._iterate):
                yield pickle.loads(str(obj_buffer))

    def _get_conn(self):
        id = get_ident()
        if id not in self._connection_cache:
            self._connection_cache[id] = sqlite3.Connection(self.path,
                    timeout=60)
        return self._connection_cache[id]

    def put(self, obj):
        obj_buffer = buffer(pickle.dumps(obj, 2))
        with self._get_conn() as conn:
            conn.execute(self._append, (obj_buffer,))

    def get(self, sleep_wait=True):
        keep_pooling = True
        wait = 0.1
        max_wait = 2
        tries = 0
        with self._get_conn() as conn:
            id = None
            while keep_pooling:
                conn.execute(self._write_lock)
                cursor = conn.execute(self._popleft_get)
                try:
                    id, obj_buffer = cursor.next()
                    keep_pooling = False
                except StopIteration:
                    conn.commit() # unlock the database
                    if not sleep_wait:
                        keep_pooling = False
                        continue
                    tries += 1
                    sleep(wait)
                    wait = min(max_wait, tries/10 + wait)
            if id:
                conn.execute(self._popleft_del, (id,))
                return pickle.loads(str(obj_buffer))
        return None

    def get_nowait(self):
        return self.get(False)

    def peek(self):
        with self._get_conn() as conn:
            cursor = conn.execute(self._peek)
            try:
                return pickle.loads(str(cursor.next()[0]))
            except StopIteration:
                return None



Queue = SqliteQueue
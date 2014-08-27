# -*- coding: utf-8 -*-
__author__ = 'dmitry'

import config
import os
import sqlite3
import logging
import sqlitedict
import app
import sqlalchemy



# class DbDict:
#     def __init__(self, sqlite_file):
#         database_name = os.path.join(config.BASE_DIR, sqlite_file)
#         logging.debug("Database: " + database_name)
#         self.data = sqlitedict.SqliteDict(database_name, autocommit=True)




# database_name = os.path.join(config.BASE_DIR, 'data.db')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_name






database_name = os.path.join(config.BASE_DIR, 'data.db')
logging.debug("Database: " + database_name)
data = sqlitedict.SqliteDict(database_name, autocommit=True)
data['test'] = 'blah'

class Db:
    def __init__(self, sqlite_file):
        database_name = os.path.join(config.BASE_DIR, sqlite_file)
        logging.debug("Database: " + database_name)
        if not os.path.isfile(database_name):
            logging.debug(sqlite_file + " doesn't exist, creating a new one")
        try:
            self.con = sqlite3.connect(database_name, row_factory=sqlite3.Row)
            self.cur = self.con.cursor()
            self.cur.execute('''CREATE TABLE IF NOT EXISTS tests
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name CHAR(255), project_name CHAR(255), url CHAR(1024), timeout INTEGER, status CHAR(255))''')
            self.con.commit()
        except sqlite3.IntegrityError:
            logging.error("Already exists")

        except Exception as e:
            logging.error("SQLite Error")

    def close(self):
        self.con.commit()
        self.con.close()

    def query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def query_dict(self, query):
        return dict(self.cur.execute(query, ()).fetchall())


    def get_last_id(self):
        return self.cur.lastrowid


def test_create(name, project_name, url, timeout, status='queued'):
    query = '''INSERT INTO tests (name, project_name, url, timeout, status) VALUES
                    ('{name}', '{project_name}', '{url}', {timeout}, '{status}')'''.format(name=name,
                                                                                           project_name=project_name,
                                                                                           url=url, timeout=timeout,
                                                                                           status=status)
    logging.debug(query)
    db = Db('rodent.db')

    db.query(query)

    test = {'id': db.get_last_id(), 'name': name, 'projectName': project_name, 'url': url, 'timeout': timeout, 'status': status}

    db.close()
    return test


def test_update(id, status):
    query = '''UPDATE tests SET status='{status}' WHERE id={id}'''.format(status=status, id=id)
    # TODO: Update task status
    #
    logging.debug(query)
    db = Db('rodent.db')

    db.query(query)

    test = {'id': id, 'status': status}

    db.close()
    return test


def tests_list_get(filter='all'):
    test = {}
    if filter == 'all':
        query = '''SELECT * FROM tests '''
    elif filter == 'queued' or filter == 'running' or filter == 'finished':
        query = '''SELECT * FROM tests WHERE state = '{state}' '''.format(status=filter)

    logging.debug(query)

    db = Db('rodent.db')
    test = db.query(query)
    db.close()

    return test


def test_get(test_id):
    test = {}
    query = '''SELECT * FROM tests WHERE id={test_id}'''.format(test_id=test_id)
    logging.debug(query)

    db = Db('rodent.db')
    test = db.query_dict(query)
    db.close()

    return test


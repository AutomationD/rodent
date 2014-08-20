# -*- coding: utf-8 -*-
__author__ = 'dmitry'

import config
import os
import sqlite3
import logging


class Db:
    def __init__(self, sqlite_file):
        database_name = os.path.join(config.BASE_DIR, sqlite_file)
        logging.debug("Database: " + database_name)
        if not os.path.isfile(database_name):
            logging.debug(sqlite_file + " doesn't exist, creating a new one")
        try:
            self.con = sqlite3.connect(database_name)
            self.cur = self.con.cursor()
            self.cur.execute('''CREATE TABLE IF NOT EXISTS tests
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name CHAR(255), project_name CHAR(255), url CHAR(1024), timeout INTEGER, status CHAR(255))''')
            self.con.commit()
        except sqlite3.IntegrityError:
            logging.error("Already exists")

        except Exception as e:
            logging.error("SQLite Error")

    def close(self):
        self.con.close()

    def query(self, query):
        # Insert a row of data
        self.cur.execute(query)
        self.con.commit()
        return self.cur.fetchall()

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


def test_update(name, project_name, url, timeout, status='queued'):
    query = '''INSERT INTO tests (name, project_name, url, timeout, status) VALUES
                    ('{name}', '{project_name}', '{url}', {timeout}, '{status}')'''.format(name=name,
                                                                                           project_name=project_name,
                                                                                           url=url, timeout=timeout,
                                                                                           status=status)
    # TODO: Update task status
    #
    # logging.debug(query)
    # db = Db('rodent.db')
    #
    # db.query(query)
    #
    # test = {'id': db.get_last_id(), 'name': name, 'projectName': project_name, 'url': url, 'timeout': timeout, 'status': status}
    #
    # db.close()
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
    test = db.query(query)
    db.close()

    return test


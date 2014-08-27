__author__ = 'dmitry'

from app import db
from sqlalchemy.orm import object_mapper


class _Base():
    def __init__(self):
        pass

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in object_mapper(self).mapped_table.c}

class Test(db.Model, _Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    project_name = db.Column(db.String(120))
    url = db.Column(db.String(1024))
    timeout = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __init__(self, name, project_name, url, timeout, status):
        self.name = name
        self.project_name = project_name
        self.url = url
        self.timeout = timeout
        self.status = status
    # def __repr__(self):
    #     return '<Name %r' % self.name

class TestResults(db.Model, _Base):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer)
    result = db.Column(db.Integer)
    result_message = db.Column(db.Integer)

    def __init__(self, test_id, result, result_message):
        self.test_id = test_id
        self.result = result
        self.result_message = result_message
    # def __repr__(self):
    #     return '<Name %r' % self.name


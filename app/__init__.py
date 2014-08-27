# -*- coding: utf-8 -*-
__author__ = 'dmitry'

import config
# import app.db as db

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import jsonify, make_response, request
import json



logger = config.setup_custom_logger()


app = Flask(__name__)


# # Configurations
app.config.from_object('config')

# Db init
db = SQLAlchemy(app)
import models

db.create_all()

# Static modules import
from app.modules import jdog
from app.modules import dns



# import app.modules.dns

## global (replace by configuration params)
# server = 'ns1.domain.corp'


def is_64_bit():
    import struct
    if (8 * struct.calcsize("P")) == 32:
        return False
    if (8 * struct.calcsize("P")) == 64:
        return True


###################### features: ######################
@app.route('/features/', methods=['GET'])
def features():
    if request.method == 'GET':
        features = ['dns', 'jdog']

        return make_response(json.dumps(features))
###################### :features ######################


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found' }), 404)


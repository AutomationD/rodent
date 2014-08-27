# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
import sys

## Logging
def setup_custom_logger():
    logging.basicConfig(format='%(asctime)s %(message)s', filename='rodent.log', level=logging.DEBUG, stream=sys.stdout)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    return logger




# Statement for enabling the development environment
DEBUG = True

# Define the application directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define bind IP address
BIND_IP = '0.0.0.0'

DNS_ENABLED = True

#DNS_SERVER_IP = '192.168.1.11'
# DNS_SERVER_IP = '8.8.8.8'
DNS_SERVER_IP = '127.0.0.1'

### jdog config ###
# USE_SELENIUM (True/False)
USE_SELENIUM = True



SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
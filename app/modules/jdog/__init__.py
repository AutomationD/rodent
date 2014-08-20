# -*- coding: utf-8 -*-
__author__ = 'dmitry'

# from subprocess import Popen, PIPE

import logging
import os
import shutil
import platform
import json

from flask import jsonify, make_response, request
from app import app
import app.db as db
import threading
# from jsonschema import validate
import subprocess

from pprint import pprint

logger = logging.getLogger()

# TODO:
"""
- Generate test uid (or id - will be used in browser/profiles
- Make sure browser is ready to run in a new profile
    - Create a separate executable
    - Be able to start a browser with a profile
√ Be able to store data in a local db (test_id, status, ...)
- Be able to control browser
    - Start app
    - Kill all process with a known process name (that contains test id)
"""


###################### jdog: ######################
# TODO: Create a loop that will pick first item in the queue (db - queued) and run test_start on their id


# Test runner
def test_start(test_id):
    result = {}
    command = test_init(test_id)
    # TODO: set task status to 'starting' and start a different thread
    result = command
    # result = test_get(test_id)
    return result

def test_init(test_id):
    # TODO: Set up browser environment

    while( True ):
        pass

    if platform.system() == 'Darwin':
        src_dir = '/Applications/Google Chrome.app/'
        dst_dir = "/Applications/Google Chrome-jdog-test-{test_id}.app/".format(test_id=test_id)

        if not os.path.exists(dst_dir):
            shutil.copytree(src_dir, dst_dir)
        else:
            logging.debug("{dst_dir} Already exists".format(dst_dir=dst_dir))

    return command

# Create a new test

@app.route('/jdog/create', methods=['POST'])
def test_create():
    result = {}
    # TODO: Add json validation

    # if request.json['name'] and request.json['projectName'] and request.json['url'] and request.json['timeout']:
    if request:
        result = db.test_create(request.json['name'], request.json['projectName'], request.json['url'], request.json['timeout'])
    else:
        result = {'result': 'error'}


    # TODO: Send task to a worker that will pick up queued item and start processing it. ->
    thread = threading.Thread(target=test_start, args=(result['id'],))
    thread.start()

    result['status'] = 'initializing'

    # TODO: ??? Check if test with the same name exists???

    return make_response(json.dumps(result))

@app.route('/jdog/<int:test_id>', methods=['GET'])
def test_get(test_id):
    test = db.test_get(test_id)

    result = test
    return make_response(json.dumps(result))

@app.route('/jdog/list/', methods=['GET'])
def tests_list():
    # TODO: Get list of queued tests (?filter=queued, ?filter=current)
    if request.args.get('filter'):
        tests_list = db.tests_list_get(request.args.get('filter'))
    else:
        tests_list = db.tests_list_get()
    return make_response(json.dumps(tests_list))

### /stop vs /finish?????
# Stop task (kill browsers for a test)
@app.route('/jdog/<int:test_id>/stop', methods=['GET'])
def test_stop(test_id):
    result = {}

    test = db.test_get(test_id)

    return make_response(json.dumps(test))

### /stop vs /finish?????
@app.route('/jdog/<int:test_id>/finish', methods=['GET'])
def test_finish(test_id):
    result = {}

    test = db.test_get(test_id)

    result = {'status': 1, 'test': test}
    return make_response(json.dumps(result))



@app.route('/jdog/<int:test_id>/stop_all', methods=['GET'])
def tests_stop_all():
    result = {}



    result = {'status': 1, 'test': test}
    return make_response(json.dumps(result))


# Remove task from the queue
@app.route('/jdog/<int:test_id>/clear', methods=['GET'])
def test_clear_queue(test_id):
    result = {}

    test = db.test_get(test_id)

    result = {'status': 1, 'test': test}
    return make_response(json.dumps(result))


# @app.route('/jdog/<int:test_id>/start/', methods=['POST'])
# def test_start(test_id):
#     import uuid
#     import time
#     import signal
#     # from selenium import webdriver
#
#     # logging.debug("test_id: " + str(test_id))
#     result = {}
#     #
#     #
#     # os.environ['SELENIUM_SERVER_JAR'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "selenium-server-standalone.jar")
#     #
#     #
#     # #Following are optional required
#     # # from selenium.webdriver.common.by import By
#     # # from selenium.webdriver.support.ui import Select
#     # # from selenium.common.exceptions import NoSuchElementException
#     #
#     #
#     # if not test_id:
#     #     return make_response(jsonify({'error': 'test_id must be present'}), 500)
#     #
#     # baseurl = "http://stg.quickbookslicenses.com/jdog/integration/endToEndRegistration.html?"+"&test_id="+str(test_id)
#     #
#     # ## Spawn each driver in a separate python queue, that will have test_id in it.
#     #
#     #
#     #
#     #
#     # driver = webdriver.Chrome(os.path.join(os.path.dirname(os.path.realpath(__file__)), "chromedriver"))
#     # time.sleep(3)
#     # driver.get(baseurl)
#     # driver.close()
#     # #
#     # # driver = webdriver.Firefox()
#     # #
#     # # time.sleep(3)
#     # # driver.get(baseurl)
#     # # # driver.close()
#     # #
#     # # driver = webdriver.Safari()
#     # # time.sleep(3)
#     # # driver.get(baseurl)
#     #
#     result['message'] = 'Started id:' + str(test_id)
#     result['response_code'] = 200
#     logging.debug(result['message'])
#
#     return make_response(jsonify({'result': result['message']}), result['response_code'])
#
#     # tasks.put(task_id)
#
#
#     ## Start Timer
#
#     ## IF Timer not stopped - ERORRRRRR!
###################### :jdog ######################
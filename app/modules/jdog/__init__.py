# -*- coding: utf-8 -*-
__author__ = 'dmitry'

# from subprocess import Popen, PIPE

import logging
import os
import shutil
import platform
import json

from pprint import pprint


import config

from flask import jsonify, make_response, request
from app import app
import threading

from app.modules.jdog import native
from app.modules.jdog import selenium
from app.models import Test, TestResults
from app import db

logger = logging.getLogger()



###################### jdog: ######################
# TODO: Create a loop that will pick first item in the queue (db - queued) and run test_start on their id


@app.route('/jdog/<int:test_id>/status', methods=['get'])
def test_status(test_id):
    thread_count = threading.active_count()
    return str(thread_count)

# Create a new test
@app.route('/jdog/create', methods=['POST'])
def test_create():
    result = {}
    # TODO: Add json validation
    # if request.json['name'] and request.json['projectName'] and request.json['url'] and request.json['timeout']:

    if request:
        test = Test('myname', 'project_name', 'http://test_url', 40, 'initializing')
        db.session.add(test)
        db.session.commit()
        result = test.to_dict()

    # else:
    #     result = {'result': 'error'}

    # If selenium was chosen
    # if config.USE_SELENIUM:
    #     # thread = threading.Thread(target=selenium.test_start, args=(result['id'],))
    #     thread = threading.Thread(target=selenium.test_start, args=(10,))
    # else:
    #     thread = threading.Thread(target=native.test_start, args=(result['id'],))
    #
    # thread.start()



    # TODO: ??? Check if test with the same name exists???

    return make_response(json.dumps(result))

@app.route('/jdog/<int:test_id>', methods=['GET'])
def test_get(test_id):
    test = (Test.query.get(test_id)).to_dict()

    result = test
    return make_response(json.dumps(result))

@app.route('/jdog/list/', methods=['GET'])
def tests_list():
    results = {}
    # TODO: Get list of queued tests (?filter=queued, ?filter=current)
    if request.args.get('filter'):
        # tests_list = db.tests_list_get(request.args.get('filter'))
        tests_list = Test.query.filter_by(status=request.args.get('filter'))

    else:
        tests_list = Test.query.all()

    for test in tests_list:
        results[test.to_dict()['id']] = test.to_dict()
    pprint(results)

    return make_response(json.dumps(results))

### /stop vs /finish?????
# Stop task (kill browsers for a test)
@app.route('/jdog/<int:test_id>/stop', methods=['GET'])
def test_stop(test_id):
    result = {}


    # TODO: Check if test is already stopped
    test = Test.query.get(test_id)
    test.status = 'stopped'
    db.session.commit()

    result = test.to_dict()
    return make_response(json.dumps(result))

@app.route('/jdog/<int:test_id>/start', methods=['GET'])
def test_start(test_id):
    result = {}


    # TODO: Check if test is already stopped
    test = Test.query.get(test_id)
    test.status = 'started'
    db.session.commit()

    result = test.to_dict()
    return make_response(json.dumps(result))

@app.route('/jdog/<int:test_id>/results', methods=['get'])
def test_result(test_id):
    result = {}
    results_rows = TestResults.query.filter_by(test_id=test_id)

    if results_rows.count():
        for results in results_rows:
            result[results.to_dict()['id']] = results.to_dict()
    else:
        result = {'result': 'no rows'}

    return make_response(json.dumps(result))


### /stop vs /finish????? >>>> finish saves whatever result was passed and stops
@app.route('/jdog/<int:test_id>/finish', methods=['GET'])
def test_finish(test_id):
    result = {}
    if request.args.get('result_message'):
        result_message = request.args.get('result_message')
    else:
        result_message = 'none'


    if request.args.get('result'):

        test_result = TestResults(test_id, request.args.get('result'), result_message)
        db.session.add(test_result)
        result = test_result.to_dict()
        db.session.commit()








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

    db.data.append({'name': 'data'})
    test = db.data

    result = {'status': 1, 'test': test}
    return make_response(json.dumps(result))

@app.route('/jdog/info', methods=['GET'])
def info_get():
    result = {}
    # db.data['a'] = ('yourname', 'George')
    test = db.data


    return make_response(test)


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
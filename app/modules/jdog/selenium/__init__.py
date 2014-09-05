__author__ = 'dmitry'
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import logging
from flask import jsonify, make_response, request
from app import db
from pprint import pprint
from app.models import Test, TestResults






def test_start(test_id):
    result = {}
    test = Test.query.get(test_id)
    test.status = 'started'
    db.session.commit()

    # test = db.test_get(test_id)


    driver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "chromedriver_mac32")
    logging.debug("chrome_driver path: " + driver_path)
    driver = webdriver.Chrome(driver_path)
    time.sleep(3)

    ## Temp variable - change to actual url param
    driver.get(test.url + '?job='+test_id)
    driver.close()


    #
    # driver = webdriver.Firefox()
    #
    # time.sleep(3)
    # driver.get(baseurl)
    # # driver.close()
    #
    # driver = webdriver.Safari()
    # time.sleep(3)
    # driver.get(baseurl)



    result = {'result': 'success', 'message': 'Started id:' + str(test.id) + ' ' + driver.session_id}
    # result['response_code'] = 200
    # logging.debug(result['message'])
    # db.DbDict.data.append({'name': 'data'})

    return result
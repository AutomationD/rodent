__author__ = 'dmitry'
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import logging
from flask import jsonify, make_response, request

from pprint import pprint



# os.environ['SELENIUM_SERVER_JAR'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "selenium-server-standalone.jar")

def test_start(test_id):
    result = {}
    # test = db.test_get(test_id)


    driver = webdriver.Chrome(os.path.join(os.path.dirname(os.path.realpath(__file__)), "chromedriver_mac32"))
    time.sleep(3)
    # driver.get(test['url'])
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

    result['message'] = 'Started id:' + str(test_id), driver.session_id
    # result['response_code'] = 200
    # logging.debug(result['message'])
    # db.DbDict.data.append({'name': 'data'})
    return result
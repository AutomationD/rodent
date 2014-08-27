__author__ = 'dmitry'


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
from subprocess import call
import time

global a

def test_cancel():
    global a
    a = True
    while a:
        print("Second function")
        time.sleep(1)


def test_start(test_id):
    # --disable-infobars
    # --disable-shared-workers
    # --extension-process ⊗
    # --new-window ⊗
    # --no-default-browser-check ⊗
    # --original-process-start-time ⊗
    # --trace-startup=base --trace-to-console ⊗
    #??--utility
    # --worker

    # ??--enable-strict-site-isolation
    command =['open', '-n', "/Applications/Chromium-jdog-test-{test_id}.app".format(test_id=test_id), "--args", "--profile-directory=jdog-test-{test_id}".format(test_id=test_id)]
    command.append("http://licenses.intuit.com?test_id={test_id}".format(test_id=test_id))

    subprocess.call(command)
    logging.debug(command)

thread = threading.Thread(target=test_start, args=('79',))
thread.start()

thread = threading.Thread(target=test_start, args=('78',))
thread.start()


thread = threading.Thread(target=test_start, args=('77',))
thread.start()

time.sleep(5)
a = False


print(str(threading.active_count()))
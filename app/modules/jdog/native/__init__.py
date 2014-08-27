# -*- coding: utf-8 -*-
__author__ = 'dmitry'

import logging
import subprocess
import platform
import os

# TODO:
"""
- Generate test uid (or id - will be used in browser/profiles
- Make sure browser is ready to run in a new profile
    - Create a separate executable
    - Be able to start a browser with a profile
√ Be able to store data in a native db (test_id, status, ...)
- Be able to control browser
    - Start app
    - Kill all process with a known process name (that contains test id)
"""

# Test runner
def test_start(test_id):
    result = {}
    test = db.test_get(test_id)

    command = test_init(test_id)
    command.append("http://licenses.intuit.com?test_id={test_id}".format(test_id=test_id))
    # command = ['open', '-a', "/Applications/Chromium-jdog-test-62.app/Contents/MacOS/Chromium", "--args", "--profile-directory=jdog-test-62"]
    # TODO: set task status to 'starting' and start a different thread
    result = command
    # subprocess.Popen(['open', '-a', "/Applications/Google Chrome-jdog-test-34.app", "--args", "--profile-directory=jdog-test-34"])

    subprocess.call(command)
    logging.debug(command)
    # call("open -a '" + command + "'")

    #subprocess.Popen('open -a /Applications/Google Chrome-jdog-test-34.app --args --profile-directory=jdog-test-34')
    db.test_update(test_id, 'started')
    return result

def test_init(test_id):
    if platform.system() == 'Darwin':
        src = '/Applications/Chromium.app'
        dst = "/Applications/Chromium-jdog-test-{test_id}.app".format(test_id=test_id)
        # command = ['open', '-n', src, "--args", "--no-first-run", "--profile-directory=jdog-test-{test_id}".format(test_id=test_id)]
        command = ['open', '-n', dst, "--args", "--no-first-run", "--profile-directory=jdog-test-{test_id}".format(test_id=test_id)]
        # command = ['open', '-a', os.path.join(dst, "Contents/MacOS/Chromium-jdog-test-{test_id}".format(test_id=test_id)), "--args", "--single-process", "--no-first-run", "--profile-directory=jdog-test-{test_id}".format(test_id=test_id)]
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
            # os.rename(os.path.join(dst, "Contents/MacOS/Chromium"), os.path.join(dst, "Contents/MacOS/Chromium-jdog-test-{test_id}".format(test_id=test_id)))
        else:
            logging.debug("{dst} Already exists".format(dst=dst))
    return command

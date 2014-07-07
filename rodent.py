# coding: interpy
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
__author__ = 'dmitry'

import config


import re
import sys
import os
from subprocess import Popen, PIPE
from flask import Flask
from flask import jsonify, make_response, request, abort
import logging

from Queue import Queue




## Logging
logging.basicConfig(format='%(asctime)s %(message)s', filename='rodent.log', level=logging.DEBUG, stream=sys.stdout)
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


app = Flask(__name__)


tasks = Queue(maxsize=0)

## global (replace by configuration params)
# server = 'ns1.docstoc.corp'


###################### jdog: ######################
@app.route('/jdog/test/<int:test_id>', methods=['GET'])
def test_get(test_id):
    tasks


@app.route('/jdog/test/<int:test_id>/stop', methods=['POST'])
def test_stop(test_id):
    # Stop the test with no timeout error
    return True


@app.route('/jdog/test/<int:test_id>/start/', methods=['POST'])
def test_start(test_id):
    import uuid
    import time
    import signal
    from selenium import webdriver

    logging.debug("test_id: " + str(test_id))
    result = {}


    os.environ['SELENIUM_SERVER_JAR'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "selenium-server-standalone.jar")


    #Following are optional required
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.common.exceptions import NoSuchElementException


    if not test_id:
        return make_response(jsonify({'error': 'test_id must be present'}), 500)

    baseurl = "http://stg.quickbookslicenses.com/jdog/integration/endToEndRegistration.html?"+"&test_id="+str(test_id)

    ## Spawn each driver in a separate python queue, that will have test_id in it.




    driver = webdriver.Chrome(os.path.join(os.path.dirname(os.path.realpath(__file__)), "chromedriver"))
    time.sleep(3)
    driver.get(baseurl)
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
    result['response_code'] = 200
    logging.debug(result['message'])

    return make_response(jsonify({'result': result['message']}), result['response_code'])

    tasks.put(task_id)


    ## Start Timer

    ## IF Timer not stopped - ERORRRRRR!

###################### :jdog ######################

###################### DNS: ######################
@app.route('/dns/', methods=['POST', 'DELETE'])
def dns(type='A', name_server='localhost'):
    import dns.name
    import dns.resolver
    result = {}

    if request.method == 'DELETE':
        # fqdn=test15.docstoc.corp&value=192.168.5.1&type=A
        if os.name == 'nt':

            fqdn = request.args.get('fqdn')
            if request.args.get('type'):
                type = request.args.get('type')


            if request.args.get('name_server'):
                name_server = request.args.get('name_server')

            if not fqdn:
                return make_response(jsonify({'error': 'fqdn must be present'}), 404)


            zone = dns.name.from_text(fqdn).split(3)[1].to_text(omit_final_dot=True)

            if dns_found(fqdn, type):

                if is_64_bit():
                    command = "c:\Windows\System32\dnscmd.exe /RecordDelete #{zone} #{fqdn}. A /f"
                else:
                    command = "c:\Windows\sysnative\dnscmd.exe /RecordDelete #{zone} #{fqdn}. A /f"

                logging.debug(command)

                process = Popen(command, stdout=PIPE)
                (output, err) = process.communicate()

                logging.debug("output: " + str(output))

                if err:
                    logging.debug("err: " + str(err))




                result['exit_code'] = process.wait()

                if result['exit_code'] != 0:
                    result['response_code'] = 500
                    result['message'] = "Error running #{command}. Error Code #{result['exit_code']}"
                else:
                    if not dns_found(fqdn, type):
                        result['exit_code'] = 0
                        result['response_code'] = 200
                        result['message'] = "Successfully deleted #{fqdn}"
                        logging.debug(result['message'])
                    else:
                        result['exit_code'] = 1
                        result['response_code'] = 404
                        result['message'] = "#{fqdn} is still there. Could be a bug."
                        logging.error(result['message'])
            else:
                result['exit_code'] = 1
                result['response_code'] = 500
                result['message'] = "#{fqdn} Does not exist."
                logging.error(result['message'])

        else:
            result['message'] = 'Not implemented for ' + os.name
            result['response_code'] = 501
            logging.error(result['message'])
        return make_response(jsonify({'result': result['message']}), result['response_code'])


    ### POST: ###
    elif request.method == 'POST':

        # fqdn=test15.docstoc.corp&value=192.168.5.1&type=A
        if os.name == 'nt':

            fqdn = request.args.get('fqdn')
            value = request.args.get('value')
            type = request.args.get('type')
            if request.args.get('name_server'):
                name_server = request.args.get('name_server')

            if not fqdn:
                return make_response(jsonify({'error': '"fqdn" variable must be present'}), 404)
            if not value:
                return make_response(jsonify({'error': '"value" variable must be present (IP, CNAME host, etc)'}), 404)
            if not type:
                return make_response(jsonify({'error': '"type" variable must be present (A, CNAME, etc)'}), 404)

            zone = dns.name.from_text(fqdn).split(3)[1].to_text(omit_final_dot=True)

            if not dns_found(fqdn, type):
                if is_64_bit():
                    command = "c:\Windows\System32\dnscmd.exe /RecordAdd #{zone} #{fqdn}. #{type} #{value}"
                else:
                    command = "c:\Windows\sysnative\dnscmd.exe /RecordAdd #{zone} #{fqdn}. #{type} #{value}"

                logging.debug(command)

                process = Popen(command, stdout=PIPE)
                (output, err) = process.communicate()

                logging.debug("output: \n" + output)

                if err:
                    logging.debug("err: \n" + err)

                result['exit_code'] = process.wait()

                if result['exit_code'] != 0:
                    result['response_code'] = 500
                    result['message'] = "Error running #{command}. Error Code #{result['exit_code']}"
                else:
                    if dns_found(fqdn, type):
                        result['exit_code'] = 0
                        result['response_code'] = 201
                        result['message'] = "Successfully created #{fqdn}"
                        logging.debug(result['message'])
                    else:
                        result['exit_code'] = 1
                        result['response_code'] = 404
                        result['message'] = "Can't find #{fqdn}. Could be a bug."
                        logging.error(result['message'])
            else:
                result['exit_code'] = 1
                result['response_code'] = 500
                result['message'] = "#{fqdn} Already exists."
                logging.error(result['message'])

        else:
            result['message'] = 'Not implemented for ' + os.name
            result['response_code'] = 501
            logging.error(result['message'])
        return make_response(jsonify({'result': result['message']}), result['response_code'])
    ### :POST ###

def dns_found(fqdn, type):
    import dns.name
    import dns.resolver

    logging.debug("Checking if " + fqdn + " type " + type + " exists")

    resolver = dns.resolver.Resolver(configure=False)


    if not config.DNS_SERVER_IP:
        config.DNS_SERVER_IP = '127.0.0.1'

    logging.debug("Using DNS server: " + config.DNS_SERVER_IP)
    resolver.nameservers = [config.DNS_SERVER_IP, ]

    try:
        #resolver.timeout = 5
        #resolver.lifetime = 10
        logging.debug("Querying " + config.DNS_SERVER_IP + " for " + fqdn)
        result = resolver.query(fqdn, type)

        logging.debug(fqdn + "resolved to" + str(result[0]))

        if result:
            return True
        else:
            return False
    except dns.exception.DNSException:
        logging.debug("Can't resolve " + fqdn + " on " + config.DNS_SERVER_IP)
        return False
###################### :DNS ######################

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found' }), 404)



def is_64_bit():
    import struct
    if (8 * struct.calcsize("P")) == 32:
        return False
    if (8 * struct.calcsize("P")) == 64:
        return True



if __name__ == '__main__':
    #print dns_found('www.google.com', "A")
    # import dns.name
    # import dns.resolver
    #
    # fqdn = 'www.google.com'
    # type = 'A'
    # logging.debug("Checking if " + fqdn + " type " + type + " exists")
    #
    # resolver = dns.resolver.Resolver(configure=False)
    #
    #
    # if not config.DNS_SERVER_IP:
    #     config.DNS_SERVER_IP = '127.0.0.1'
    #
    # logging.debug("Using DNS server: " + config.DNS_SERVER_IP)
    # resolver.nameservers = [config.DNS_SERVER_IP, ]
    #
    # # try:
    # resolver.timeout = 5
    # resolver.lifetime = 10
    # logging.debug("Querying " + str(config.DNS_SERVER_IP) + " for " + fqdn)
    # result = resolver.query(fqdn, type)
    # logging.debug(fqdn + "resolved to " + str(result[0]))
    #
    # if result:
    #     print True
    # else:
    #     print False
    # # except:
    # #     logging.debug("Can't resolve " + fqdn + " on " + config.DNS_SERVER_IP)
    # #     print False
    app.run(host=config.BIND_IP)

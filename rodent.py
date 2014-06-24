# coding: interpy
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
__author__ = 'dmitry'

import config
import struct
import re
import sys
import os
from subprocess import Popen, PIPE
import dns.name
import dns.resolver
from flask import Flask
from flask import jsonify, make_response, request, abort
import logging

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


## global (replace by configuration params)
# server = 'ns1.docstoc.corp'

################ DNS ################


@app.route('/dns/', methods=['POST'])
def create_dns():
    result = {}
    # fqdn=test15.docstoc.corp&value=192.168.5.1&type=A
    if os.name == 'nt':

        fqdn = request.args.get('fqdn')
        value = request.args.get('value')
        type = request.args.get('type')
        name_server = request.args.get('name_server')

        if not fqdn:
            return make_response(jsonify({'error': 'fqdn must be present'}), 404)
        if not value:
            return make_response(jsonify({'error': 'value must be present'}), 404)
        if not type:
            return make_response(jsonify({'error': 'type must be present'}), 404)
        if not type:
            return make_response(jsonify({'error': 'name_server must be present'}), 404)

        zone = dns.name.from_text(fqdn).split(3)[1].to_text(omit_final_dot=True)

        if not dns_found(fqdn, type):
            if is_64_bit():
                #cmd = r'c:\windows\sysnative\cmd.exe /c '
                command = "c:\Windows\System32\dnscmd.exe /RecordAdd #{zone} #{fqdn}. #{type} #{value}"
            else:
                #cmd = r'c:\windows\system32\cmd.exe /c '
                command = "c:\Windows\sysnative\dnscmd.exe /RecordAdd #{zone} #{fqdn}. #{type} #{value}"


            #command = cmd + "c:\Windows\System32\dnscmd.exe /RecordAdd #{zone} #{fqdn}. #{type} #{value}"
            print command

            process = Popen(command, stdout=PIPE)
            (output, err) = process.communicate()
            print "output:"
            print output

            print "err:"
            print err
            result['exit_code'] = process.wait()

            if result['exit_code'] != 0:
                result['response_code'] = 500
                result['message'] = "Error running #{command}. Error Code #{result['exit_code']}"
            else:
                if dns_found(fqdn, type):
                    result['exit_code'] = 0
                    result['response_code'] = 200
                    result['message'] = "Successfully created #{fqdn}"
                else:
                    result['exit_code'] = 1
                    result['response_code'] = 404
                    result['message'] = "Can't find #{fqdn}. Could be a bug."
        else:
            result['exit_code'] = 1
            result['response_code'] = 500
            result['message'] = "#{fqdn} Already exists."

    else:
        result['message'] = 'Not implemented for ' + os.name
        result['response_code'] = 501
    return make_response(jsonify({'result': result['message']}), result['response_code'])

def command_report(stdin, stderr, exit_code):
    return True




def dns_found(fqdn, type):

    resolver = dns.resolver.Resolver(configure=False)

    if not config.DNS_SERVER_IP:
        config.DNS_SERVER_IP = '127.0.0.1'

    logging.debug(config.DNS_SERVER_IP)
    resolver.nameservers = [config.DNS_SERVER_IP, ]

    try:
        resolver.timeout = 5
        resolver.lifetime = 10
        result = resolver.query(fqdn, type)

        if result:
            return True
        else:
            return False
    except:
        return False

################################################

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found' }), 404)



def is_64_bit():
    if (8 * struct.calcsize("P")) == 32:
        return False
    if (8 * struct.calcsize("P")) == 64:
        return True



if __name__ == '__main__':
    app.run(host=config.BIND_IP)

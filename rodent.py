# coding: interpy
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
__author__ = 'dmitry'

import config
import struct
import re
import sys
import os
import subprocess as sb
import dns.name
from flask import Flask
import logging
from flask import jsonify,make_response, request, abort
import socket

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
    # fqdn=test15.docstoc.corp&value=192.168.5.1&type=A
    if os.name == 'nt':

        fqdn = request.args.get('fqdn')
        value = request.args.get('value')
        type = request.args.get('type')

        if not fqdn:
            return make_response(jsonify({'error': 'fqdn must be present'}), 404)
        if not value:
            return make_response(jsonify({'error': 'value must be present'}), 404)
        if not type:
            return make_response(jsonify({'error': 'type must be present'}), 404)

        zone = dns.name.from_text(fqdn).split(3)[1].to_text(omit_final_dot=True)

        if not dns_found(fqdn):
            if is_64_bit():
                #cmd = r'c:\windows\sysnative\cmd.exe /c '
                command = "c:\Windows\sysnative\dnscmd.exe /RecordAdd #{zone} #{fqdn}. #{type} #{value}"
            else:
                #cmd = r'c:\windows\system32\cmd.exe /c '
                command = "c:\Windows\System32\dnscmd.exe /RecordAdd #{zone} #{fqdn}. #{type} #{value}"

            #command = cmd + "c:\Windows\System32\dnscmd.exe /RecordAdd #{zone} #{fqdn}. #{type} #{value}"
            print command

            sb.call(command)

            message = 'OK ' + zone, "cmd:", command

            return make_response(jsonify({'message': message}), 200)
    else:
        message = 'Not implemented for ' + os.name
        return make_response(jsonify({'error': message}), 500)


def dns_found(hostname):
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.error:
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

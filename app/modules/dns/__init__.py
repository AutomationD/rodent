__author__ = 'dmitry'


import config
import os
import logging
from app import app
from flask import jsonify, make_response, request

logger = logging.getLogger('root')



###################### DNS: ######################
@app.route('/dns/', methods=['POST', 'DELETE'])
def dns(type='A', name_server='localhost'):
    import dns.name
    import dns.resolver
    result = {}

    ### DELETE: ###
    if request.method == 'DELETE':
        # fqdn=test15.domain.corp&value=192.168.5.1&type=A
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
    ### :DELETE ###


    ### POST: ###
    elif request.method == 'POST':

        # fqdn=test15.domain.corp&value=192.168.5.1&type=A
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


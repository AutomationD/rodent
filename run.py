#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import config
from app import app



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
    #     config.DNS_SERVER_IP = '127.0.0.1'e
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

    app.run(host=config.BIND_IP, debug=config.DEBUG, threaded=True)
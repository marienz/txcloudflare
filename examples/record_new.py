#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

    Copyright 2013 Joe Harris

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

'''

'''

    Trivial example of how to add a DNS record to a domain. See:
    
    http://www.cloudflare.com/docs/client-api.html#s5.1

'''

import os, sys

# make sure our local copy of txcloudflare is in sys.path
PATH_TO_TXCF = '../txcloudflare/'
try:
    import txcloudflare
except ImportError:
    txcfpath = os.path.dirname(os.path.realpath(PATH_TO_TXCF))
    if txcfpath not in sys.path:
        sys.path.insert(0, txcfpath)

from twisted.internet import reactor
import txcloudflare

def got_response(response):
    '''
        'response' is a txcloudflare.response.Response() instance.
    '''
    print '< got a response (done)'
    for k,v in response.data.items():
        print k, '->', v
    reactor.stop()

def got_error(error):
    '''
        'error' is a twisted.python.failure.Failure() instance wrapping one of
        the exceptions in txcloudflare.errors. The exceptions return the
        CloudFlare error code, a plain text string and a response object
        (txcloudflare.response.Response). The response object has a 'request'
        parameter if you need to look at the reques that generated the error.
    '''
    print '< error'
    print error.printTraceback()
    reactor.stop()

email_address = os.environ.get('TXCFEMAIL', '')
api_token = os.environ.get('TXCFAPI', '')
domain_name = os.environ.get('TXCFDOMAIN', '')

if __name__ == '__main__':
    record_name = 'subdomain'
    record_content = 'mx.someserver.com'
    record_ttl = 1
    record_priority = 10
    print '> adding a MX DNS record for zone: {0}.{1} -> {2}'.format(record_name, domain_name, record_content)
    cloudflare = txcloudflare.client_api(email_address, api_token)
    
    # cloudflare.rec_new() parameters here are:
    #   zone                the domain name (required)
    #   record_type         one of A/CNAME/MX/TXT/SPF/AAAA/NS/SRV/LOC (required)
    #   name                name of subdomain, use @ for root (required)
    #   content             content of the DNS record (required)
    #   ttl                 TTL of the DNS record in seconds, between 120 and 4,294,967,295, 1 for automatic (required)
    #   priority            priority of DNS record, only works with a record_type of MX or SRV
    #   service             service, only works with record_type of SRV
    #   service_name        service name, only works with record_type of SRV
    #   service_protocol    service protocol, one of _tcp/_udp/_tls, only works with record_type of SRV
    #   service_weight      service weight, only works with record_type of SRV
    #   service_port        service port, only works with record_type of SRV
    #   service_target      service target, only works with record_type of SRV
    
    cloudflare.rec_new(
        zone=domain_name,
        record_type='MX',
        name=record_name,
        content=record_content,
        ttl=record_ttl,
        priority=record_priority
    ).addCallback(got_response).addErrback(got_error)
    reactor.run()

'''

    EOF

'''

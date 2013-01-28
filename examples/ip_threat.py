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

    Trivial example of how to check the threat score for an IP. See:
    
    http://www.cloudflare.com/docs/client-api.html#s3.6

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
    print '< got a response'
    for ip,status in response.data.items():
        print ip, '->', status
    reactor.stop()

def got_error(error):
    '''
        'error' is a twisted.python.failure.Failure() instance wrapping a
        txcloudflare.response.Response() instance.
    '''
    print '< error'
    print error.printTraceback()
    reactor.stop()

email_address = os.environ.get('TXCFEMAIL', '')
api_token = os.environ.get('TXCFAPI', '')

if __name__ == '__main__':
    ip = '8.8.8.8'
    print '> checking threat level of an ip: {0}'.format(ip)
    cloudflare = txcloudflare.client_api(email_address, api_token)
    cloudflare.ip_lkup(ip=ip).addCallback(got_response).addErrback(got_error)
    reactor.run()

'''

    EOF

'''

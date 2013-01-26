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

    Trivial example of how to get domain stats from CloudFlare. See:
    
    http://www.cloudflare.com/docs/client-api.html#s3.1

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
    for s in response.data:
        print s
    reactor.stop()

def got_error(response):
    '''
        'response' is a txcloudflare.response.Response() instance.
    '''
    print '< error'
    print response.error_code
    print response.error_message
    reactor.stop()

email_address = os.environ.get('TXCFEMAIL', '')
api_token = os.environ.get('TXCFAPI', '')

if __name__ == '__main__':
    print '> listing all domains'
    cloudflare = txcloudflare.api(email_address, api_token)
    cloudflare.zone_load_multi().addCallback(got_response).addErrback(got_error)
    reactor.run()

'''

    EOF

'''

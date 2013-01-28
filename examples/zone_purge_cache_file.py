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

    Trivial example of how to purge the cache for a single file in a zone. See:
    
    http://www.cloudflare.com/docs/client-api.html#s4.5

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
    for k,v in response.data.items():
        print k, '->', v
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
domain_name = os.environ.get('TXCFDOMAIN', '')

if __name__ == '__main__':
    some_url = 'http://{0}/some-file.html'.format(domain_name)
    print '> purging all cache for file: {0}'.format(some_url)
    cloudflare = txcloudflare.client_api(email_address, api_token)
    cloudflare.zone_file_purge(zone=domain_name, url=some_url).addCallback(got_response).addErrback(got_error)
    reactor.run()

'''

    EOF

'''
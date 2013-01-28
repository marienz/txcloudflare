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

    Trivial example of how to request CloudFlare to update their snapshot image
    if a site. As this uses the internal zone IDs (that need to be resolved with
    zone_check() first) this is a chained double-lookup example to show it using
    a zone name. See:
    
    http://www.cloudflare.com/docs/client-api.html#s4.6

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

# shuffle these up a bit in this example to increase their scope
email_address = os.environ.get('TXCFEMAIL', '')
api_token = os.environ.get('TXCFAPI', '')
domain_name = os.environ.get('TXCFDOMAIN', '')
cloudflare = txcloudflare.client_api(email_address, api_token)

def got_zone_id(response):
    '''
        'response' is a txcloudflare.response.Response() instance.
    '''
    print '< got first response (zone id lookup)'
    zone_id = response.data.get(domain_name, '')
    print '< zone {0} has zone id {1}'.format(domain_name, zone_id)
    print '> requesting snapshot update for zone:', zone_id
    
    def updated_snapshot(response):
        print '< got second response (updated snapshot)'
        print response.data
        reactor.stop()
    
    # send the second request now we have the zone id
    cloudflare.zone_grab(zone_id=zone_id).addCallback(updated_snapshot).addErrback(got_error)

def got_error(error):
    '''
        'error' is a twisted.python.failure.Failure() instance wrapping one of
        the exceptions in txcloudflare.errors. The exceptions return the
        CloudFlare error code, a plain text string, the request object that
        generated the error (txcloudflare.request.Request) and a response object
        (txcloudflare.response.Response).
    '''
    print '< error'
    print error.printTraceback()
    reactor.stop()



if __name__ == '__main__':
    print '> listing zone ids for: {0}'.format(domain_name)
    cloudflare.zone_check(zones=[domain_name]).addCallback(got_zone_id).addErrback(got_error)
    reactor.run()

'''

    EOF

'''

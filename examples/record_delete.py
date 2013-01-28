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

    Trivial example of how to delete a DNS record from a zone. As this uses the
    internal record ID (that need to be resolved with rec_load_all() first) this
    is a chained double-lookup example to show it used a record name. See:
    
    http://www.cloudflare.com/docs/client-api.html#s5.3

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

def got_record_list(response):
    '''
        'response' is a txcloudflare.response.Response() instance.
    '''
    print '< got first response (record id lookup)'
    target_name = 'subdomain.' + domain_name
    target_type = 'MX'
    target = {}
    for d in response.data:
        print d['type'], d['name'], d['display_content']
        if d['name'] == target_name and d['type'] == target_type:
            target = d
    
    def deleted_record(response):
        print '< got second response (deleted record)'
        reactor.stop()
    
    if target:
        # send the second request now we have the record id
        print '> requesting removal of "{0}" record "{1}" id: {2}'.format(target['type'], target['name'], target['rec_id'])
        cloudflare.rec_delete(zone=domain_name, record_id=target['rec_id']).addCallback(deleted_record).addErrback(got_error)
    else:
        # no matching record found to delete
        print '> no record matches "{0}" record "{1}"'.format(target['type'], target['name'])
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

if __name__ == '__main__':
    print '> listing all records for zone: {0}'.format(domain_name)
    cloudflare.rec_load_all(zone=domain_name).addCallback(got_record_list).addErrback(got_error)
    reactor.run()

'''

    EOF

'''

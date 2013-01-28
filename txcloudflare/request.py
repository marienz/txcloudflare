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

    Classes used to format requests properly.

'''

from urlparse import urlunsplit

from twisted.internet import defer
from twisted.python.failure import Failure

from txcloudflare.transport import HttpStreamReceiver
from txcloudflare.parse import Response
from txcloudflare.errors import RequestValidationException, TransportException

class HttpRequest(object):
    '''
    
        A base HTTP request providing some simple validation for requests as
        well as generating the required paramters for the transport.
    
    '''
    
    ACTION = ''
    METHOD = ''
    REQUIRED_PARAMS = ()
    OPTIONAL_PARAMS = ()
    PARAM_MAP = {}
    
    def __init__(self, request_name, transport):
        self.request_name = request_name
        self.transport = transport
        self.params = {}
        self.inverse_map = {}
        self.d = None
        for param_name,api_name in self.PARAM_MAP.items():
            self.inverse_map[api_name] = param_name
    
    def get_method(self):
        if self.METHOD not in self.transport.METHODS:
            raise RequestValidationException('invalid HTTP method specified: {0}'.format(self.METHOD))
        return self.METHOD
    
    def get_request_url(self):
        return urlunsplit((
            self.transport.TRANSPORT_SCHEME,
            self.transport.TRANSPORT_NETLOC,
            self.transport.TRANSPORT_URI,
            '',
            ''
        ))
    
    def get_post_data(self):
        return self.params
    
    def go(self):
        self.params['a'] = self.ACTION
        for k,v in self.transport.get_auth_params().items():
            self.params[k] = v
        self.d = defer.Deferred()
        method = self.get_method()
        url = self.get_request_url()
        post_data = self.get_post_data()
        self.transport.do_request(method=method, url=url, post_data=post_data).addBoth(self._got_reply)
        return self.d
    
    def _got_reply(self, r):
        # this means we got a twisted.web._newclient.Response object or a 
        # twisted.python.failure.Failure object. Response() is the start of an
        # HTTP stream, Failure() means there was a transport error connecting
        # to the API
        if isinstance(r, Failure):
            self.d.errback(TransportException(r))
        else:
            response = Response()
            response.request = self
            response.raw_headers = list(r.headers.getAllRawHeaders())
            r.deliverBody(HttpStreamReceiver(self, response, self.d))
    
    def validate(self):
        for p in self.REQUIRED_PARAMS:
            z = self.inverse_map.get(p, p)
            if p not in self.params:
                raise RequestValidationException('request "{0}" requires parameter: {1})'.format(self.request_name, z))
                return False
        for k,v in self.params.items():
            if k in self.REQUIRED_PARAMS:
                f = self.REQUIRED_PARAMS[k]
            else:
                f = self.OPTIONAL_PARAMS[k]
            try:
                self.params[k] = f(v)
            except:
                raise RequestValidationException('param "{0}" is required to be of type: {1})'.format(k, f))
                return False
        return True
    
    def pre_process(self, params):
        return params
    
    def post_process(self, data):
        return data
    
    def __call__(self, *a, **k):
        for param_key,param_val in k.items():
            api_key = self.PARAM_MAP.get(param_key, None)
            if api_key in self.REQUIRED_PARAMS or api_key in self.OPTIONAL_PARAMS:
                self.params[api_key] = param_val
            elif param_key in self.REQUIRED_PARAMS or param_key in self.OPTIONAL_PARAMS:
                self.params[param_key] = param_val
        self.validate()
        self.params = self.pre_process(self.params)
        return self.go()

'''

    EOF

'''

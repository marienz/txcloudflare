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

    Transport provides the generic wrapper interface to the CloudFlare API that
    provides a generic point to create and process the requests.

'''

from urllib import urlencode
from urlparse import urlsplit
from collections import OrderedDict

from zope.interface import implements
from twisted.internet import reactor, protocol
from twisted.web.client import Agent
from twisted.web.iweb import IBodyProducer
from twisted.web.http_headers import Headers
from twisted.internet.defer import succeed

import txcloudflare, txcloudflare.requests
from txcloudflare.parse import Parser
from txcloudflare.errors import *

# try and import the verifying SSL context from txverifyssl
try:
    from txverifyssl.context import VerifyingSSLContext as SSLContextFactory
except ImportError:
    # if txverifyssl is not installed default to the built-in SSL context, this works but has no SSL verification
    from twisted.internet.ssl import ClientContextFactory
    class SSLContextFactory(ClientContextFactory):
        def getContext(self, hostname, port):
            return ClientContextFactory.getContext(self)

class TransportBase(object):
    '''
    
        The transport base class.
    
    '''
    
    def do_request(self, *a, **k):
        raise TransportException('do_request() must be overridden')

class HttpTransport(TransportBase):
    '''
    
        Extends the TransportBase to provide an interface to HTTP and HTTPS
        endpoints.
    
    '''
    
    UA = 'txcloudflare'
    TRANSPORT_SCHEME = ''
    TRANSPORT_NETLOC = ''
    TRANSPORT_URI = ''
    API_RESPONSE_EXCEPTIONS = {}
    METHOD_GET = 'GET'
    METHOD_POST = 'POST'
    METHOD_PUT = 'PUT'
    METHOD_DELETE = 'DELETE'
    METHOD_HEAD = 'HEAD'
    METHODS = (
        METHOD_GET,
        METHOD_POST,
        METHOD_PUT,
        METHOD_DELETE,
        METHOD_HEAD,
    )
    
    def do_http_request(self, method='', url='', post_data={}):
        '''
        
            Performs an HTTP or HTTPS request and returns a deferred that fires
            the callback when the request is complete.
        
        '''
        
        method = method.upper()
        if method not in self.METHODS:
            raise TransportException('invalid HTTP method specified: {0}'.format(method))
        
        url_parts = urlsplit(url)
        scheme = url_parts.scheme.lower()
        if scheme == 'https':
            context = SSLContextFactory()
            if hasattr(context, 'set_expected_host'):
                context.set_expected_host(url)
            agent = Agent(reactor, context)
        elif scheme == 'http':
            agent = Agent(reactor)
        else:
            raise TransportException('only HTTP and HTTPS schemes are supported')
        
        if type(post_data) != dict:
            raise TransportException('post_data must be a dictionary')
        if method == self.METHOD_POST and not post_data:
            raise TransportException('post_data must contain data when the method is POST')
        
        #print 'method:', method
        #print 'url:', url
        #print 'data:', post_data
        
        producer = HttpStreamProducer(urlencode(OrderedDict(post_data))) if post_data else None
        request_headers = {'User-Agent': [self.UA + ' v' + txcloudflare.__version__]}
        if method == self.METHOD_POST:
            request_headers['Content-Type'] = ['application/x-www-form-urlencoded']
        return agent.request(method, url, Headers(request_headers), producer)
    
    def do_request(self, *a, **k):
        method = k.get('method', '')
        url = k.get('url', '')
        post_data = k.get('post_data', {})
        return self.do_http_request(method, url, post_data)

class HttpStreamProducer(object):
    '''
    
        Produces an stream of data on request to send to the remote HTTP
        server. This is used to encode and send HTTP POST data.
    
    '''
    
    implements(IBodyProducer)
    
    def __init__(self, data):
        self.body = data
        self.length = len(self.body)
    
    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)
    
    def pauseProducing(self):
        pass
    
    def stopProducing(self):
        pass

class HttpStreamReceiver(protocol.Protocol):
    '''
    
        Receives the downstream data from an HTTP connection in chunks.
    
    '''
    
    def __init__(self, request, response, d):
        self.request = request
        self.response = response
        self.d = d
    
    def dataReceived(self, data):
        self.response.raw_data += data
    
    def connectionLost(self, reason):
        # on connection lost we can assume we have connected to the API and got
        # a reply of some kind, time to fire off our request callback and parse
        # the response
        self.response = Parser(self.response).get_parsed()
        self.response.data = self.response.request.post_process(self.response.data)
        if self.response.error:
            e = self.request.transport.API_RESPONSE_EXCEPTIONS.get(self.response.error_code, ApiResponseException)
            self.d.errback(e(self.response.error_code, self.response.error_message, self.response))
        else:
            self.d.callback(self.response)

class CloudFlareClientTransport(HttpTransport):
    '''
    
        CloudFlare client API specific transport.
    
    '''
    
    TRANSPORT_SCHEME = 'https'
    TRANSPORT_NETLOC = 'www.cloudflare.com'
    TRANSPORT_URI = 'api_json.html'
    API_RESPONSE_EXCEPTIONS = {
        'E_UNAUTH': ApiInvalidAuthException,
        'E_INVLDINPUT': ApiInvalidInputException,
        'E_MAXAPI': ApiExceededLimitException,
    }
    
    def __init__(self, email_address='', api_token=''):
        self.email_address = email_address
        self.api_token = api_token
        if not self.email_address:
            raise TransportException('email_address parametermust be set')
        if not self.api_token:
            raise TransportException('api_token parameter must be set')
        # dynamically load all the child requests
        for r in txcloudflare.requests.__all__:
            __import__('txcloudflare.requests.{0}'.format(r))
    
    def get_auth_params(self):
        return {
            'email': self.email_address,
            'tkn': self.api_token,
        }
    
    def __getattr__(self, attr):
        if attr not in txcloudflare.requests.__all__:
            raise TransportException('unknown API request: {0}'.format(attr))
        request = getattr(txcloudflare.requests, attr, None)
        if not request or not hasattr(request, 'api_request'):
            raise TransportException('invalid API request: {0}'.format(attr))
        return request.api_request(attr, self)

'''

    EOF

'''

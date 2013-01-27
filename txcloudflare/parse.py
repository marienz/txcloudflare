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

    Parse a response into something standardised.

'''

import json

class Parser(object):
    '''
    
        Populate the raw data in a Response() object into something hopefully
        more usable.
    
    '''
    
    def __init__(self, response):
        self.response = response
        try:
            self.response.json = json.loads(self.response.raw_data)
            self.response.decoded = True
        except:
            self.response.json = {}
            self.response.decoded = True
        self.parse_headers()
        if self.response.decoded:
            self.check_error()
            if not self.response.error:
                self.check_data()
    
    def get_parsed(self):
        return self.response
    
    def parse_headers(self):
        for h in self.response.raw_headers:
            self.response.headers[h[0]] = h[1][0]
    
    def check_error(self):
        self.response.success = False if self.response.json.get('result', 'error') == 'error' else True
        self.response.error = False if self.response.success else True
        if self.response.error:
            self.response.error_code = self.response.json.get('err_code', '')
            self.response.error_message = self.response.json.get('msg', '')
    
    def check_data(self):
        self.response.data = self.response.json.get('response', {})
        self.response.request_data = self.response.json.get('request', {})

class Response(object):
    '''
    
        A generic and sane container for response information. Provides basic
        validation to test if the request completed successfully with naive
        string checks.
    
    '''
    
    def __init__(self):
        self.request = None
        self.raw_headers = []
        self.raw_data = ''
        self.json = {}
        self.headers = {}
        self.decoded = False
        self.success = False
        self.error = True
        self.error_code = ''
        self.error_message = ''
        self.data = {}
        self.request_data = {}

'''

    EOF

'''

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

    Ban/blacklist an IP. See:
    
    http://www.cloudflare.com/docs/client-api.html#s4.7

'''

from txcloudflare.request import HttpRequest
from txcloudflare.errors import RequestValidationException

class IpBanRequest(HttpRequest):
    
    ACTION = 'ban'
    METHOD = 'POST'
    REQUIRED_PARAMS = {
        'key': str,
    }
    OPTIONAL_PARAMS = {}
    PARAM_MAP = {
        'ip': 'key',
    }
    
    def pre_process(self, params):
        return params
    
    def post_process(self, data):
        return data.get('result', {})

api_request = IpBanRequest

'''

    EOF

'''

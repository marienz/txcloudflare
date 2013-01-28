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

    Set the cache level for a zone. See:
    
    http://www.cloudflare.com/docs/client-api.html#s4.2

'''

from txcloudflare.request import HttpRequest
from txcloudflare.errors import RequestValidationException

class SetCacheLevelRequest(HttpRequest):
    
    ACTION = 'cache_lvl'
    METHOD = 'POST'
    REQUIRED_PARAMS = {
        'z': str,
        'v': str,
    }
    OPTIONAL_PARAMS = {}
    PARAM_MAP = {
        'zone': 'z',
        'level': 'v',
    }
    
    def pre_process(self, params):
        allowed_levels = ('agg', 'basic')
        l = params.get('v', None).lower()
        if l not in allowed_levels:
            raise RequestValidationException('param "level" can only be one of: {0}'.format(','.join(allowed_levels)))
        params['v'] = l
        return params
    
    def post_process(self, data):
        return data.get('zone', {}).get('obj', {})

api_request = SetCacheLevelRequest

'''

    EOF

'''

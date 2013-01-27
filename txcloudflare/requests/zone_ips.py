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

    Get the IPs that have recently accessed a zone. See:
    
    http://www.cloudflare.com/docs/client-api.html#s3.5

'''

from txcloudflare.request import HttpRequest
from txcloudflare.errors import RequestValidationException

class ZoneIpsRequest(HttpRequest):
    
    ACTION = 'zone_ips'
    METHOD = 'POST'
    REQUIRED_PARAMS = {
        'z': str,
        'hours': int,
    }
    OPTIONAL_PARAMS = {
        'class': str,
    }
    PARAM_MAP = {
        'zone': 'z',
        'hours': 'hours',
        'filter_by': 'class',
    }
    
    def pre_process(self, params):
        class_map = {
            'regular': 'r',
            'crawler': 'c',
            'threat': 't',
        }
        f = params.get('class', None)
        if f:
            if f not in class_map:
                keys = ','.join(interval_map.keys())
                raise RequestValidationException('optional param "filter_by" can only be one of: {0}'.format(keys))
            params['class'] = class_map.get(f, None)
        params['geo'] = 1
        return params
    
    def post_process(self, data):
        return data.get('ips', [])

api_request = ZoneIpsRequest

'''

    EOF

'''

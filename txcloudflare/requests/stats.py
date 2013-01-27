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

    Get the statistics for a zone. See:
    
    http://www.cloudflare.com/docs/client-api.html#s3.1

'''

from txcloudflare.request import HttpRequest
from txcloudflare.errors import RequestValidationException

class StatsRequest(HttpRequest):
    
    ACTION = 'stats'
    METHOD = 'POST'
    REQUIRED_PARAMS = {
        'z': str,
        'interval': int
    }
    OPTIONAL_PARAMS = {}
    PARAM_MAP = {
        'zone': 'z',
        'hours': 'interval',
    }
    
    def pre_process(self, params):
        interval = params.get('interval', 0)
        interval_map = {
            6: 120,
            12: 110,
            24: 40,
            168: 30,
            720: 20,
        }
        cf_interval = interval_map.get(interval, None)
        if not cf_interval:
            keys = ','.join(str(x) for x in sorted(interval_map.keys()))
            raise RequestValidationException('param "hours" can only be one of: {0}'.format(keys))
        params['interval'] = cf_interval
        return params
    
    def post_process(self, data):
        return data.get('result', {}).get('objs', [])

api_request = StatsRequest

'''

    EOF

'''

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

    Delete a DNS record from a zone by record ID. See:
    
    http://www.cloudflare.com/docs/client-api.html#s5.3

'''

from txcloudflare.request import HttpRequest
from txcloudflare.errors import RequestValidationException

class DeleteDnsRecordRequest(HttpRequest):
    
    ACTION = 'rec_delete'
    METHOD = 'POST'
    REQUIRED_PARAMS = {
        'z': str,
        'id': int,
    }
    OPTIONAL_PARAMS = {}
    PARAM_MAP = {
        'zone': 'z',
        'record_id': 'id',
    }
    
    def pre_process(self, params):
        return params
    
    def post_process(self, data):
        return data

api_request = DeleteDnsRecordRequest

'''

    EOF

'''

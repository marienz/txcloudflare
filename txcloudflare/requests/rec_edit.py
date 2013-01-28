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

    Add a DNS record to a zone. See:
    
    http://www.cloudflare.com/docs/client-api.html#s5.1

'''

from txcloudflare.request import HttpRequest
from txcloudflare.errors import RequestValidationException

class EditDnsRecordRequest(HttpRequest):
    
    ACTION = 'rec_edit'
    METHOD = 'POST'
    REQUIRED_PARAMS = {
        'z': str,
        'type': str,
        'name': str,
        'content': str,
        'ttl': int,
        'id': int,
    }
    OPTIONAL_PARAMS = {
        'prio': int,
        'service': str,
        'srvname': str,
        'protocol': str,
        'weight': int,
        'port': int,
        'target': str,
        'service_mode': bool,
    }
    PARAM_MAP = {
        'zone': 'z',
        'record_id': 'id',
        'record_type': 'type',
        'name': 'name',
        'content': 'content',
        'ttl': 'ttl',
        'priority': 'prio',
        'service': 'service',
        'service_name': 'srvname',
        'service_protocol': 'protocol',
        'service_weight': 'weight',
        'service_port': 'port',
        'service_target': 'target',
        'proxy': 'service_mode',
    }
    
    def pre_process(self, params):
        if 'service_mode' in params:
            params['service_mode'] = 1 if params['service_mode'] else 0
        if 120 > params['ttl'] < 4294967295 and params['ttl'] != 1:
            raise RequestValidationException('ttl must be between 120 and 4294967295 (or 1), got: {0}'.format(params['ttl']))
        srv_required = ('priority', 'service', 'srvname', 'protocol', 'weight', 'port', 'target')
        mx_required = ('prio',)
        if params['type'] == 'SRV':
            for p in srv_required:
                if not params.get(p, False):
                    raise RequestValidationException('record type "SRV" requires parameter "{0}"'.format(p))
        elif params['type'] == 'MX':
            for p in mx_required:
                if not params.get(p, False):
                    raise RequestValidationException('record type "MX" requires parameter "{0}"'.format(p))
            for p in srv_required:
                if p not in mx_required:
                    if p in params:
                        del params[p]
        else:
            for p in srv_required:
                if p in params:
                    del params[p]
        if params['name'] == params['z']:
            params['name'] = '@'
        return params
    
    def post_process(self, data):
        return data.get('rec', {}).get('obj', {})

api_request = EditDnsRecordRequest

'''

    EOF

'''

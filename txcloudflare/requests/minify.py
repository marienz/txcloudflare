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

    Set the async Rocket Loader level for a zone. See:
    
    http://www.cloudflare.com/docs/client-api.html#s4.9

'''

from txcloudflare.request import HttpRequest
from txcloudflare.errors import RequestValidationException

class SetMinifyLevelRequest(HttpRequest):
    
    ACTION = 'minify'
    METHOD = 'POST'
    REQUIRED_PARAMS = {
        'z': str,
        'css': bool,
        'js': bool,
        'html': bool,
    }
    OPTIONAL_PARAMS = {}
    PARAM_MAP = {
        'zone': 'z',
        'css': 'css',
        'js': 'js',
        'html': 'html',
    }
    
    def pre_process(self, params):
        css = params.get('css', False)
        js = params.get('js', False)
        html = params.get('html', False)
        if css and js and html:
            params['v'] = 7
        elif css and not js and html:
            params['v'] = 6
        elif not css and js and html:
            params['v'] = 5
        elif not css and not js and html:
            params['v'] = 4
        elif css and js and not html:
            params['v'] = 3
        elif css and not js and not html:
            params['v'] = 2
        elif not css and js and not html:
            params['v'] = 1
        else:
            params['v'] = 0
        del params['css']
        del params['js']
        del params['html']
        return params
    
    def post_process(self, data):
        return data

api_request = SetMinifyLevelRequest

'''

    EOF

'''

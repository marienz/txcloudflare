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

    Contains the custom exceptions that can be raised during api request
    validation, transport and parsing.

'''

class TransportException(Exception):
    '''
    
        Raised when there is an error during the transport or requests.
    
    '''

class RequestValidationException(Exception):
    '''
    
        Raised when validating a request before dispatching it.
    
    '''

class ApiInvalidAuthException(Exception):
    '''
    
        Raised when the API request returns an E_UNAUTH error (authentication details were invalid).
    
    '''

class ApiInvalidInputException(Exception):
    '''
    
        Raised when the API request returns an E_INVLDINPUT error (some other part of the request was invalid).
    
    '''

class ApiExceededLimitException(Exception):
    '''
    
        Raised when the API request returns an E_MAXAPI error (exceeded API request limits).
    
    '''

class ApiResponseException(Exception):
    '''
    
        Raised when the API request returns any other error code.
    
    '''

'''

    EOF

'''

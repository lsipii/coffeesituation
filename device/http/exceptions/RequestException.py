#!/usr/bin/env python3
"""
@author lsipii
"""
class RequestException(Exception):
    def __init__(self, message, code = 500):
    	self.message = message
    	self.code = code
    def __str__(self):
    	return repr({self.message, self.code})
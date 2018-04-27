# -*- coding: utf-8 -*-
"""
@author lsipii
"""
class ConnectionException(Exception):
	def __init__(self, message):
		super().__init__(message)

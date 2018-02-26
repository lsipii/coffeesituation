#!/usr/bin/env python3
"""
@author lsipii
"""
from flask_restful import Resource

class BaseController(Resource):

	"""
	The base getter
	
	@params (dict) params = None
	@return (json ojb)
	"""
	def get(self, params = None):
		return self.getNotFoundResponse()

	"""
	The base setter
	
	@params (dict) params = None
	@return (json ojb)
	"""
	def set(self, params = None):
		return self.getNotFoundResponse()

	"""
	The base 404 response
	
	@params (dict) params = None
	@return (json ojb)
	"""
	def getNotFoundResponse(self, params = None):
		return {"message": "Why are you jamming?"}
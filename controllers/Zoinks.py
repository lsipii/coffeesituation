#!/usr/bin/env python3
"""
@author lsipii
"""
from flask_restful import Resource

class Zoinks(Resource):
	def get(self, access_key = None):
		return {"message": "Why are you jamming?"}
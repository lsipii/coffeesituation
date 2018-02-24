#!/usr/bin/env python3
"""
@author lsipii
"""
from flask_restful import Resource
from features.CoffeeChecker import CoffeeChecker
from app.AccessChecker import AccessChecker

class Zoinks(Resource):
	def get(self, accessKey = None):
		if AccessChecker().ifAccessGranted(accessKey):
			return CoffeeChecker().hasWeCoffee()
		else:
			return {"message": "Why are you jamming?"}
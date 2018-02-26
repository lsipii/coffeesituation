#!/usr/bin/env python3
"""
@author lsipii
"""

from controllers.BaseController import BaseController
from features.CoffeeChecker import CoffeeChecker
from app.AccessChecker import AccessChecker

class Zoinks(BaseController):
	def get(self, params = None):
		if AccessChecker().ifAccessGranted():
			return CoffeeChecker().hasWeCoffee()
		else:
			return self.getNotFoundResponse()
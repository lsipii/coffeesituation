#!/usr/bin/env python3
"""
@author lsipii
"""
from flask import Flask, request
from flask_restful import Resource, Api

from controllers.Zoinks import Zoinks

app = Flask("tshzoink")
api = Api(app)

api.add_resource(Zoinks, '/<string:accessKey>', '/')


if __name__ == '__main__':
    app.run(debug=True)
#!/usr/bin/env python3
"""
@author lsipii
"""
from flask import Flask
from flask_restful import Api

from controllers.Zoinks import Zoinks

app = Flask("tshzoink")
api = Api(app)

api.add_resource(Zoinks, '/')

if __name__ == '__main__':
    app.run(debug=True)
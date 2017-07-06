#!/usr/bin/python

import logging 
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask.json import JSONEncoder
import handler

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        
        return obj.__dict__

class MyFlask(Flask):
    def make_response(self, rv):
        if hasattr(rv, 'response') and rv.response is None:
            return super(MyFlask, self).make_response(rv)
        if hasattr(rv, 'new_url') and rv.new_url is not None:
            return super(MyFlask, self).make_response(rv)
        return super(MyFlask, self).make_response(jsonify(rv))

app = MyFlask(__name__)
app.json_encoder = CustomJSONEncoder

@app.route('/', methods=['GET'])
def index():
    return handler.get_index(app)

@app.route('/config', methods=['GET'])
def im_alive(name):
    return handler.list_config(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80222)

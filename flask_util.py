#!/usr/bin/env/python3

from flask import jsonify

API_NAME = 'tv'
API_NAME_KEY = 'api_name'
RESPONSE_KEY = 'response'
VERSION = '1.0'
VERSION_KEY = 'version'


def flask_response(response_string):
    """
    https://stackoverflow.com/questions/7907596/json-dumps-vs-flask-jsonify
    :param response_string:
    :return: a flask.Response object
    """
    data = {API_NAME_KEY: API_NAME,
            VERSION_KEY: VERSION,
            RESPONSE_KEY: response_string}

    json = jsonify(data)
    return json


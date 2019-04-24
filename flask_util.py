#!/usr/bin/env/python3

from enum import Enum
from flask import jsonify


class ServiceConstants(Enum):
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
    data = {ServiceConstants.API_NAME_KEY.value: ServiceConstants.API_NAME.value,
            ServiceConstants.VERSION_KEY.value: ServiceConstants.VERSION.value,
            ServiceConstants.RESPONSE_KEY.value: response_string.value}

    print('flask_response data: {}'.format(data))
    json = jsonify(data)
    return json


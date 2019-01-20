#!/usr/bin/env/python3

""" A Flask web service to accept television command requests (e.g. volume decrease, volume increase)
and instruct a transmitter (e.g. infrared) to transmit command
"""

from flask import Flask, jsonify, request

# app is a flask object
app = Flask(__name__)

API_NAME_KEY = 'api_name'
RESPONSE_KEY = 'response'
VERSION_KEY = 'version'

API_NAME = 'tv'
VERSION = '1.0'


def transmit_command(command):
    """
    instruct infrared transmitter to transmit command
    :parameter command: a string. # TODO: consider use an enum
    :return: data dictionary with status 'success'
    Note success indicates command was sent, not if any television received command
    """

    # f string requires python >= 3.6
    response = f'transmitted command {command}'

    # TODO: send command to infrared transmitter
    if command == "volume-decrease":
        pass
    elif command == "volume-increase":
        pass

    data = {API_NAME_KEY: API_NAME,
            VERSION_KEY: VERSION,
            RESPONSE_KEY: response}

    return jsonify(data)


# / is the website root, the entry point
# http://127.0.0.1:5000
# home http://127.0.0.1
# port :5000
@app.route('/')
@app.route("/api/v1/tv/ping/", methods=['GET'])
def api_status():
    if request.method == 'GET':
        data = {API_NAME_KEY: API_NAME,
                VERSION_KEY: VERSION,
                RESPONSE_KEY: 'pong'}

        return jsonify(data)


# api use hyphens not underscore to increase searchability
# https://stackoverflow.com/questions/10302179/hyphen-underscore-or-camelcase-as-word-delimiter-in-uris#18450653

# POST but not GET because GET should not change any state on the server
@app.route("/api/v1/tv/volume-decrease/", methods=['POST'])
def volume_decrease():
    return transmit_command("volume-decrease")


@app.route("/api/v1/tv/volume-increase/", methods=['POST'])
def volume_increase():
    return transmit_command("volume-increase")


if __name__ == '__main__':
    try:
        # '0.0.0.0' accessible to any device on the network
        app.run(host='0.0.0.0', debug=True)
    except RuntimeError:
        pass
    finally:
        # fix RunTimeWarning This channel is already in use
        # may need to put in a try:catch:finally finally section to handle exceptions
        pass


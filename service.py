#!/usr/bin/env/python3

""" A Flask web service to accept television command requests (e.g. volume decrease, volume increase)
and instruct a transmitter (e.g. infrared) to transmit command
"""

# Enum requires Python >= 3.4
from enum import Enum

from flask import Flask, jsonify, request
import subprocess

# app is a flask object
app = Flask(__name__)

API_NAME_KEY = 'api_name'
RESPONSE_KEY = 'response'
VERSION_KEY = 'version'

API_NAME = 'tv'
VERSION = '1.0'

# lirc commands
IRSEND = 'irsend'
SEND_ONCE = 'SEND_ONCE'

# use LIRC remote control configuration file /etc/lirc/lircd.conf.d/polk.lirc.conf
IR_REMOTE = 'polk'


class IrCommand(Enum):
    KEY_MUTE = 'KEY_MUTE'
    KEY_VOLUMEDOWN = 'KEY_VOLUMEDOWN'
    KEY_VOLUMEUP = 'KEY_VOLUMEUP'
    KEY_UP = 'KEY_UP'
    KEY_DOWN = 'KEY_DOWN'


def transmit_command(command):
    """
    instruct infrared transmitter to transmit command
    :parameter command: an IrCommand with a .value of type String.
    :return: data dictionary with status 'success'
    Note success indicates command was sent, not if any television received command
    """

    # f string requires Python >= 3.6, so don't use it yet.
    # response = f'transmitted command {command}'
    response = 'transmitted command {}'.format(command.value)

    # Don't allow user to run arbitrary string input, that is a security risk.
    #
    # If LIRC irsend isn't installed, throws error:
    # FileNotFoundError: [Errno 2] No such file or directory: 'irsend': 'irsend'
    # Can run unit tests on macOS by temporarily disabling subprocess.call(IRSEND...)
    #
    # subprocess.run requires Python >= 3.5, so don't use it yet.
    # subprocess.run([IRSEND, SEND_ONCE, IR_REMOTE, IrCommand.KEY_VOLUMEDOWN.value])
    subprocess.call([IRSEND, SEND_ONCE, IR_REMOTE, command.value])

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

@app.route("/api/v1/tv/mute/", methods=['POST'])
def mute():
    return transmit_command(IrCommand.KEY_MUTE)


@app.route("/api/v1/tv/voice-decrease/", methods=['POST'])
def voice_decrease():
    return transmit_command(IrCommand.KEY_DOWN)


@app.route("/api/v1/tv/voice-increase/", methods=['POST'])
def voice_increase():
    return transmit_command(IrCommand.KEY_UP)


@app.route("/api/v1/tv/volume-decrease/", methods=['POST'])
def volume_decrease():
    return transmit_command(IrCommand.KEY_VOLUMEDOWN)


@app.route("/api/v1/tv/volume-increase/", methods=['POST'])
def volume_increase():
    return transmit_command(IrCommand.KEY_VOLUMEUP)


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


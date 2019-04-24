#!/usr/bin/env/python3

""" A Flask web service to accept remote control command requests (e.g. volume decrease, volume increase)
and instruct a transmitter (e.g. infrared) to transmit command
"""

from flask import Flask, jsonify, request

from remote_command import RemoteCommand
from ir_remote import transmit_command_ir

import scheduler


# app is a flask object
app = Flask(__name__)

API_NAME_KEY = 'api_name'
RESPONSE_KEY = 'response'
VERSION_KEY = 'version'

API_NAME = 'tv'
VERSION = '1.0'


def route(command):
    """
    :param command: a RemoteCommand
    :return: route string
    """
    return "/api/v1/{}/{}/".format(API_NAME, command.value)


def transmit_command(command):
    """
    instruct infrared transmitter to transmit command
    :parameter command: a RemoteCommand
    :return: data dictionary with status 'success'
    Note success indicates command was sent, not if any television received command
    """

    # mac doesn't have an ir transmitter.
    # Can run unit tests on macOS by temporarily commenting out call to transmit_command_ir
    transmit_command_ir(command)

    # f string requires Python >= 3.6, so don't use it yet.
    # response = f'transmitted command {command}'
    response = 'transmitted command {}'.format(command.value)

    data = {API_NAME_KEY: API_NAME,
            VERSION_KEY: VERSION,
            RESPONSE_KEY: response}

    return jsonify(data)


# / is the website root, the entry point
# http://127.0.0.1:5000
# home http://127.0.0.1
# port :5000
@app.route('/')
@app.route("/api/v1/{}/ping/".format(API_NAME), methods=['GET'])
def api_status():
    if request.method == 'GET':
        data = {API_NAME_KEY: API_NAME,
                VERSION_KEY: VERSION,
                RESPONSE_KEY: 'pong'}

        return jsonify(data)


# POST but not GET because GET should not change any state on the server

@app.route(route(RemoteCommand.MUTE), methods=['POST'])
def mute():
    return transmit_command(RemoteCommand.MUTE)


@app.route(route(RemoteCommand.POWER), methods=['POST'])
def power():
    return transmit_command(RemoteCommand.POWER)


@app.route(route(RemoteCommand.VOICE_DECREASE), methods=['POST'])
def voice_decrease():
    return transmit_command(RemoteCommand.VOICE_DECREASE)


@app.route(route(RemoteCommand.VOICE_INCREASE), methods=['POST'])
def voice_increase():
    return transmit_command(RemoteCommand.VOICE_INCREASE)


@app.route(route(RemoteCommand.VOLUME_DECREASE), methods=['POST'])
def volume_decrease():
    return transmit_command(RemoteCommand.VOLUME_DECREASE)


@app.route(route(RemoteCommand.VOLUME_INCREASE), methods=['POST'])
def volume_increase():
    return transmit_command(RemoteCommand.VOLUME_INCREASE)


@app.route("/api/v1/{}/volume-decrease-increase/".format(API_NAME), methods=['POST'])
def volume_duck():
    return scheduler.Scheduler.volume_decrease_increase(decrease_count=4, increase_count=3, duration_seconds=10)


if __name__ == '__main__':

    # runs jobs at scheduled times
    # scheduler = scheduler.Scheduler()
    # scheduler.schedule_jobs()

    try:
        # start Flask web service
        # '0.0.0.0' accessible to any device on the network
        app.run(host='0.0.0.0', debug=True)
    except RuntimeError:
        pass
    finally:
        # fix RunTimeWarning This channel is already in use
        # may need to put in a try:catch:finally finally section to handle exceptions
        pass


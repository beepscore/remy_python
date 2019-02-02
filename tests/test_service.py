#!/usr/bin/env/python3

import unittest
from flask import Flask
from service import IrCommand, transmit_command


class TestTvService(unittest.TestCase):

    def setUp(self):
        # https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask
        app = Flask(__name__)
        app.app_context().push()

    def test_transmit_command_mute(self):

        json_expected = {'api_name': 'tv',
                         'version': '1.0',
                         'response': 'transmitted command KEY_MUTE'}

        # call method under test
        # http://flask.pocoo.org/docs/0.12/api/#response-objects
        response = transmit_command(IrCommand.KEY_MUTE)

        self.assertEqual(len(response.headers), 2)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, json_expected)

    def test_transmit_command_volume_decrease(self):

        json_expected = {'api_name': 'tv',
                         'version': '1.0',
                         'response': 'transmitted command KEY_VOLUMEDOWN'}

        # call method under test
        # http://flask.pocoo.org/docs/0.12/api/#response-objects
        response = transmit_command(IrCommand.KEY_VOLUMEDOWN)

        self.assertEqual(len(response.headers), 2)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, json_expected)

    def test_transmit_command_volume_increase(self):

        json_expected = {'api_name': 'tv',
                         'version': '1.0',
                         'response': 'transmitted command KEY_VOLUMEUP'}

        # call method under test
        # http://flask.pocoo.org/docs/0.12/api/#response-objects
        response = transmit_command(IrCommand.KEY_VOLUMEUP)

        self.assertEqual(len(response.headers), 2)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, json_expected)

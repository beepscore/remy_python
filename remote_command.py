#!/usr/bin/env/python3

# Enum requires Python >= 3.4
from enum import Enum

""" Remote control commands. Independent of transmitter type (e.g. infrared, Bluetooth, wifi)
"""


class RemoteCommand(Enum):
    """ api use hyphens not underscore to increase searchability
    https://stackoverflow.com/questions/10302179/hyphen-underscore-or-camelcase-as-word-delimiter-in-uris#18450653
    mute alternate calls toggle sound off and on
    power alternate calls toggle power off and on
    """
    MUTE = 'mute'
    POWER = 'power'
    VOICE_DECREASE = 'voice-decrease'
    VOICE_INCREASE = 'voice-increase'
    VOLUME_DECREASE = 'volume-decrease'
    VOLUME_INCREASE = 'volume-increase'


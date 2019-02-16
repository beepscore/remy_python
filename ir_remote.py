#!/usr/bin/env/python3

""" Instructs an infrared transmitter to transmit a command
"""
from remote_command import RemoteCommand

import subprocess
import logging_util

# instantiate at module level, not class level
# https://stackoverflow.com/questions/22807972/python-best-practice-in-terms-of-logging
logger = logging_util.get_logger(__name__)

# use constants and unit tests to help guard against misspelling
# lirc commands
IRSEND = 'irsend'
SEND_ONCE = 'SEND_ONCE'

# directory /etc/lirc/lircd.conf.d may contain multiple remote control configuration files e.g.
# /polk.lirc.conf
POLK_IR_REMOTE = 'polk'


def ir_command(command):
    """
    Translates and "sanitizes" command
    :parameter command: typically a RemoteCommand. Caller could supply arbitrary string or other object.
    :return: valid command string for infrared remote, else None
    values from LIRC remote control configuration file /etc/lirc/lircd.conf.d/polk.lircd.conf
    """
    command_dict = {
        RemoteCommand.MUTE: 'KEY_MUTE',
        RemoteCommand.POWER: 'KEY_POWER',
        RemoteCommand.VOICE_DECREASE: 'KEY_DOWN',
        RemoteCommand.VOICE_INCREASE: 'KEY_UP',
        RemoteCommand.VOLUME_DECREASE: 'KEY_VOLUMEDOWN',
        RemoteCommand.VOLUME_INCREASE: 'KEY_VOLUMEUP'
    }
    return command_dict.get(command)


def transmit_command_ir(command):
    """
    Instructs infrared transmitter to transmit command
    Uses python subprocess to call LIRC irsend.
    Doesn't allow user to run arbitrary input, that would be a security risk.
    :parameter command: typically a RemoteCommand. Caller could supply arbitrary string or other object.
    """

    # translate and "sanitize" command
    ir_command_string = ir_command(command)

    logger.debug('command: {}'.format(command))
    # e.g.
    # 2019-02-16 13:36:02 DEBUG    transmit_command_ir line:58 command: RemoteCommand.MUTE

    if ir_command_string is None:
        # command unrecognized
        return

    # If LIRC irsend isn't installed, throws error:
    # FileNotFoundError: [Errno 2] No such file or directory: 'irsend': 'irsend'
    #
    # subprocess.run requires Python >= 3.5, so don't use it yet.
    subprocess.call([IRSEND, SEND_ONCE, POLK_IR_REMOTE, ir_command_string])


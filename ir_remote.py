#!/usr/bin/env/python3

""" Instructs a transmitter (e.g. infrared) to transmit a command
"""
from remote_command import RemoteCommand

import subprocess

# lirc commands
IRSEND = 'irsend'
SEND_ONCE = 'SEND_ONCE'

# use LIRC remote control configuration file /etc/lirc/lircd.conf.d/polk.lirc.conf
IR_REMOTE = 'polk'


def ir_command(command):
    # values from LIRC remote control configuration file /etc/lirc/lircd.conf.d/polk.lirc.conf
    dict = {
        RemoteCommand.MUTE: 'KEY_MUTE',
        RemoteCommand.VOICE_DECREASE: 'KEY_DOWN',
        RemoteCommand.VOICE_INCREASE: 'KEY_UP',
        RemoteCommand.VOLUME_DECREASE: 'KEY_VOLUMEDOWN',
        RemoteCommand.VOLUME_INCREASE: 'KEY_VOLUMEUP',
    }
    return dict.get(command)


def transmit_command_ir(command):
    """
    instruct infrared transmitter to transmit command
    :parameter command: an IrCommand with a .value of type String.
    :return: data dictionary with status 'success'
    Note success indicates command was sent, not if any television received command
    """

    ir_command_string = ir_command(command)

    # Don't allow user to run arbitrary string input, that is a security risk.
    #
    # If LIRC irsend isn't installed, throws error:
    # FileNotFoundError: [Errno 2] No such file or directory: 'irsend': 'irsend'
    #
    # subprocess.run requires Python >= 3.5, so don't use it yet.
    subprocess.call([IRSEND, SEND_ONCE, IR_REMOTE, ir_command_string])


#!/usr/bin/env/python3

# Potential alternatives:
# Use cron, available on Raspberry Pi Raspbian Linux don't need to worry about Windows
# flask-apscheduler adds support for flask context but I think that's not needed here
# https://apscheduler.readthedocs.io/en/latest/userguide.html
from apscheduler.schedulers.background import BackgroundScheduler

import json
import datetime

from collections import namedtuple
from remote_command import RemoteCommand
from ir_remote import transmit_command_ir

cron = 'cron'
day_of_week = 'mon-sun'

QuietTime = namedtuple('QuietTime', 'start end')


def schedule_jobs():
    """ Calls remote control functions based on time of day
    """
    scheduler = BackgroundScheduler()
    # apscheduler job store- use default MemoryJobStore, in memory, not persisted
    # apscheduler executor- use default

    # can add jobs before or after starting scheduler
    add_jobs_ir_remote(scheduler)
    scheduler.start()


def add_jobs_ir_remote(scheduler):
    """
    https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html#module-apscheduler.triggers.cron
    :param scheduler: an APScheduler
    """
    # add_jobs_volume(quiet_times18, scheduler)

    quiet_times = get_quiet_times('./data/quiet_times.json')
    add_jobs_mute(quiet_times, scheduler)


def get_quiet_times(filename):
    """
    reads a json text file of the form
    [
        {"start": {"hour": 17, "minute": 17, "second": 0}, "end": {"hour": 17, "minute": 20, "second": 0}},
        {"start": {"hour": 17, "minute": 27, "second": 0}, "end": {"hour": 17, "minute": 31, "second": 20}},
    ]
    :param filename: a string, e.g. './data/quiet_times.json'
    :return: a list of QuietTime
    """
    with open(filename, 'r') as f:
        quiet_times_from_json = json.load(f)

    quiet_times = []

    for quiet_time_dict in quiet_times_from_json:

        quiet_time = quiet_time_from_dict(quiet_time_dict)
        quiet_times.append(quiet_time)

    return quiet_times


def quiet_time_from_dict(quiet_time_dict):
    """
    :param quiet_time_dict: a dictionary of the form
    {"hour": 17, "minute": 27, "second": 0}, "end": {"hour": 17, "minute": 31, "second": 20}
    :return: a QuietTime
    """
    start_dict = quiet_time_dict.get("start")
    end_dict = quiet_time_dict.get("end")

    start_time = time_from_dict(start_dict)
    end_time = time_from_dict(end_dict)

    quiet_time = QuietTime(start_time, end_time)
    return quiet_time


def time_from_dict(time_dict):
    """
    :param time_dict: a dictionary of the form
    {"hour": 17, "minute": 27, "second": 0}
    :return: a datetime.time
    """
    # datetime.time: An idealized time, independent of any particular day
    date_time_time = datetime.time(hour=time_dict.get("hour"),
                                   minute=time_dict.get("minute"),
                                   second=time_dict.get("second"))
    return date_time_time


def add_jobs_volume(quiet_times, scheduler):

    for quiet_time in quiet_times:

        # explicitly instantiating CronTrigger is more verbose but I hoped it would be more clear
        # trigger_start = CronTrigger(hour=quiet_time.start.hour,
        #                             minute=quiet_time.start.minute,
        #                             second=quiet_time.start.second)
        # add_job with a pre instantiated trigger didn't work, I didn't figure out correct syntax
        # scheduler.add_job(transmit_command_ir, cron, trigger_start, args=[RemoteCommand.VOLUME_DECREASE])
        # scheduler.add_job(transmit_command_ir_volume_decrease, cron, trigger_start)

        # add_job, implicitly create the trigger
        # args is for function transmit_command_ir
        scheduler.add_job(transmit_command_ir, cron,
                          day_of_week=day_of_week,
                          hour=quiet_time.start.hour, minute=quiet_time.start.minute, second=quiet_time.start.second,
                          args=[RemoteCommand.VOLUME_DECREASE])
        scheduler.add_job(transmit_command_ir, cron,
                          day_of_week=day_of_week,
                          hour=quiet_time.end.hour, minute=quiet_time.end.minute, second=quiet_time.end.second,
                          args=[RemoteCommand.VOLUME_INCREASE])


def add_jobs_mute(quiet_times, scheduler):
    """ mute sound during each quiet time
    """

    for quiet_time in quiet_times:
        # add_job, implicitly create the trigger
        # args is for function transmit_command_ir
        # first call to mute toggles sound off
        scheduler.add_job(transmit_command_ir, cron,
                          day_of_week=day_of_week,
                          hour=quiet_time.start.hour, minute=quiet_time.start.minute, second=quiet_time.start.second,
                          args=[RemoteCommand.MUTE])
        # next call to mute toggles sound on
        scheduler.add_job(transmit_command_ir, cron,
                          day_of_week=day_of_week,
                          hour=quiet_time.end.hour, minute=quiet_time.end.minute, second=quiet_time.end.second,
                          args=[RemoteCommand.MUTE])


if __name__ == '__main__':

    # from command line, python scheduler.py will run schedule, won't run Flask service
    schedule_jobs()

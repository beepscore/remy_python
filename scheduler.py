#!/usr/bin/env/python3

# Potential alternatives:
# Use cron, available on Raspberry Pi Raspbian Linux don't need to worry about Windows
# flask-apscheduler adds support for flask context but I think that's not needed here
# https://apscheduler.readthedocs.io/en/latest/userguide.html
from apscheduler.schedulers.background import BackgroundScheduler

import datetime

from collections import namedtuple
from remote_command import RemoteCommand
from ir_remote import transmit_command_ir

cron = 'cron'
day_of_week = 'mon-sun'

QuietTime = namedtuple('QuietTime', 'start end')

# datetime.time: An idealized time, independent of any particular day
# TODO: consider read quiet_times from a json file
quiet_times_debug = [
    QuietTime(datetime.time(hour=17, minute=1, second=0), datetime.time(hour=17, minute=2, second=0)),
    QuietTime(datetime.time(hour=17, minute=3, second=0), datetime.time(hour=17, minute=4, second=0)),
    QuietTime(datetime.time(hour=17, minute=5, second=0), datetime.time(hour=17, minute=6, second=0)),
    QuietTime(datetime.time(hour=17, minute=7, second=0), datetime.time(hour=17, minute=8, second=0)),
    QuietTime(datetime.time(hour=17, minute=9, second=0), datetime.time(hour=17, minute=10, second=0)),
    QuietTime(datetime.time(hour=17, minute=11, second=0), datetime.time(hour=17, minute=12, second=0)),
    QuietTime(datetime.time(hour=17, minute=13, second=0), datetime.time(hour=17, minute=14, second=0)),
    QuietTime(datetime.time(hour=17, minute=15, second=0), datetime.time(hour=17, minute=16, second=0)),
    QuietTime(datetime.time(hour=17, minute=17, second=0), datetime.time(hour=17, minute=18, second=0)),
    QuietTime(datetime.time(hour=17, minute=19, second=0), datetime.time(hour=17, minute=20, second=0)),
    QuietTime(datetime.time(hour=17, minute=21, second=0), datetime.time(hour=17, minute=22, second=0)),
    QuietTime(datetime.time(hour=17, minute=23, second=0), datetime.time(hour=17, minute=24, second=0)),
    QuietTime(datetime.time(hour=17, minute=25, second=0), datetime.time(hour=17, minute=26, second=0)),
    QuietTime(datetime.time(hour=17, minute=27, second=0), datetime.time(hour=17, minute=28, second=0)),
    QuietTime(datetime.time(hour=17, minute=29, second=0), datetime.time(hour=17, minute=30, second=0)),
    QuietTime(datetime.time(hour=17, minute=31, second=0), datetime.time(hour=17, minute=32, second=0)),
    QuietTime(datetime.time(hour=17, minute=33, second=0), datetime.time(hour=17, minute=34, second=0)),
    QuietTime(datetime.time(hour=17, minute=35, second=0), datetime.time(hour=17, minute=36, second=0)),
    QuietTime(datetime.time(hour=17, minute=37, second=0), datetime.time(hour=17, minute=38, second=0))
]

quiet_times18 = [
    QuietTime(datetime.time(hour=18, minute=1, second=0), datetime.time(hour=18, minute=2, second=0)),
    QuietTime(datetime.time(hour=18, minute=3, second=0), datetime.time(hour=18, minute=4, second=0)),
    QuietTime(datetime.time(hour=18, minute=5, second=0), datetime.time(hour=18, minute=6, second=0)),
    QuietTime(datetime.time(hour=18, minute=7, second=0), datetime.time(hour=18, minute=8, second=0)),
    QuietTime(datetime.time(hour=18, minute=9, second=0), datetime.time(hour=18, minute=10, second=0))
]


def schedule_jobs():
    """ Calls remote control functions based on time of day
    """
    scheduler = BackgroundScheduler()
    # apscheduler job store- use default MemoryJobStore, in memory, not persisted
    # apscheduler executor- use default

    scheduler.start()
    add_ir_jobs(scheduler)


def add_ir_jobs(scheduler):
    """
    https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html#module-apscheduler.triggers.cron
    :param scheduler: an APScheduler
    """
    # add_jobs_volume(quiet_times18, scheduler)
    add_jobs_mute(quiet_times_debug, scheduler)


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

    for quiet_time in quiet_times:
        # add_job, implicitly create the trigger
        # args is for function transmit_command_ir
        scheduler.add_job(transmit_command_ir, cron,
                          day_of_week=day_of_week,
                          hour=quiet_time.start.hour, minute=quiet_time.start.minute, second=quiet_time.start.second,
                          args=[RemoteCommand.MUTE])
        scheduler.add_job(transmit_command_ir, cron,
                          day_of_week=day_of_week,
                          hour=quiet_time.end.hour, minute=quiet_time.end.minute, second=quiet_time.end.second,
                          args=[RemoteCommand.MUTE])


if __name__ == '__main__':

    # from command line, python scheduler.py will run schedule, won't run Flask service
    schedule_jobs()

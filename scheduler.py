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
quiet_times17 = [
    # observed sunday
    QuietTime(datetime.time(hour=17, minute=17, second=0), datetime.time(hour=17, minute=20, second=0)),
    QuietTime(datetime.time(hour=17, minute=27, second=0), datetime.time(hour=17, minute=31, second=20)),
    QuietTime(datetime.time(hour=17, minute=38, second=15), datetime.time(hour=17, minute=41, second=45)),
    QuietTime(datetime.time(hour=17, minute=48, second=0), datetime.time(hour=17, minute=51, second=50)),
    QuietTime(datetime.time(hour=17, minute=54, second=20), datetime.time(hour=17, minute=57, second=50))
]

quiet_times18 = [
    QuietTime(datetime.time(hour=18, minute=7, second=0), datetime.time(hour=18, minute=10, second=0)),
    QuietTime(datetime.time(hour=18, minute=17, second=0), datetime.time(hour=18, minute=20, second=0)),
    QuietTime(datetime.time(hour=18, minute=27, second=0), datetime.time(hour=18, minute=31, second=20)),
    QuietTime(datetime.time(hour=18, minute=38, second=15), datetime.time(hour=18, minute=41, second=45)),
    QuietTime(datetime.time(hour=18, minute=48, second=0), datetime.time(hour=18, minute=51, second=50)),
    QuietTime(datetime.time(hour=18, minute=54, second=20), datetime.time(hour=18, minute=57, second=50))
]


def schedule_jobs():
    """ Calls remote control functions based on time of day
    """
    scheduler = BackgroundScheduler()
    # apscheduler job store- use default MemoryJobStore, in memory, not persisted
    # apscheduler executor- use default

    # can add jobs before or after starting scheduler
    add_ir_jobs(scheduler)
    scheduler.start()


def add_ir_jobs(scheduler):
    """
    https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html#module-apscheduler.triggers.cron
    :param scheduler: an APScheduler
    """
    # add_jobs_volume(quiet_times18, scheduler)
    add_jobs_mute(quiet_times17, scheduler)


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

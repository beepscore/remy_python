#!/usr/bin/env/python3

# Potential alternatives:
# Use cron, available on Raspberry Pi Raspbian Linux don't need to worry about Windows
# flask-apscheduler adds support for flask context but I think that's not needed here
# https://apscheduler.readthedocs.io/en/latest/userguide.html
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import datetime

from collections import namedtuple
from remote_command import RemoteCommand
from ir_remote import transmit_command_ir


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

    cron = 'cron'

    QuietTime = namedtuple('QuietTime', 'start end')

    # datetime.time: An idealized time, independent of any particular day
    # TODO: consider implement weekdays e.g. via datetime.datetime
    quiet_times = [
        QuietTime(datetime.time(hour=11, minute=1, second=0), datetime.time(hour=11, minute=2, second=0)),
        QuietTime(datetime.time(hour=18, minute=1, second=0), datetime.time(hour=18, minute=2, second=0)),
    ]

    for quiet_time in quiet_times:

        # explicitly instantiating CronTrigger is a little more verbose but hopefully more clear.
        # Alternatively could write as
        # scheduler.add_job(transmit_command_ir(RemoteCommand.VOLUME_DECREASE), cron,
        #                  hour=quiet_time.start.hour, minute=quiet_time.start.minute, second=quiet_time.start.second)
        trigger_start = CronTrigger(hour=quiet_time.start.hour,
                                    minute=quiet_time.start.minute,
                                    second=quiet_time.start.second)
        trigger_end = CronTrigger(hour=quiet_time.end.hour,
                                  minute=quiet_time.end.minute,
                                  second=quiet_time.end.second)

        scheduler.add_job(transmit_command_ir(RemoteCommand.VOLUME_DECREASE), cron, trigger_start)
        scheduler.add_job(transmit_command_ir(RemoteCommand.VOLUME_INCREASE), cron, trigger_end)


if __name__ == '__main__':

    schedule_jobs()

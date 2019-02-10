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
    # TODO: consider read quiet_times from a json file
    quiet_times = [
        QuietTime(datetime.time(hour=13, minute=1, second=0), datetime.time(hour=13, minute=2, second=0)),
        QuietTime(datetime.time(hour=13, minute=3, second=0), datetime.time(hour=13, minute=4, second=0)),
        QuietTime(datetime.time(hour=13, minute=5, second=0), datetime.time(hour=13, minute=6, second=0)),
        QuietTime(datetime.time(hour=13, minute=7, second=0), datetime.time(hour=13, minute=8, second=0)),
        QuietTime(datetime.time(hour=13, minute=9, second=0), datetime.time(hour=13, minute=10, second=0))
    ]

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
                          day_of_week='mon-sat',
                          hour=quiet_time.start.hour, minute=quiet_time.start.minute, second=quiet_time.start.second,
                          args=[RemoteCommand.VOLUME_DECREASE])
        scheduler.add_job(transmit_command_ir, cron,
                          day_of_week='mon-sat',
                          hour=quiet_time.end.hour, minute=quiet_time.end.minute, second=quiet_time.end.second,
                          args=[RemoteCommand.VOLUME_INCREASE])


if __name__ == '__main__':

    schedule_jobs()

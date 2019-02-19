#!/usr/bin/env/python3

# Potential alternatives:
# Use cron, available on Raspberry Pi Raspbian Linux don't need to worry about Windows
# flask-apscheduler adds support for flask context but I think that's not needed here
# https://apscheduler.readthedocs.io/en/latest/userguide.html
from apscheduler.schedulers.background import BackgroundScheduler

from remote_command import RemoteCommand
from ir_remote import transmit_command_ir
import quiet_times

cron = 'cron'
day_of_week = 'mon-sun'


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
    times = quiet_times.get_quiet_times('./data/quiet_times.json')

    # add_jobs_volume(times, scheduler)
    add_jobs_mute(times, scheduler)


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

        # add time + timedelta
        quiet_time_end = quiet_time.start + quiet_time.duration

        scheduler.add_job(transmit_command_ir, cron,
                          day_of_week=day_of_week,
                          hour=quiet_time_end.hour, minute=quiet_time_end.minute, second=quiet_time_end.second,
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

        # add time + timedelta
        quiet_time_end = quiet_time.start + quiet_time.duration
        scheduler.add_job(transmit_command_ir, cron,
                          day_of_week=day_of_week,
                          hour=quiet_time_end.hour, minute=quiet_time_end.minute, second=quiet_time_end.second,
                          args=[RemoteCommand.MUTE])


if __name__ == '__main__':

    # from command line, python scheduler.py will run schedule, won't run Flask service
    schedule_jobs()

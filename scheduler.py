#!/usr/bin/env/python3

# Potential alternatives:
# Use cron, available on Raspberry Pi Raspbian Linux don't need to worry about Windows
# flask-apscheduler adds support for flask context but I think that's not needed here
# https://github.com/agronholm/apscheduler/blob/master/docs/userguide.rst

# from apscheduler.scheduler import Scheduler
# from collections import namedtuple
# from remote_command import RemoteCommand
# from ir_remote import transmit_command_ir
#
# """ Calls remote control functions based on time of day
# """
#
# QuietTime = namedtuple('QuietTime', 'start stop')
#
#
# def build_schedule():
#
#     quiet_times = [QuietTime("10:01", "10:02"),
#                    QuietTime("18:01", "18:02")
#                    ]
#
#     for quiet_time in quiet_times:
#
#         # TODO: consider implement weekdays
#         # https://github.com/dbader/schedule/issues/249
#         schedule.every().day.at(quiet_time.start).do(transmit_command_ir(RemoteCommand.VOLUME_DECREASE))
#         schedule.every().day.at(quiet_time.end).do(transmit_command_ir(RemoteCommand.VOLUME_INCREASE))
#
#
# if __name__ == '__main__':
#
#     build_schedule()
#
#     # TODO: consider avoid blocking main thread
#     # See: How to continuously run the scheduler without blocking the main thread? run_continuously()
#     # https://schedule.readthedocs.io/en/stable/faq.html#how-to-continuously-run-the-scheduler-without-blocking-the-main-thread
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


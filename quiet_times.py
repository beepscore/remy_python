#!/usr/bin/env/python3

import json
import datetime

from collections import namedtuple

# start is datetime.time, duration is datetime.timedelta
QuietTime = namedtuple('QuietTime', 'start duration')


def get_quiet_times(filename):
    """
    reads a json text file of the form
    [
        {"start": {"hour": 17, "minute": 17, "second": 0}, "duration": {"minutes": 3, "seconds": 0}},
        {"start": {"hour": 17, "minute": 27, "second": 0}, "duration": {"minutes": 4, "seconds": 0}},
    ]
    :param filename: a string, e.g. './data/quiet_times.json'
    :return: a list of QuietTime
    """
    with open(filename, 'r') as f:
        quiet_times_from_json = json.load(f)

    # list comprehension
    quiet_times = [quiet_time_from_dict(x) for x in quiet_times_from_json]
    return quiet_times


def quiet_time_from_dict(quiet_time_dict):
    """
    :param quiet_time_dict: a dictionary of the form
    {"start": {"hour": 17, "minute": 27, "second": 0}, "duration": {"minutes": 3, "seconds": 0}}
    :return: a QuietTime
    """
    start_dict = quiet_time_dict.get("start")
    duration_dict = quiet_time_dict.get("duration")

    start_time = time_from_dict(start_dict)
    duration_timedelta = timedelta_from_dict(duration_dict)

    quiet_time = QuietTime(start_time, duration_timedelta)
    return quiet_time


def time_from_dict(time_dict):
    """
    :param time_dict: a dictionary of the form
    {"hour": 17, "minute": 27, "second": 0}
    Keys are singular similar to datetime.time parameters.
    :return: a datetime.time
    """
    # datetime.time: An idealized time, independent of any particular day
    hour = time_dict.get("hour")
    minute = time_dict.get("minute")
    second = time_dict.get("second")
    date_time_time = datetime.time(hour=hour, minute=minute, second=second)
    return date_time_time


def timedelta_from_dict(timedelta_dict):
    """
    :param timedelta_dict: a dictionary of the form
    {"hours": 0, "minutes": 3, "seconds": 30}.
    Keys are plural similar to datetime.timedelta parameters.
    Each key is optional.
    :return: a datetime.timedelta
    """
    hours = timedelta_dict.get("hours") if timedelta_dict.get("hours") is not None else 0
    minutes = timedelta_dict.get("minutes") if timedelta_dict.get("minutes") is not None else 0
    seconds = timedelta_dict.get("seconds") if timedelta_dict.get("seconds") is not None else 0
    date_time_timedelta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return date_time_timedelta


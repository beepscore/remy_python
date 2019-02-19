#!/usr/bin/env/python3

import json
import datetime

from collections import namedtuple

QuietTime = namedtuple('QuietTime', 'start end')


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

    # list comprehension
    quiet_times = [quiet_time_from_dict(x) for x in quiet_times_from_json]
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


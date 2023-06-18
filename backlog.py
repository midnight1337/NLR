"""
Author: Kamil Koltowski
Date: 2022-07-28
Description: This file provides a backlog decorator, it's used to track and save particular methods flow (pass/fail).
"""
import hashdata
import functools
import datetime


def backlog(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        with open(f"{hashdata.PATH_TO_BACKLOG}", "a") as file:
            result = method(*args, **kwargs)
            file.write(f"[{date}]\n{result}\n")
        file.close()
        return result
    return wrapper

"""
Class: Notifier
Author: Kamil Koltowski
Date: 2022-05-05
Description: This class provides ability to run windows toast notifier.
"""
import win10toast
import hashdata


class Notifier(object):
    def __init__(self):
        self.__notify: win10toast.ToastNotifier = win10toast.ToastNotifier()
        self.__title: str = "NLR"

    def run_notify(self, message):
        self.__notify.show_toast(
            title=self.__title,
            msg=message,
            icon_path=hashdata.PATH_TO_ICON_ICO,
            duration=15,
            threaded=True
        )

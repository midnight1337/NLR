"""
Author: Kamil Koltowski
Date: 2023-01-04
Description: This file contains confidential data necessary for proper operation of the tool, passwords, users, remote paths etc.
"""
import os


CONTACT = "Kamil Koltowski"
URL = "https://github.com/midnight1337"
VERSION = "1.0.0"

NLR_PATH = rf"C:\Users\{os.getlogin()}\Documents\NLR\\"
USER_DESKTOP_DIRECTORY = rf"C:\Users\{os.getlogin()}\Desktop\\"
PATH_TO_BACKLOG = rf"C:\Users\{os.getlogin()}\Documents\NLR\backlog.txt"
PATH_TO_ICON_PNG = rf"C:\Users\{os.getlogin()}\Documents\NLR\icon.png"
PATH_TO_ICON_ICO = rf"C:\Users\{os.getlogin()}\Documents\NLR\icon.ico"
DATABASE_FILE_PATH = rf"C:\Users\{os.getlogin()}\Documents\NLR\local_database.txt"
MOBA_DATABASE_FILE_PATH = rf"C:\Users\{os.getlogin()}\Documents\MobaXterm\MobaXterm.ini"

WELCOME_TEXT = f"Hi {os.getlogin()}, welcome in NLR.\nSelect your test line."

TEXT = "NLR is a tool that purpose is to automate manual log collection.\n" \
       "It provides logging into SSH servers, running logs and watch logging data of\n" \
       "PID, size, time and status in real time.\n" \
       "Tool is based on SSH library and threads running in background." \
       "\n\n"

import sys
import os
import datetime


def initialrun():
    """This function checks if the program is run for the first time"""
    logfilepath = os.path.join(os.getcwd(),"access.log")
    if not os.path.isfile(logfilepath):
        logfile = open(logfilepath,"x")
        logfile.write("The application is created and the log file made on {}".format(datetime.datetime.now()))
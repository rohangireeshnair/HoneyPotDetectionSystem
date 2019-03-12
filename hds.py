import sys
import os
import datetime

import argumentparser


def initialrun():
    """This function checks if the program is run for the first time"""
    logfilepath = os.path.join(os.getcwd(),"access.log")
    if not os.path.isfile(logfilepath):
        logfile = open(logfilepath,"x")
        logfile.write("The application is created and the log file made on {}".format(datetime.datetime.now()))

def main():
    parser = argumentparser.parsing()
    args = parser.parse_known_args()
    if args is not None:
        print("In main")
    else:
        sys.exit("No valid arguments specified")

if __name__ == '__main__':
    print("The application is now running....")
    main()
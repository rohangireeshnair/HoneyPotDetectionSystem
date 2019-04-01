import sys
import os
import datetime
import ipaddress
import argumentparser
from portscan.basicportscan import PortScan


def initialrun():
    """This function checks if the program is run for the first time"""
    logfilepath = os.path.join(os.getcwd(),"access.log")
    if not os.path.isfile(logfilepath):
        logfile = open(logfilepath,"x")
        logfile.write("The application is created and the log file made on {}".format(datetime.datetime.now()))

def main():
    parser = argumentparser.parsing()
    args = parser.parse_args()
    if args is not None:
        try:
            ipaddr = ipaddress.ip_address(args.target)
            ipaddrstr = args.target
            prtscan = PortScan(target=ipaddrstr,portrange=args.portrange,osscan=args.osscan,synscan=args.synscan,verbose=args.verbose)
        except ValueError:
            sys.exit("Invalid IP Address entered. \nProgram now exiting")
if __name__ == '__main__':
    main()
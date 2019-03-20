import sys
import nmap
import os

try:
    # import nmap
    print()
except ImportError:
    sys.exit("Install nmap python module. \nProgram exiting")


class PortScan:


    def __init__(self, target, portrange, osscan, synscan, verbose):
        self.target = target
        self.portrange = portrange
        self.osscan = osscan
        self.synscan = synscan
        self.verbose = verbose
        self.openport_tcp = []
        self.openport_udp = []

        nmapscnr = nmap.PortScanner()
        arg = None
        if synscan and osscan:
            arg = '-sS -sU -O'
        elif not synscan and osscan:
            arg = '-sT -sU -O'
        elif synscan and not osscan:
            arg = '-sS -sU'
        else:
            arg = '-sT -sU'
        if synscan or osscan:
            if os.getuid()!= 0:
                sys.exit("Root privilages required!!. Program now exiting")
        nmapscnr.scan(hosts=self.target, ports=self.portrange, arguments=arg)
        portstart = str(self.portrange).split("-")[0]
        portstart=int(portstart)
        portstop = str(self.portrange).split("-")[1]
        portstop=int(portstop)

        for x in range(portstart, portstop+1):
            por = nmapscnr[target].tcp(x)
            if por['state'] == 'open':
                self.openport_tcp.append(por)
        for x in range(portstart, portstop+1):
            por = nmapscnr[target].udp(x)
            if por['state'] == 'open':
                self.openport_udp.append(por)

    def otcpports(self):
        return self.openport_tcp
    def oudpposrts(self):
        return self.openport_udp
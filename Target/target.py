import sys
import nmap
import os
import logging

logger = logging.getLogger(__name__)

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
        self.tcpbanner = {}
        self.udpbanner = {}

        self.nmapscnr = nmap.PortScanner()
        arg = None
        if synscan:
            arg = '-sS -O'
        else:
            arg = '-sT -O'
        if os.getuid()!= 0:
                sys.exit("Root privilages required!!. Program now exiting")
        self.nmapscnr.scan(hosts=self.target, ports=self.portrange, arguments=arg)
        portstart = str(self.portrange).split("-")[0]
        portstart=int(portstart)
        portstop = str(self.portrange).split("-")[1]
        portstop=int(portstop)

        self.openport_tcp = self.nmapscnr[target]['tcp']
        self.openport_udp = self.nmapscnr[target]['udp']

    def otcpports(self):
        return self.openport_tcp
    def oudpports(self):
        return self.openport_udp

    def get_service(self,service,protocol):
        result = {}
        if protocol=='tcp':
            ports = self.otcpports()
        elif protocol=='udp':
            ports = self.oudpports()
        for port , attr in ports.items():
            if attr['name']==service:
                result[str(port)]=attr
        return result
    def get_os_info(self):
        osresult = []
        try:
            osresult.append(self.nmapscnr[self.target]['osmatch'][0]['osclass'][1]['osfamily'])
        except (IndexError, KeyError):
            logger.info("First OS try failed")

        try:
            osresult.append(self.nmapscnr[self.target]['osmatch'][1]['osclass'][0]['osfamily'])
        except (IndexError, KeyError):
            logger.info("Second OS try failed")
        if len(osresult)>=1:
            return osresult
        else:
            return -1
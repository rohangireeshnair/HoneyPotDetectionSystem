import sys
import nmap
import os
import logging
import urllib
import socket

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
        self.websites = []
        self.css = []


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
    def get_target_website(self):
        result = self.get_service('http', 'tcp')
        for target_port in result:
            try:

                request = urllib.request.urlopen('http://' + self.target + ':' + str(target_port) + '/',
                                                 timeout=5)

                if request.headers.get_content_charset() is None:
                    content = request.read()
                else:
                    content = request.read().decode(request.headers.get_content_charset())

                self.websites.append(content)

            except Exception as e:
                logger.info("Failed to fetch the web data")
        return self.websites

    def get_web_css(self):
        result = self.get_service('http', 'tcp')
        for target_port in result:
            try:
                request = urllib.request.urlopen('http://' + self.ip + ':' + str(target_port) + '/style.css',
                                                 timeout=5)

                if request.headers.get_content_charset() is None:
                    content = request.read()
                else:
                    content = request.read().decode(request.headers.get_content_charset())

                self.css.append(content)

            except Exception as e:
                logger.info("Failed to fetch the stylesheet")

            return self.css

        def get_banner(self, port, protocol='tcp'):

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)

            try:
                s.connect((self.address, port))
                recv = s.recv(1024)
            except socket.error as e:
                raise Exception("Banner grab failed for port", port, e)

             return recv
import sys
import socket
import logging
from Target.target import PortScan

def bannergrab(targetobj, ipadr):
    tcpports=targetobj.otcpports()
    udpports=targetobj.oudpports()
    for port in tcpports:
        ban = tcpbannergrab(ipadr, port)
        if ban:
            targetobj.tcpbanner[port]=ban

def tcpbannergrab(ipadr,port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ipadr,int(port)))
        banner = sock.recv(1024)
        return banner.decode()
    except (UnicodeDecodeError):
        logging.debug("Decode failed for port number {}".format(port))
    except ConnectionError:
        logging.debug("Connection to port {} refused".format(port))
import argparse
def parsing():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",help="To mention the target system to be scanned", type=str)
    parser.add_argument("-v","--verbose",help="To print the output on screent regarding background processes",action="store_true")
    parser.add_argument("-p","--portrange",help="To define the port range on the target machine to be scanned", type=str)
    parser.add_argument("-o", "--osscan", help="To enable operating system scan on the target(Requires escalated privilages)", action="store_true")
    parser.add_argument("-s", "--synscan", help="To initiate syn scan on the target system to detect open ports(Requires higher privilages)", action="store_true")
    return parser

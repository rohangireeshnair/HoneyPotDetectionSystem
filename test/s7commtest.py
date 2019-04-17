from support.s7comm_client import s7
from test.test import Test
import time
from support.s7comm_client import S7ProtocolError
import logging

logger = logging.getLogger(__name__)

class s7commtest(Test):
    s7client = None
    t_ip = None
    t_port = None
    src_tsaps = (0x100, 0x200)
    dst_tsaps = (0x102, 0x200, 0x201)
    src_tsap = None
    dst_tsap = None

    def __init__(self, target_obj):
        super(target_obj)
        self.t_ip = self.target.target
        self.t_port = self.target.get_ports(service='iso-tsap', protocol='tcp')
        self.s7client = s7(ip=self.t_ip, port=self.t_port)
        self.set_test_name("S7commServiceTest")
        self.get_test_description("This test checks for the authenticity of implementation pf the S7 server on the target machine provided.")
        # TODO implement imp_value

    def initialize_test(self):
        logger.info("Performing s7 connection")
        c_flag=False
        for src_tsap in self.src_tsaps:
            for des_tsap in self.dst_tsaps:
                try:
                    self.s7client.src_tsap= src_tsap
                    self.s7client.dst_tsap = des_tsap
                    self.s7client.Connect()
                    c_flag=True
                    self.src_tsap = src_tsap
                    self.dst_tsap = des_tsap
                    break
                except S7ProtocolError:
                    continue
        if not c_flag:
            result = "UNABLE"
            report = "{}:Unable to obtain s7comm connection with the server. Could be a different protocol server running on port 102.".format(self.get_test_name())
            self.set_test_status(result, report)
            logger.info("Unable to connect to s7 server. Brute of tsaps failed.")
            return
        elif c_flag:
            logger.info("Successfully Connected to s7 server.")
            time.sleep(10)
            tuple1 = (17,17,17,28,28,28,28,28,28,28,28,28,28,28)
            tuple2 = (1,6,7,1,2,3,4,5,6,7,8,9,10,11)
            count1 = 0
            count2 = 0

            data =self.s7client.GetIdentity(self.t_ip, self.t_port, self.src_tsap, self.dst_tsap)
            if data:
                for line in data:
                    try:
                        sec, item, val = line.split(";")
                        if not(sec==str(tuple1[count1]) and item == str(tuple2[count2]) and len(val)>0):
                            raise Exception
                    except Exception:
                        result = "FAIL"
                        report = "{}:S7comm test failed as the values returned by the server are not complete. Could be a honeypot machine. Data recieved: {}.".format(
                            self.get_test_name(), data)
                        self.set_test_status(result, report)
                        logger.info("S7comm test failed")
                        return
                result = "PASS"
                report = "{}:Test successfully passed ".format(self.get_test_name())
                self.set_test_status(result, report)
                logger.info("S7comm test passed")
                return
            if not data:
                result = "FAIL"
                report = "{}:Failed as server couldn't deliver data of the PLC. Could be a honeypot machine.".format(self.get_test_name())
                self.set_test_status(result, report)
                logger.info("S7comm test failed as the server did not send PLC data")
                return
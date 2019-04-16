from test.test import Test

import logging
from Target.target import Target
logger=logging.getLogger(__name__)

class OsCombinationTest(Test):
    combination_dict = { ('Mac OS X'):"MacOS",
                         ('iOS'):"MacOS",
                         ('OS X'):"MacOS",
                         ("Windows"):"Windows",
                         ("Linux"): "Linux"

    }
    primary_os_family = None

    def __init__(self, target_obj):
        super(target_obj)
        self.set_test_name("OsCombinationTest")
        self.get_test_description("This test checks for discrepancies in "
                                  "         1. The possibility of OSFamily returned by the Nmap scan"
                                  "         2. The services running on the Target System")
        #TODO implement imp_value

    def initialize_test(self):
        target_os_result = self.target.get_os_info()
        if(target_os_result==(-1)):
            result = "UNABLE"
            report = "Unable to perform {}. Reason:Nmap was unable to retrieve OS information from the target.".format(self.get_test_name())
            self.set_test_status(result, report)
            logger.info("Unable to perform {}".format(self.get_test_name()))
            return
        elif(len(target_os_result>=2)):
            for osfamily in target_os_result:
                if osfamily in self.combination_dict.keys():
                    if self.primary_os_family == None:
                        self.primary_os_family=self.combination_dict[osfamily]
                    elif self.primary_os_family==self.combination_dict[osfamily]:
                        result = "PASS"
                        report = "{}: Succesfully passed. OSFamily returned by NMAP matches and is {}".format(self.get_test_name(),self.primary_os_family )
                        self.set_test_status(result, report)
                        logger.debug("{} Successfully passed".format(self.get_test_name()))
                        return
                    elif self.primary_os_family != self.combination_dict[osfamily]:
                        result ="FAIL"
                        report ="{}: Failed as the OSFamily returned by NMAP does not match. {} and {}".format(self.get_test_name(), self.primary_os_family, osfamily)
                        self.set_test_status(result, report)
                        logger.debug("{} Failed".format(self.get_test_name()))
                        return
                else:
                    result = "UNABLE"
                    report = "Unable to perform {}. Reason:The detected OSFamily not defined in databse. OSFamily:{}".format(self.get_test_name(), osfamily)
                    self.set_test_status(result, report)
                    logger.info("Unable to perform {}".format(self.get_test_name()))
                    return
        elif(len(target_os_result)==1):
            result = "UNABLE"
            report = "Unable to perform {}. Reason:Single OSFamily Possibility detected. OSFamily:{}".format(
                self.get_test_name(), target_os_result[0])
            self.set_test_status(result, report)
            logger.info("Unable to perform {}".format(self.get_test_name()))
            return
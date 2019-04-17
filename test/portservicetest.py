from test.test import Test

import logging
from Target.target import Target
logger=logging.getLogger(__name__)

class PortServiceTest(Test):
    dict1 = {}
    dict2 = {}
    dict3 = {}
    dict4 = {}

    primary_os_family = None

    def __init__ (self, target_obj):
        super(target_obj)
        self.set_test_name("PortServiceTest")
        self.get_test_description("Check for the conflicts between services running on different ports and the platform which is being used")


    def initialize_test(self):
        get_services = self.target.get_services()

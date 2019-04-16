from Target.target import Target

class Test:
    target = None
    imp_val = None
    test_name = None
    test_result = None
    test_report = None
    test_descrip = None

    status_dict = {
        "PASS":0,
        "FAIL":1,
        "NA":0,
        "UNABLE":0

    }

    def __init__(self, target_obj):
        assert isinstance(target_obj, Target)
        self.target = target_obj


    def set_imp_val(self, val):
        self.imp_val = val
    def set_test_name(self, name):
        self.test_name = name
    def set_test_status(self, result, report ):

        assert result in self.status_dict.keys()
        self.test_result =result
        self.test_report = report
        self.target.set_pos_point(self.target.get_pos_point()+self.imp_val*self.status_dict[result])

    def get_test_result(self):
        return self.test_result

    def get_test_report(self):
        return self.test_report

    def get_test_name(self):
        return self.test_name

    def get_test_description(self):
        return self.test_descrip
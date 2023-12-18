from check_registers import test_check_register_code, test_register_reg_code
from test_login import test_login
from registration_test import test_registration


def run_test():
    test_check_register_code()
    test_registration()
    test_login()
    test_register_reg_code()


if __name__ == "__main__":
    run_test()

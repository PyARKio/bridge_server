# -- coding: utf-8 --
from __future__ import unicode_literals
from drivers.log_settings import log
from helpers import Exceptions
from helpers import decorators
import types


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


# ***** Test Part ***********************************************
import unittest


class CalcTest(unittest.TestCase):
    def test_none(self):
        self.assertTrue(ip_len('1254345.12.12.12h'))

# ***************************************************************


# ********* CHECK IP ***************
@decorators.check_types_bool
def ip(response: str):
    log.info('response: {}'.format(response))

    try:
        result = ip_max(ip_ever_segments(ip_digit(ip_len(response))))

    except Exceptions.FailCheckStr as err:
        log.error(err)
    except Exceptions.FailCheckLenIP as err:
        log.error(err)
    except Exceptions.FailCheckDigitIP as err:
        log.error(err)
    except Exception as err:
        log.error(err)
    else:
        log.info(result)
        return result
    return False


@decorators.check_ip_len
def ip_len(object_to_check: str):
    return object_to_check


@decorators.check_ip_digit
def ip_digit(object_to_check: str):
    return object_to_check


@decorators.check_ip_ever_segments
def ip_ever_segments(object_to_check: str):
    return object_to_check


@decorators.check_ip_max
def ip_max(object_to_check: str):
    return object_to_check


# ******** CHECK PORT *************
@decorators.check_types_bool
def port(response: int):
    log.info('response: {}'.format(response))

    try:
        result = maximum_value(subtraction_sign(response))

    except Exceptions.FailCheckInt as err:
        log.error(err)
    except Exceptions.FailCheckMaxValue as err:
        log.error(err)
    except Exceptions.FailCheckErrSign as err:
        log.error(err)
    except Exception as err:
        log.error(err)
    else:
        log.info(result)
        return result
    return False


@decorators.check_maximum_value
def maximum_value(object_to_check: int):
    return object_to_check


@decorators.check_subtraction_sign
def subtraction_sign(object_to_check: int):
    return object_to_check


# ********* CHECK CALLBACK ************
@decorators.check_types_bool
def callback_func(object_to_check: types.FunctionType):
    return object_to_check


# ********* CHECK WORDS ************
@decorators.check_types_bool
def words(response: dict):
    return response


# ********* CHECK RUN TIMER ************
@decorators.check_types_bool
def runner(object_to_check: bool):
    return True


if __name__ == '__main__':
    unittest.main()



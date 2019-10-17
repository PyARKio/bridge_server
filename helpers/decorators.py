# -- coding: utf-8 --
from __future__ import unicode_literals
from drivers.log_settings import log
from helpers import Exceptions
import inspect
import types
import time


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


# ***** Test Part ***********************************************
import unittest


class CalcTest(unittest.TestCase):
    def test_none(self):
        print(check_ip_arg_raise())

# ***************************************************************


# ********* CHECK IP ***************
def check_ip_arg_raise(f_object=None):
    def _f(*object_to_check):
        log.info('{}, args: {}'.format(f_object, *object_to_check))
        # This part of function need for check input parameter that to ensure the safe execution of the function
        for index, argument in enumerate(inspect.getfullargspec(f_object)[0]):
            if not isinstance(object_to_check[index], f_object.__annotations__[argument]):
                raise Exceptions.FailCheckStr('object_to_check <{}> must be <str> type'.format(*object_to_check))
        log.info('Function: {}, Status: OK'.format(f_object.__name__))
        return f_object(*object_to_check)
    return _f


def check_ip_len(f_object=None):
    def _f(object_to_check):
        log.info('{}, args: {}'.format(f_object, object_to_check))
        try:
            sample = object_to_check.split('.')
        except Exception as err:
            log.error(err)
            raise err
        if len(sample) != 4:
            raise Exceptions.FailCheckLenIP('len({}) must be 4'.format(object_to_check))
        log.info('Function: {}, Status: OK'.format(f_object.__name__))
        return f_object(object_to_check)
    return _f


def check_ip_digit(f_object=None):
    def _f(object_to_check):
        log.info('{}, args: {}'.format(f_object, object_to_check))
        if not ''.join(object_to_check.split('.')).isdigit():
            raise Exceptions.FailCheckDigitIP('{} should contain numbers and dots'.format(object_to_check))
        log.info('Function: {}, Status: OK'.format(f_object.__name__))
        return f_object(object_to_check)
    return _f


def check_ip_ever_segments(f_object=None):
    def _f(object_to_check):
        log.info('{}, args: {}'.format(f_object, object_to_check))
        for segment in object_to_check.split('.'):
            if len(segment) > 3:
                raise Exceptions.FailCheckDigitIP('Every segment must consist of from one to three digits')
        log.info('Function: {}, Status: OK'.format(f_object.__name__))
        return f_object(object_to_check)
    return _f


def check_ip_max(f_object=None):
    def _f(object_to_check):
        log.info('{}, args: {}'.format(f_object, object_to_check))
        for segment in object_to_check.split('.'):
            if int(segment) > 255:
                raise Exceptions.FailCheckDigitIP('Oops :)')
        log.info('Function: {}, Status: OK'.format(f_object.__name__))
        return f_object(object_to_check)
    return _f


# ******** CHECK PORT *************
def check_maximum_value(f_object=None):
    def _f(object_to_check):
        log.info('{}, args: {}'.format(f_object, object_to_check))
        if object_to_check > 65536:
            raise Exceptions.FailCheckMaxValue('Oops :)')
        log.info('Function: {}, Status: OK'.format(f_object.__name__))
        return f_object(object_to_check)
    return _f


def check_subtraction_sign(f_object=None):
    def _f(object_to_check):
        log.info('{}, args: {}'.format(f_object, object_to_check))
        if object_to_check < 0:
            raise Exceptions.FailCheckErrSign('Oops :)')
        log.info('Function: {}, Status: OK'.format(f_object.__name__))
        return f_object(object_to_check)
    return _f


# ******** TOOLS *************
def check_types_bool(f_object=None):
    def _f(*object_to_check):
        log.info('{}, args: {}'.format(f_object, *object_to_check))
        # This part of function need for check input parameter that to ensure the safe execution of the function
        for index, argument in enumerate(inspect.getfullargspec(f_object)[0]):
            if object_to_check[index] is not None:
                if not isinstance(object_to_check[index], f_object.__annotations__[argument]):
                    log.error('object_to_check <{}> must be {f} type'.format(*object_to_check,
                                                                             f=f_object.__annotations__[argument]))
                    return False
            else:
                log.error('object_to_check <{}> is <None> type'.format(*object_to_check))
                return True
        log.info('Function: {}, Status: OK'.format(f_object.__name__))
        return f_object(*object_to_check)
    return _f


def update_time(f_object=None):
    def _f(*object_to_check):
        log.info('{}, args: {}'.format(f_object, object_to_check))
        log.info('STATUS: {}, TIME: {}'.format(object_to_check[1].status, object_to_check[1].time))
        object_to_check[1].time = time.time()
        log.info('STATUS: {}, TIME: {}'.format(object_to_check[1].status, object_to_check[1].time))
        return f_object(*object_to_check)
    return _f


if __name__ == '__main__':
    unittest.main()



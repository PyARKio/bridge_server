# -- coding: utf-8 --
from __future__ import unicode_literals


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


class FailCheckSession(BaseException):
    pass


class FailCheckNone(BaseException):
    pass


class FailCheckList(BaseException):
    pass


class FailCheckStr(BaseException):
    pass


class FailCheckLenIP(BaseException):
    pass


class FailCheckDigitIP(BaseException):
    pass


class FailCheckArgs(BaseException):
    pass


class FailCheckInt(BaseException):
    pass


class FailCheckMaxValue(BaseException):
    pass


class FailCheckErrSign(BaseException):
    pass


class FailCheckFuncTypes(BaseException):
    pass


class FailCheckServerArgs(BaseException):
    pass





# -- coding: utf-8 --
from __future__ import unicode_literals
import logging
import logging.handlers
import traceback


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


trace_pattern = logging.Formatter("[%(asctime)s] %(levelname)s %(module)s:%(lineno)d:%(funcName)s: %(message)s")

# file_handler = logging.handlers.RotatingFileHandler('/home/user/check_battery.log', 'a', 10 * 1024 * 1024, 10)
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(trace_pattern)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(trace_pattern)

log = logging.getLogger()
log.setLevel(logging.DEBUG)
# log.addHandler(file_handler)
log.addHandler(stream_handler)



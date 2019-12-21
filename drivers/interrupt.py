# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
import time
from drivers.log_settings import log


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


def func(data):
    print(data)


class Interrupt(threading.Thread):
    def __init__(self, callback_handler, periodic):
        threading.Thread.__init__(self)
        self._running = True
        self.__handler = callback_handler
        self.__time = periodic
        self._pause = False

    def terminate(self):
        self._running = False
        log.debug('self._running: {}'.format(self._running))

    def go_go(self):
        self._running = True
        self.start()

    def run(self):
        while self._running:
            time.sleep(self.__time)
            if not self._pause:
                self.__handler()
        log.debug('TIMER STOP !!!')


if __name__ == '__main__':
    i = Interrupt(func, 10)
    i.go_go()
    time.sleep(15)
    i.terminate()



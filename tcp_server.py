# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
import socket
import time
from datetime import datetime
from multiprocessing import Queue
from drivers.log_settings import log
from drivers.interrupt import Interrupt
from helpers import Exceptions
from helpers import checkers
import AssistantBot
from read_mac import get_mac


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"

# my_ip = socket.gethostbyname_ex(socket.gethostname())  # [2][0]
# log.info(my_ip)


class CommonQueue:
    CQ = Queue()
    SysCQ = Queue()


class Thread4Server(threading.Thread):
    def __init__(self, ip=None, _port=None, data_cb=None, sys_cb=None,
                 word_for_check_new_acceptance={'request': None, 'response': None}, _run_timer=False):
        """

        :param ip:
        :param port:
        :param callback:
        :param word_for_check_new_acceptance: must be list type with 2 include, for example, ['request', 'response']
        :return:
        """
        if not self._check_args(ip, _port, data_cb, sys_cb, word_for_check_new_acceptance, _run_timer):
            log.error(Exceptions.FailCheckServerArgs('Oops :) Some args are incorrect'))
            raise Exceptions.FailCheckServerArgs('Oops :) Some args are incorrect')

        self.sock = None
        self.ip = ip
        self.port = _port
        self.data_callback = data_cb
        self.sys_callback = sys_cb
        self.is_check_new_acceptance = word_for_check_new_acceptance

        threading.Thread.__init__(self)

        self.flag_run = False
        self.info = dict()
        self.queue_handlers = {'acceptance': self.accept_handler,
                               'accept error': self.accept_error_handler,
                               'speak': self.speak_handler,
                               'speak error': self.speak_error_handler,
                               'control': self.cmd_handler
                               }

        self.acceptThread = Thread4Accept()
        self.speakThread = dict()

        if _run_timer:
            self.timer = Interrupt(callback_handler=self.callback_for_timer, periodic=1)
            # self.timer.go_go()

    def callback_for_timer(self):
        keys = self.speakThread.keys()
        # log.info(keys)

        for key in keys:
            if time.time() - self.speakThread[key].time > 15 and self.speakThread[key].status and self.speakThread[key].ping:
                log.info('send PING {} {}'.format(self.speakThread[key].time, time.time()))
                self.speakThread[key].ping = False
                Thread4Server._send(whom=self.speakThread[key].connection, what='Ping')
                if self.sys_callback:
                    self.sys_callback('SEND TO CLIENT <{}> TEST PING at {} ({})'.
                                      format(key, time.time(), datetime.now()))
                else:
                    self.data_callback('SEND TO CLIENT <{}> TEST PING at {} ({})'.
                                       format(key, time.time(), datetime.now()))
            elif time.time() - self.speakThread[key].time > 40 and self.speakThread[key].status and not self.speakThread[key].ping:
                log.info('DETECT LOST CONNECTION {} {}'.format(self.speakThread[key].time, time.time()))
                self.speakThread[key].status = False
                if self.sys_callback:
                    self.sys_callback('LOST <{}> at {} ({})'.format(key, time.time(), datetime.now()))
                else:
                    self.data_callback('LOST <{}> at {} ({})'.format(key, time.time(), datetime.now()))

    @staticmethod
    def _check_args(ip, _port, data_callback, sys_callback, word_for_check_new_acceptance, _run_timer):
        if checkers.ip(ip) and \
                checkers.port(_port) and \
                checkers.callback_func(data_callback) and \
                checkers.callback_func(sys_callback) and \
                checkers.words(word_for_check_new_acceptance) and \
                checkers.runner(_run_timer):
            log.info('GOOD')
            return True
        else:
            log.info('BAD')
            return False

    @staticmethod
    def _send(whom, what):
        try:
            whom.send(bytes(str(what) + '\r\n', encoding='UTF-8'))
        except Exception as err:
            log.error(err)

    @staticmethod
    def _get_key(response):
        return list(response.keys())

    def _init_tcp_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.ip, self.port))
        except Exception as err:
            log.error(err)
            # raise err
            return False
        else:
            self.sock.listen(10)
            self.sock.setblocking(False)
            self.sock.settimeout(1)
            log.info('server start. ip: {} port: {}'.format(self.ip, self.port))
            self.acceptThread.sock = self.sock
            self.acceptThread.start()
            self.timer.go_go()
            self.flag_run = True

    def run(self):
        self._init_tcp_server()
        while self.flag_run:
            response = CommonQueue.CQ.get()
            log.info(response)
            if not isinstance(response, dict):
                log.error('<{}> must be <dict> type. <{}>'.format(response, type(response)))

            elif self._get_key(response)[0] in self._get_key(self.queue_handlers):
                self.queue_handlers[self._get_key(response)[0]](response[self._get_key(response)[0]])

    def accept_error_handler(self, string_err):
        log.error(string_err)
        self.sys_callback(str(string_err))

    def accept_handler(self, value):
        self.sys_callback(str(value))
        log.info('Connecting to {}'.format(value['address']))
        self.speakThread[value['address']] = Thread4Speak(connection=value['connection'], address=value['address'])
        self.speakThread[value['address']].start()

        if self.is_check_new_acceptance['request']:
            log.info('send CHECK')
            Thread4Server._send(whom=self.speakThread[value['address']].connection,
                                what=self.is_check_new_acceptance['request'])
        else:
            self.speakThread[value['address']].certificate = True

        log.debug(self.speakThread)
        log.info('Number of active clients: {}'.format(len(self.speakThread)))

    # TESTING IT !!!
    def speak_error_handler(self, string_err):
        self.sys_callback(str(string_err))
        log.info('{} from {}'.format(string_err['string'], string_err['who']))
        self.speakThread.pop(string_err['who'])
        log.info(self.speakThread)

    def speak_handler(self, string):
        log.info(string)
        if self._check_new_client(string):
            self._check_to_find(self.speakThread[string['who']])
            self._routing_data(string)

    # NOT FINISHED !!!!  ADD CHECKERS AND LOGIC
    def cmd_handler(self, value):
        log.debug(value)
        self.acceptThread.flag_run = False
        self.timer.terminate()
        self.flag_run = False

        log.debug(self.speakThread)
        for key in list(self.speakThread.keys()):
            log.debug(self.speakThread[key])
            self.speakThread[key].flag_run = False
            self.speakThread[key].close()
            self.speakThread.pop(key)
        log.debug(self.speakThread)
        self.sock.close()  # .shutdown(socket.SHUT_RDWR)

    # ******************** CHECK NEW CLIENT ****************************
    def _check_new_client(self, string):
        if not self.speakThread[string['who']].certificate and self.is_check_new_acceptance['response']:
            log.info('certificate: {}, check response: {}, state: 1'.format(self.speakThread[string['who']].certificate,
                                                                            self.is_check_new_acceptance['response']))
            if string['string'] == self.is_check_new_acceptance['response']:
                self.speakThread[string['who']].certificate = True
                if self.sys_callback:
                    self.sys_callback('NEW CLIENT <{}> at {} ({})'.format(string['who'], time.time(), datetime.now()))
                else:
                    self.data_callback('NEW CLIENT <{}> at {} ({})'.format(string['who'], time.time(), datetime.now()))
                log.info('certificate: {}'.format(self.speakThread[string['who']].certificate))
            else:
                log.info('something Oops!')
                log.info('RECEIVE STRING: {receive}, '
                         'WAIT STRING: {wait}'.format(receive=string['string'],
                                                      wait=self.is_check_new_acceptance['response']))
                log.debug(self.speakThread)
                self.speakThread[string['who']].flag_run = False
                self.speakThread[string['who']].close()
                self.speakThread.pop(string['who'])
                log.debug(self.speakThread)
                return False
        elif not self.speakThread[string['who']].certificate:
            log.info('certificate: {}, check response: {}, state: 2'.format(self.speakThread[string['who']].certificate,
                                                                            self.is_check_new_acceptance['response']))
            self.speakThread[string['who']].certificate = True
            if self.sys_callback:
                self.sys_callback('NEW CLIENT <{}> at {} ({})'.format(string['who'], time.time(), datetime.now()))
            else:
                self.data_callback('NEW CLIENT <{}> at {} ({})'.format(string['who'], time.time(), datetime.now()))
            log.info('certificate: {}'.format(self.speakThread[string['who']].certificate))
        return True

    # ******************** CHECK TO FIND CLIENT ************************
    def _check_to_find(self, _client):
        if not _client.status:
            _client.status = True
            _client.ping = True
            if self.sys_callback:
                self.sys_callback('FIND CLIENT <{}> at {} ({})'.format(_client.address, time.time(), datetime.now()))
            else:
                self.data_callback('FIND CLIENT <{}> at {} ({})'.format(_client.address, time.time(), datetime.now()))
            log.info('FIND {}'.format(_client.address))
        elif not _client.ping:
            _client.ping = True
            if self.sys_callback:
                self.sys_callback('RECEIVE FROM CLIENT <{}> TEST PING at {} ({})'.
                                  format(_client.address, time.time(), datetime.now()))
            else:
                self.data_callback('RECEIVE FROM CLIENT <{}> TEST PING at {} ({})'.
                                   format(_client.address, time.time(), datetime.now()))

    # ******************** ROUTING DATA ********************************
    def _routing_data(self, string):
        if self.data_callback:
            log.info('data_callback: {}'.format(self.data_callback))
            self.data_callback(string['string'])
            Thread4Server._send(whom=self.speakThread[string['who']].connection, what='READY TO NEXT')
            log.info(self.speakThread[string['who']].time)
        else:
            log.debug('from {} response {}'.format(string['who'], string['string']))


class Thread4Speak(threading.Thread):
    def __init__(self, connection=None, address=None):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.certificate = False
        self.status = True
        self.time = time.time()
        self.ping = True
        self.flag_run = True

    def __del__(self):
        log.debug('DELETED {}'.format(self.address))

    def run(self):
        log.info('start for {}'.format(self.address))
        while self.flag_run:
            try:
                log.debug('start listen')
                data = self.connection.recv(10000)
                log.debug('stop listen {}'.format(data))
            except Exception as err:
                log.error('{}\nfrom {}'.format(err, self.address))
                if self.flag_run:
                    CommonQueue.CQ.put({'speak error': {'string': err, 'who': self.address}})
                self.flag_run = False
                self.close()
            else:
                if not data:
                    log.error('No data from {}'.format(self.address))
                    if self.flag_run:
                        CommonQueue.CQ.put({'speak error': {'string': 'No data', 'who': self.address}})
                    self.flag_run = False
                    self.close()
                else:
                    if self.flag_run:
                        # CommonQueue.CQ.put({'speak': {'string': data.decode('cp1251'),
                        #                               'who': self.address,
                        #                               'certificate': self.certificate,
                        #                               'status': self.status,
                        #                               'time': self.time,
                        #                               'ping': self.ping
                        #                               }
                        #                     })
                        self.time = time.time()
                        CommonQueue.CQ.put({'speak': {'string': data.decode('cp1251'),
                                                      'who': self.address,
                                                      'time': self.time,
                                                      'date': datetime.now()
                                                      }
                                            })

    def close(self):
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
        except Exception as err:
            log.error('{}\nfrom {}'.format(err, self.address))
        else:
            log.info('Closed connection for {address}'.format(address=self.address))


class Thread4Accept(threading.Thread):
    # Need to identity new connection
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = None
        self.flag_run = True

    def run(self):
        while self.flag_run:
            try:
                __connection, __address = self.sock.accept()
                log.info("Connection from: " + str(__address))
            except socket.timeout:
                pass
            except Exception as __err:
                CommonQueue.CQ.put({'accept error': __err})
            else:
                CommonQueue.CQ.put({'acceptance': {'connection': __connection, 'address': __address}})
        log.info('SHUTDOWN')


def test_call(response):
    # save in db, for example
    log.info(response)


def system_call(response):
    log.info(response)
    AssistantBot.CommonQueue.CQ.put(response, block=False)


if __name__ == '__main__':
    assistant_start = threading.Thread(target=AssistantBot.on)
    assistant_start.start()

    start_ip = 0
    while not start_ip:
        net_data = get_mac('ifconfig')
        log.debug(net_data)

        if 'VPN' in net_data.keys():
            start_ip = net_data['VPN']['VPN IP']

            serverThread = Thread4Server(ip=start_ip, _port=777,
                                         word_for_check_new_acceptance={'request': 'check', 'response': 'check ok'},
                                         data_cb=test_call, sys_cb=system_call,
                                         _run_timer=True)
            serverThread.start()
        else:
            time.sleep(3)
    log.debug('GO TO ANOTHER WHILE !!!')
    while True:
        net_data = get_mac('ifconfig')
        log.debug(net_data)

        if 'VPN' in net_data.keys():
            if net_data['VPN']['VPN IP'] != start_ip:
                log.debug('RESTART SERVER !!!')
                log.debug(net_data)
                start_ip = net_data['VPN']['VPN IP']

                CommonQueue.CQ.put({'control': 'shutdown'})
                while serverThread.is_alive():
                    time.sleep(2)
                del(serverThread)
                # time.sleep(3)

                serverThread = Thread4Server(ip=start_ip, _port=777,
                                             word_for_check_new_acceptance={'request': 'check', 'response': 'check ok'},
                                             data_cb=test_call, sys_cb=system_call,
                                             _run_timer=True)
                serverThread.start()

        time.sleep(3)
        # cmd = input('-> ')
        # CommonQueue.CQ.put({'control': cmd})







# -- coding: utf-8 --
from __future__ import unicode_literals
import sys
import subprocess
import platform


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


def get_mac(cmd):
    result = dict()
    response = read_mac(cmd=cmd)
    response_strings = parse(response)

    for i in response_strings:
        # print(i)
        if 'enp3s0' in i:
            result['Ethernet'] = find_eth1(i)
        elif 'eth1' in i:
            result['Ethernet'] = find_eth1(i)
        elif 'wlan0' in i:
            # print(i)
            result['WiFi'] = find_wlan0(i)
        elif 'tun0' in i:
            result['VPN'] = find_tun0(i)

    return result


def parse(response):
    string = list()
    number_segment = 0
    string.append(str())
    for number, line in enumerate(response.stdout):
        if '\n' == line.decode():
            number_segment += 1
            string.append(str())
        else:
            string[number_segment] += line.decode()
    # print(len(string))
    return string


def read_mac(cmd):
    try:
        response = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    except Exception as err:
        print(err)
        sys.exit(0)
    else:
        return response


def find_eth1(data):
    if platform.node() == 'qwerty' and platform.processor() == 'x86_64':
        if 'inet ' in data:
            return {'Ethernet MAC': data.split('ether ')[1].split('  txqueuelen')[0],
                    'Ethernet IP': data.split('inet ')[1].split('  netmask ')[0]}
    elif platform.node() == 'pine64so' and platform.processor() == 'aarch64':
        if 'HWaddr' in data:
            return {'Ethernet MAC': data.split('HWaddr ')[1].split('  \n')[0],
                    'Ethernet IP': data.split('inet addr:')[1].split('  Bcast:')[0]}
    return None


def find_wlan0(data):
    if platform.node() == 'qwerty' and platform.processor() == 'x86_64':
        pass
    elif platform.node() == 'pine64so' and platform.processor() == 'aarch64':
        if 'HWaddr' in data:
            return {'WiFi MAC': data.split('HWaddr ')[1].split('  \n')[0],
                    'WiFi IP': data.split('inet addr:')[1].split('  Bcast:')[0]}
    return None


def find_tun0(data):
    if platform.node() == 'qwerty' and platform.processor() == 'x86_64':
        if 'inet ' in data:
            return {'VPN IP': data.split('inet ')[1].split('  netmask ')[0]}
    elif platform.node() == 'pine64so' and platform.processor() == 'aarch64':
        if 'inet addr:' in data:
            return {'VPN IP': data.split('inet addr:')[1].split('  P-t-P:')[0]}
    return None


if __name__ == '__main__':
    print(get_mac('ifconfig'))





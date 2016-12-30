#!/usr/bin/env python3

import urllib.request
import subprocess


def get_ip_list(url):
    raw_file = urllib.request.urlopen(url).read().decode()
    raw_list = raw_file.split('\n')
    ipv4_list = list(filter(lambda x: x[9:13] == 'ipv4', raw_list[:-1]))
    ipv4_cn_list = list(filter(lambda x: x[6:8] == 'CN', ipv4_list))
    ipv4_cn_ip_list = []
    for i in ipv4_cn_list:
        ipv4_cn_ip_list.append(i.split('|')[3] + ',' + i.split('|')[4])
    return ipv4_cn_ip_list


def add_mask(ip_raw_list):
    mask_dic = {'256': '/24', '512': '/23', '1024': '/22', '2048': '/21', '4096': '/20', '8192': '/19', '16384': '/18',
                '32768': '/17', '65536': '/16', '131072': '/15', '262144': '/14', '524288': '/13', '1048576': '/12',
                '2097152': '/11', '4194304': '/10'}
    for i,k in enumerate(ip_raw_list):
        ip_and_mask = k.split(',')
        ip_raw_list[i] = ip_and_mask[0] + mask_dic[ip_and_mask[1]]
    return ip_raw_list


def add_routing(route_list, gateway):
    try:
        count = 0
        for i in route_list:
            subprocess.check_output(['route', 'add', i, gateway])
            count += 1
        print("{} routes have been successful injected".format(count))
    except:
        print("Error")


def del_routing(route_list):
    try:
        count = 0
        for i in route_list:
            subprocess.check_output(['route', 'delete', i])
            count += 1
        print("{} routes have been successful deleted".format(count))
    except:
        print("Error")


def main():
    url = 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    gateway = '10.0.2.1'
    choice = input("Do you want to add[A] routes or delete[D] them?: ")
    if choice.lower() == 'a':
        add_routing(add_mask(get_ip_list(url)), gateway)
    else:
        del_routing(add_mask(get_ip_list(url)))


if __name__ == '__main__':
    main()

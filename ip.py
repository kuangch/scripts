#!/usr/bin/env python2.7
# encoding: utf-8
# Copyright (c) 2018 Dilusense Inc. All Rights Reserved.


"""=======================================

    company : Dilusense
     author : Kuangch
       date : 2018/7/23

======================================="""

import sys
import os
import platform
import commands


def changeNetwork(ip='10.0.1.10', gateway='10.0.1.1', netmask='255.255.255.0', device='eth0'):
    """
    change the network of the system
    """
    if(is_ip_visitable(ip)):
        print 'ip conflict!'
        return -1

    platform = getPlatform()

    if platform == "centos":
        path = "/etc/sysconfig/network-scripts/ifcfg-" + str(device)
        file_handler = open(path, "r")
        network_content = file_handler.read()
        file_handler.close()
        conte = "IPADDR=%s\nNETMASK=%s\nGATEWAY=%s\n" % (ip, netmask, gateway)
        num = network_content.find("IPADDR")
        if num != -1:
            network_content = network_content[:num] + conte
            file_handler = open(path, "w")
            file_handler.write(network_content)
            file_handler.close()
    elif platform == "ubuntu":
        path = "/etc/network/interfaces"
        file_handler = open(path, "r")
        network_interfaces = file_handler.read()
        file_handler.close()
        network_content = network_interfaces.split("auto")
        has_device = False
        for i in network_content:
            if device in i:
                content = " %s\niface %s inet static\naddress %s\nnetmask %s\ngateway %s\n" % (
                device, device, ip, netmask, gateway)
                network_interfaces = network_interfaces.replace(i, content)
                has_device = True
                break

        if not has_device:
            content = "\nauto %s\niface %s inet static\naddress %s\nnetmask %s\ngateway %s\n" % (
            device, device, ip, netmask, gateway)
            network_interfaces = network_interfaces + content
        file_handler = open(path, "w")
        file_handler.write(network_interfaces)
        file_handler.close()
    result = commands.getoutput("sudo ifdown %s && sudo ifup %s" % (device, device))
    print 'change network ' + ('success' if result == '' else 'failed')
    return result == ''

def is_ip_visitable(host):
    """
    检测ip地址是否已存在
    """
    if platform.system() == 'Windows':
        ret = os.system('ping -n 1 -w 1000 ' + host)  # 0=>成功
    elif platform.system() == 'Linux':
        ret = os.system('ping -c1 -w1000 ' + host)  # 0=>成功
    return ret == 0

def getPlatform():
    """
    get the platform of the system
    """
    try:
        platForm = platform.platform().lower()
        if "ubuntu" in platForm:
            print platForm
            return "ubuntu"
        elif "centos" in platForm:
            print platForm
            return "centos"
    except:
        print "unknow os..."
        return None


if __name__ == "__main__":
    """"
    @param: <ip>,<gateway>,<netmask>,<device>
    """
    ip = sys.argv[1]
    try:
        gateway = sys.argv[2]
        netmask = sys.argv[3]
        device = sys.argv[4]
    except:
        gateway = None
        netmask = None
        device = None

    if gateway is None:
        print 'is ip visitable: %s' % is_ip_visitable(ip)
    else:
        print 'change network: %s' % changeNetwork(ip=ip, gateway=gateway, netmask=netmask, device=device)
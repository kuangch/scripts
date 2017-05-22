#!/usr/bin/env python2.7
# encoding: utf-8
# Copyright (c) 2016 Dilusense Inc. All Rights Reserved.
import os
import time
import threadpool


def ping(ips, prefix, ip):
    if os.system('ping -n 1 -w 1 ' + prefix + str(ip)) == 0:
        ips.append(prefix + str(ip))


def writeIP2file(ips):
    ips_file = open('ips.list', 'w')

    ips_line = ''
    for ip in ips:
        ips_line = ips_line + ip + '\n'

    ips_file.write(ips_line)

if __name__ == '__main__':


    start = time.time()
    prefix = '10.0.1.'
    ips = []

    # execute task by multi-thread
    pool = threadpool.ThreadPool(50)
    params = []
    for i in range(255):
        params.append(([ips,prefix,i],None))
    requests = threadpool.makeRequests(ping,params)
    [pool.putRequest(req) for req in requests]
    pool.wait()

    # sort
    ips = sorted(ips, key=lambda ip: int(ip[len(prefix):]))
    for ip in ips:
        print ip

    writeIP2file(ips)
    print '>>> pass ip total: ' + str(len(ips)) + ''
    print '>>> use time: ' + str(time.time() - start) + 's'


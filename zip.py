#!/usr/bin/env python2.7
# encoding: utf-8
# Copyright (c) 2016 Dilusense Inc. All Rights Reserved.

"""a file for deployment automatically"""
import zipfile
import os
import re

import sys
import time


def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, 'w', zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        # print arcname
        zf.write(tar, arcname)
    zf.close()

def zip_dir_log(dirname, project_name,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, 'w', zipfile.zlib.DEFLATED)

    filelist.append(dirname + os.sep + project_name + os.sep + 'log' + os.sep)

    for tar in filelist:
        arcname = tar[len(dirname):]
        # print arcname
        zf.write(tar, arcname)
    zf.close()


def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.mkdir(unziptodir, 0777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')

        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir): os.mkdir(ext_dir, 0777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()


def main(argv):
    project_name = 'multi_info_portal'
    path = 'K:\zip\multi_info_portal_cache'

    curr_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    os.system('cp -r ' + project_name + ' '+path + os.sep + project_name)

    zip_dir_log(path + os.sep + project_name,
                project_name,
                path + os.sep + 'deploy/deploy/' + project_name + '.zip')
    zip_dir(path + os.sep + 'deploy',
            path + os.sep + 'zip' + os.sep + project_name + os.sep + project_name + os.sep + 'deploy.zip')
    zip_dir(path + os.sep + 'zip' + os.sep + project_name,
            path + os.sep + 'zip' + os.sep + project_name + '_' + curr_time + '.zip')


if __name__ == '__main__':
    main(argv=sys.argv)

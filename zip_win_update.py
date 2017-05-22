#!/usr/bin/env python2.7
# encoding: utf-8
# Copyright (c) 2016 Dilusense Inc. All Rights Reserved.

"""a file for deployment automatically"""
import zipfile
import shutil
import os
import re

import sys
import time

def remove_dir(path):
    if os.path.exists(path) is True:
        print('exist path %s deleting...' % (str(path)))
        shutil.rmtree(path)
        print('deleted path %s success' % (str(path)))



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

def zip_dir_with_empty_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

            for dir in dirs:
                if len(os.listdir(os.path.join(root, dir))) == 0:
                    filelist.append(os.path.join(root, dir))

    zf = zipfile.ZipFile(zipfilename, 'w', zipfile.zlib.DEFLATED)

    for tar in filelist:
        arcname = tar[len(dirname):]
        # print arcname
        zf.write(tar, arcname)
    zf.close()


def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.makedirs(unziptodir, 0777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')

        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir): os.makedirs(ext_dir, 0777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()


def main(argv):
    project_name = 'multi_info_portal'
    project_dir = os.environ['HOME'] + os.sep + 'build' + os.sep + project_name + os.sep + project_name
    path = 'K:\zip\multi_info_portal_cache'
    update_pkg_dir = path + os.sep + 'update_win'
    project_cache = path + os.sep + project_name

    curr_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    export_zip_file = path + os.sep + 'zip' + os.sep + project_name + '_win_update_' + curr_time + '.zip'
    update_zip_file = path + os.sep + 'zip' + os.sep + project_name + '_win_update' + os.sep + 'update_win.zip'

    remove_dir(project_cache + os.sep + project_name)
    shutil.copytree(project_dir, project_cache + os.sep + project_name)

    zip_dir_with_empty_dir(project_cache, update_pkg_dir + os.sep + project_name + '.zip')
    zip_dir_with_empty_dir(update_pkg_dir, update_zip_file)
    zip_dir_with_empty_dir(path + os.sep + 'zip' + os.sep + project_name + '_win_update', export_zip_file)


if __name__ == '__main__':
    main(argv=sys.argv)

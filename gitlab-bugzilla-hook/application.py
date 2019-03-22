#!/usr/bin/python
# encoding: utf-8

from flask import Flask
from extensions import my_webhook
import json
import requests
import logging
import logging.config

bug_api = "xxxxx"
bug_url = "http://ip:port/rest.cgi/bug/"
bug_is_private = False
logging.config.fileConfig("config/logger.conf")
logger = logging.getLogger("app")


def is_number(uchar):
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    return False


def some_function(request):
    data = json.loads(request.data)
    logger.debug("+++++++++++++++++++++++++++++++++++++++")
    kind = data.get('object_kind')
    if kind == 'push':
        logger.debug("pushevent received: %s " % request.data)
        ref = data.get('ref')
        project = data.get('project')
        project_id = data.get('project_id');
        branch_name = ref[ref.rfind("/") + 1:]

        url = "http://10.0.1.80/api/v4/projects/" + bytes(project_id) + "/protected_branches"
        headers = {"PRIVATE-TOKEN": "xxxxx"}
        r = requests.get(url, params={}, headers=headers);
        be_protected = False;
        for p in r.json():
            if branch_name == p['name']:
                be_protected = True;
                break;

        if be_protected:
            logger.debug(" protected OK")
        else:
            logger.debug("the ref is not protected,not update the bugzilla info")
            return

        weburl = ""
        if not project is None:
            weburl = project.get('web_url')
        commits = data.get('commits')
        logger.debug("commits: %s " % commits)
        if not commits is None:
            update_info = {}
            for commit in commits:
                if not commit is None:
                    message = commit.get('message')
                    user_name = commit.get('user_name')
                    urlval = commit.get('url')
                    bugid = '2132'
                    bugcomment = ""
                    if -1 == message.find('desc'):
                        bugid = message
                    else:
                        bugid = message[0:message.find('desc')].replace("bug id:", "").replace(" ", "").replace("\n",
                                                                                                                "");
                        bugcomment = 'Comments:\n' + 'Author: ' + user_name + '\n' + message[message.find('desc'):] + '\n' + urlval + '\n'

                    bugids = []

                    # 多个bug id
                    try:
                        if ',' in bugid:
                            bugids = bugid.split(',')
                        else:
                            bugids.append(bugid)
                    except:
                        logger.debug('pares bug id error')
                    for bugid in bugids:
                        if is_number(bugid):
                            if update_info.get(bugid) is None:
                                update_info[bugid] = bugcomment
                            else:
                                update_info[bugid] = update_info[bugid] + bugcomment
                            logger.debug("update: %s " % update_info)

            for key, values in update_info.items():
                dataJson = {"ids": [key], "comment": {"body": values, "is_private": bug_is_private}, "api_key": bug_api}
                headers = {
                    'accept': "application/json",
                    'content-type': "application/json"
                }
                ret = requests.request("PUT", bug_url + key, data=json.dumps(dataJson), headers=headers)
                logger.debug("Bugzilla API RET: %s " % ret.json())
        logger.debug("<<<<<<<<<<<<<<<<<<<<<<<<Webhook DONE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


def some_other_function(request):
    print "some_other"


def create_app():
    app = Flask(__name__)
    my_webhook.add_route('/something', methods=['GET', 'POST'])
    my_webhook.handlers['action1'] = some_function
    my_webhook.init_app(app)
    return app

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import importlib

from airflow import configuration
from airflow.utils.log.logging_mixin import LoggingMixin

import requests
import json


def dingbot_msg_sender(msg):
    log = LoggingMixin().log
    bot_url = configuration.get('dingding', 'DING_BOT_URL')
    headers = {'Content-Type': 'application/json'}

    md_text = {
        "title": "AIRFLOW ERROR",
        "text": msg
    }
    print(msg)
    post_data = {
        "msgtype": "markdown",
        "markdown": md_text
    }
    print(post_data)
    r = requests.post(bot_url, headers=headers,data=json.dumps(post_data))
    print(r)
    with open('/usr/local/airflow/logs/ali_phone_call.log', 'a') as the_file:
        the_file.write('1\n')
    log.info("Sent an alert message to dingding.....")   

def ding_bot_backend(msg):
    """
    Send ding message using backend specified in DING_BOT_BACKEND
    :param msg:
    :return:
    """
    path, attr = configuration.get('dingbot', 'DING_BOT_BACKEND').rsplit('.', 1)
    module = importlib.import_module(path)
    backend = getattr(module, attr)
    return backend(msg)

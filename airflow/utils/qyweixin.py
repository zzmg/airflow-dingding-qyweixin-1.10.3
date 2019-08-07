from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import importlib

from airflow import configuration
from airflow.utils.log.logging_mixin import LoggingMixin

import requests
import json


def qyweixin_msg_sender(msg):
    log = LoggingMixin().log
    bot_url = configuration.get('qyweixin','QYWEIXIN_BOT_URL')
    headers = {'Content-Type': 'application/json'}

    md_text = {
        "title": "AIRFLOW ERROR",
        "text": msg
    }

    post_data = {
        "msgtype": "markdown",
            "markdown": {
                "content": md_text
    }
    
    r = requests.post(bot_url, headers=headers,data=json.dumps(post_data))
    print(r)
    log.info("Sent an alert message to qyweixin.....")
def qiyeweixin_bot_backend(msg):
    """
    Send qyweixin message using backend specified in QYWEIXIN_BOT_BACKEND
    :param msg:
    :return: airflow.utils.qyweixin.qyweixin_msg_sender
    """
    path, attr = configuration.get('qyweixinbot','QYWEIXIN_BOT_BACKEND').rsplit('.', 1)
    module = importlib.import_module(path)
    backend = getattr(module, attr)
    return backend(msg)
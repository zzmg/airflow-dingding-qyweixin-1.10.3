import importlib
from airflow import configuration

import requests
import json
import urllib3
urllib3.disable_warnings()

def qyweixin_msg_sender(msg):
    bot_url = configuration.get('qyweixin','QYWEIXIN_BOT_URL')
    headers = {'Content-Type': 'application/json'}

    md_text = {
        "title": "AIRFLOW ERROR",
        "text": msg
    }

    post_data = {
        "msgtype": "markdown",
        "content": md_text
    }

    r = requests.post(bot_url, headers=headers,data=json.dumps(post_data))

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
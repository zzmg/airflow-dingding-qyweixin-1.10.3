import importlib
from airflow import configuration

import requests
import json
import urllib3
urllib3.disable_warnings()

def dingbot_msg_sender(msg):
    bot_url = configuration.get('dingding', 'DING_BOT_URL')
    headers = {'Content-Type': 'application/json'}

    md_text = {
        "title": "AIRFLOW ERROR",
        "text": msg
    }

    post_data = {
        "msgtype": "markdown",
        "markdown": md_text
    }

    r = requests.post(bot_url, headers=headers,data=json.dumps(post_data))
    with open('/usr/local/airflow/logs/ali_phone_call.log', 'a') as the_file:
        the_file.write('1\n')


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

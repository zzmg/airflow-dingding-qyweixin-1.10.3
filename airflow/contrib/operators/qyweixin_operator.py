# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from airflow.contrib.hooks.qyweixin_hook import QyweixinHook
from airflow.operators.bash_operator import BaseOperator
from airflow.utils.decorators import apply_defaults


class QyweixinOperator(BaseOperator):
    """
    This operator allows you send qyweixin message using qyweixin custom bot.
    Get qyweixin token from conn_id.password. And prefer set domain to
    conn_id.host, if not will use default ``https://oapi.dingtalk.com``.

    For more detail message in
    `qyweixin custom bot <https://open-doc.dingtalk.com/microapp/serverapi2/qf2nxq>`_

    :param qyweixin_conn_id: The name of the qyweixin connection to use
    :type qyweixin_conn_id: str
    :param message_type: Message type you want to send to qyweixin, support five type so far
        including text, link, markdown, actionCard, feedCard
    :type message_type: str
    :param message: The message send to qyweixin chat group
    :type message: str or dict
    :param at_mobiles: Remind specific users with this message
    :type at_mobiles: list[str]
    :param at_all: Remind all people in group or not. If True, will overwrite ``at_mobiles``
    :type at_all: bool
    """
    template_fields = ('message',)
    ui_color = '#4ea4d4'  # qyweixin icon color

    @apply_defaults
    def __init__(self,
                 qyweixin_conn_id='qyweixin_default',
                 message_type='text',
                 message=None,
                 mentioned_list=None,
                 mentioned_mobile_list=None,
                 *args,
                 **kwargs):
        super(QyweixinOperator, self).__init__(*args, **kwargs)
        self.qyweixin_conn_id = qyweixin_conn_id
        self.message_type = message_type
        self.message = message
        self.mentioned_list = mentioned_list
        self.mentioned_mobile_list = mentioned_mobile_list

    def execute(self, context):
        self.log.info('Sending qyweixin message.')
        hook = QyweixinHook(
            self.qyweixin_conn_id,
            self.message_type,
            self.message,
            self.mentioned_list,
            self.mentioned_mobile_list
        )
        hook.send()

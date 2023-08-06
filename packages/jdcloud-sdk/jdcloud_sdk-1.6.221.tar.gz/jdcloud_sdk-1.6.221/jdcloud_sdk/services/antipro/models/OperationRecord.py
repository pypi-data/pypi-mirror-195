# coding=utf8

# Copyright 2018 JDCLOUD.COM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTE: This class is auto generated by the jdcloud code generator program.


class OperationRecord(object):

    def __init__(self, time=None, name=None, action=None, info=None, operator=None):
        """
        :param time: (Optional) 操作时间
        :param name: (Optional) 防护包名称
        :param action: (Optional) 操作类型.<br>- 1: 套餐变更<br>- 2: 防护规则变更<br>- 3: 防护对象变更<br>- 4: IP 地址变更<br>- 5: 防护包名称变更<br>- 6: IP地址库变更<br>- 7: 端口库变更<br>- 8: 访问控制规则变更
        :param info: (Optional) 操作详情
        :param operator: (Optional) 操作人
        """

        self.time = time
        self.name = name
        self.action = action
        self.info = info
        self.operator = operator

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


class ForbiddenStreamHistoryItem(object):

    def __init__(self, stream=None, app=None, publishIp=None, forbiddenType=None, ttl=None, startTime=None, endTime=None, forbiddenTypeDesc=None):
        """
        :param stream: (Optional) 禁播流
        :param app: (Optional) 封禁推流的app
        :param publishIp: (Optional) 封禁的IP
        :param forbiddenType: (Optional) 禁播类型:forever永不禁播limit限时禁播
        :param ttl: (Optional) 禁播时长
        :param startTime: (Optional) 开始禁播时间
        :param endTime: (Optional) 结束禁播时间
        :param forbiddenTypeDesc: (Optional) 禁播类型说明
        """

        self.stream = stream
        self.app = app
        self.publishIp = publishIp
        self.forbiddenType = forbiddenType
        self.ttl = ttl
        self.startTime = startTime
        self.endTime = endTime
        self.forbiddenTypeDesc = forbiddenTypeDesc

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

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class DeleteForbiddenInfoRequest(JDCloudRequest):
    """
    删除封禁信息
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DeleteForbiddenInfoRequest, self).__init__(
            '/forbiddenInfo:delete', 'POST', header, version)
        self.parameters = parameters


class DeleteForbiddenInfoParameters(object):

    def __init__(self,):
        """
        """

        self.forbiddenType = None
        self.forbiddenDomain = None
        self.forbiddenUrl = None
        self.shareCacheDomainFlag = None
        self.token = None

    def setForbiddenType(self, forbiddenType):
        """
        :param forbiddenType: (Optional) 封禁类型，domain 域名封禁,url url封禁
        """
        self.forbiddenType = forbiddenType

    def setForbiddenDomain(self, forbiddenDomain):
        """
        :param forbiddenDomain: (Optional) 封禁域名
        """
        self.forbiddenDomain = forbiddenDomain

    def setForbiddenUrl(self, forbiddenUrl):
        """
        :param forbiddenUrl: (Optional) 封禁url,多个以;隔开
        """
        self.forbiddenUrl = forbiddenUrl

    def setShareCacheDomainFlag(self, shareCacheDomainFlag):
        """
        :param shareCacheDomainFlag: (Optional) 是否同步操作共享缓存域名,0:仅操作本域名,1:同步操作共享缓存域名,默认为0
        """
        self.shareCacheDomainFlag = shareCacheDomainFlag

    def setToken(self, token):
        """
        :param token: (Optional) 用于封禁前缀识别的URL,应为单个特殊字符，如：~
        """
        self.token = token


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


class QueryForbiddenInfoListCommonRequest(JDCloudRequest):
    """
    查询封禁解封信息
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(QueryForbiddenInfoListCommonRequest, self).__init__(
            '/forbiddenInfoCommon:query', 'POST', header, version)
        self.parameters = parameters


class QueryForbiddenInfoListCommonParameters(object):

    def __init__(self,):
        """
        """

        self.queryDomain = None
        self.taskId = None
        self.forbiddenUrl = None
        self.pageNumber = None
        self.pageSize = None

    def setQueryDomain(self, queryDomain):
        """
        :param queryDomain: (Optional) 封禁域名.queryDomain和taskId至少传入一个
        """
        self.queryDomain = queryDomain

    def setTaskId(self, taskId):
        """
        :param taskId: (Optional) 任务id.queryDomain和taskId至少传入一个
        """
        self.taskId = taskId

    def setForbiddenUrl(self, forbiddenUrl):
        """
        :param forbiddenUrl: (Optional) 封禁url,精确查询
        """
        self.forbiddenUrl = forbiddenUrl

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码数
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 每页size
        """
        self.pageSize = pageSize


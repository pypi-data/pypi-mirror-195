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


class DescribeLogtopicsRequest(JDCloudRequest):
    """
    查询日志主题列表，支持按照名称模糊查询。
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeLogtopicsRequest, self).__init__(
            '/regions/{regionId}/logsets/{logsetUID}/logtopics', 'GET', header, version)
        self.parameters = parameters


class DescribeLogtopicsParameters(object):

    def __init__(self, regionId,logsetUID,):
        """
        :param regionId: 地域 Id
        :param logsetUID: 日志集 UID
        """

        self.regionId = regionId
        self.logsetUID = logsetUID
        self.pageNumber = None
        self.pageSize = None
        self.name = None
        self.appName = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 当前所在页，默认为1
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 页面大小，默认为20；取值范围[1, 100]
        """
        self.pageSize = pageSize

    def setName(self, name):
        """
        :param name: (Optional) 日志主题名称
        """
        self.name = name

    def setAppName(self, appName):
        """
        :param appName: (Optional) 日志主题采集的日志类型
        """
        self.appName = appName


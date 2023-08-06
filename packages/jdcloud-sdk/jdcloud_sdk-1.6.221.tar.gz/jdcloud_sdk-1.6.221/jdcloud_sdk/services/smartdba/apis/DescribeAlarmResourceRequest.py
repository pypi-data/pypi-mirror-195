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


class DescribeAlarmResourceRequest(JDCloudRequest):
    """
    近一小时告警列表，按级别倒序
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(DescribeAlarmResourceRequest, self).__init__(
            '/regions/{regionId}/describeAlarmResource', 'GET', header, version)
        self.parameters = parameters


class DescribeAlarmResourceParameters(object):

    def __init__(self, regionId,endTime):
        """
        :param regionId: 地域代码
        :param endTime: null
        """

        self.regionId = regionId
        self.pageIndex = None
        self.pageSize = None
        self.dbType = None
        self.endTime = endTime

    def setPageIndex(self, pageIndex):
        """
        :param pageIndex: (Optional) 显示数据的页码，默认为1，取值范围：[-1,∞)
        """
        self.pageIndex = pageIndex

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 每页显示的数据条数，默认为10
        """
        self.pageSize = pageSize

    def setDbType(self, dbType):
        """
        :param dbType: (Optional) 数据库类型，默认MySQL
        """
        self.dbType = dbType


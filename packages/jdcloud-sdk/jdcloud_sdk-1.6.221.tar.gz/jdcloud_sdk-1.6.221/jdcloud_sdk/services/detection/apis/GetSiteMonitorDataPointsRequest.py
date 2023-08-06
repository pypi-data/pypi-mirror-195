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


class GetSiteMonitorDataPointsRequest(JDCloudRequest):
    """
    获取站点监控数据
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(GetSiteMonitorDataPointsRequest, self).__init__(
            '/siteMonitorDataPoints', 'GET', header, version)
        self.parameters = parameters


class GetSiteMonitorDataPointsParameters(object):

    def __init__(self,):
        """
        """

        self.id = None
        self.startTime = None
        self.endTime = None

    def setId(self, id):
        """
        :param id: (Optional) 
        """
        self.id = id

    def setStartTime(self, startTime):
        """
        :param startTime: (Optional) 
        """
        self.startTime = startTime

    def setEndTime(self, endTime):
        """
        :param endTime: (Optional) 
        """
        self.endTime = endTime


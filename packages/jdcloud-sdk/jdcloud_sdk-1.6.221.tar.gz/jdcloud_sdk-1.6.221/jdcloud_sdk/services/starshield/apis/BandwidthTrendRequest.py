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


class BandwidthTrendRequest(JDCloudRequest):
    """
    按请求或响应带宽统计，返回日期直方图.
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(BandwidthTrendRequest, self).__init__(
            '/zones/{zone_identifier}/analytics$$bandwidthTrend', 'POST', header, version)
        self.parameters = parameters


class BandwidthTrendParameters(object):

    def __init__(self,zone_identifier, ):
        """
        :param zone_identifier: 
        """

        self.zone_identifier = zone_identifier
        self.zoneName = None
        self.since = None
        self.until = None
        self.direction = None

    def setZoneName(self, zoneName):
        """
        :param zoneName: (Optional) 
        """
        self.zoneName = zoneName

    def setSince(self, since):
        """
        :param since: (Optional) 
        """
        self.since = since

    def setUntil(self, until):
        """
        :param until: (Optional) 
        """
        self.until = until

    def setDirection(self, direction):
        """
        :param direction: (Optional) 
        """
        self.direction = direction


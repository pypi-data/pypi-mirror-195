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


class DescribeUrlRankingRequest(JDCloudRequest):
    """
    查询URL播放排行
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeUrlRankingRequest, self).__init__(
            '/describeUrlRanking', 'GET', header, version)
        self.parameters = parameters


class DescribeUrlRankingParameters(object):

    def __init__(self, domainName, startTime, ):
        """
        :param domainName: 播放域名
        :param startTime: 起始时间
- UTC时间
  格式:yyyy-MM-dd'T'HH:mm:ss'Z'
  示例:2018-10-21T10:00:00Z

        """

        self.domainName = domainName
        self.size = None
        self.rankfield = None
        self.startTime = startTime
        self.endTime = None

    def setSize(self, size):
        """
        :param size: (Optional) 查询Top数量，默认20，即返回Top20的数据
        """
        self.size = size

    def setRankfield(self, rankfield):
        """
        :param rankfield: (Optional) 排行依据字段，取值：["pv", "flow", "bandwidth"]，默认pv
- pv 播放次数
- flow 流量
- bandwidth 带宽

        """
        self.rankfield = rankfield

    def setEndTime(self, endTime):
        """
        :param endTime: (Optional) 结束时间:
- UTC时间
  格式:yyyy-MM-dd'T'HH:mm:ss'Z'
  示例:2018-10-21T10:00:00Z
- 为空,默认为当前时间

        """
        self.endTime = endTime


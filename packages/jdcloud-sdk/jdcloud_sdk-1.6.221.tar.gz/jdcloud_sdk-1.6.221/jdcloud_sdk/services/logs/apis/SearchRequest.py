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


class SearchRequest(JDCloudRequest):
    """
    搜索日志
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(SearchRequest, self).__init__(
            '/regions/{regionId}/logsets/{logsetUID}/logtopics/{logtopicUID}/search', 'GET', header, version)
        self.parameters = parameters


class SearchParameters(object):

    def __init__(self, regionId,logsetUID,logtopicUID,action, ):
        """
        :param regionId: 地域 Id
        :param logsetUID: 日志集ID
        :param logtopicUID: 日志主题ID
        :param action: "preview"表示预览, "fulltext"表示全文检索, "advance"表示按照搜索语句检索
        """

        self.regionId = regionId
        self.logsetUID = logsetUID
        self.logtopicUID = logtopicUID
        self.action = action
        self.expr = None
        self.caseSensitive = None
        self.startTime = None
        self.endTime = None
        self.pageNumber = None
        self.pageSize = None
        self.sort = None
        self.filters = None

    def setExpr(self, expr):
        """
        :param expr: (Optional) Base64编码的搜索表达式,
        """
        self.expr = expr

    def setCaseSensitive(self, caseSensitive):
        """
        :param caseSensitive: (Optional) 搜索关键字大小写敏感， 默认false
        """
        self.caseSensitive = caseSensitive

    def setStartTime(self, startTime):
        """
        :param startTime: (Optional) 开始时间。格式 “YYYY-MM-DDThh:mm:ssTZD”, 比如 “2018-11-09T15:34:46+0800”.当action != preview时，必填
        """
        self.startTime = startTime

    def setEndTime(self, endTime):
        """
        :param endTime: (Optional) 结束时间。格式 “YYYY-MM-DDThh:mm:ssTZD”, 比如 “2018-11-09T15:34:46+0800”.当action != preview时，必填
        """
        self.endTime = endTime

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页数。 最小为1，最大为99
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 每页个数。默认为10，最大100
        """
        self.pageSize = pageSize

    def setSort(self, sort):
        """
        :param sort: (Optional) 返回排序,不填或者为空，默认为desc，"asc":按照时间正序返回结果，"desc":按照时间倒序返回结果
        """
        self.sort = sort

    def setFilters(self, filters):
        """
        :param filters: (Optional) 指定返回字段，只对系统日志生效，不填默认按照产品线配置返回字段，Name支持：key，Values填入返回字段
        """
        self.filters = filters


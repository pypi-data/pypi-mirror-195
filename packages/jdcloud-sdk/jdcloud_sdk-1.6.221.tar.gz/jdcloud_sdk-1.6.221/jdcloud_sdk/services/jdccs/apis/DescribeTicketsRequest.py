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


class DescribeTicketsRequest(JDCloudRequest):
    """
    查询工单列表
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeTicketsRequest, self).__init__(
            '/tickets', 'GET', header, version)
        self.parameters = parameters


class DescribeTicketsParameters(object):

    def __init__(self, ):
        """
        """

        self.pageNumber = None
        self.pageSize = None
        self.type = None
        self.ticketTypeName = None
        self.status = None
        self.ticketNo = None
        self.ticketTemplateName = None
        self.description = None
        self.startTime = None
        self.endTime = None
        self.filters = None
        self.sorts = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码, 默认为1
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小，默认为20
        """
        self.pageSize = pageSize

    def setType(self, type):
        """
        :param type: (Optional) 工单TAB类型 pendingProcess:待我处理 pendingReview:待审核 processing:处理中 all:全部(默认)
        """
        self.type = type

    def setTicketTypeName(self, ticketTypeName):
        """
        :param ticketTypeName: (Optional) 工单类型
        """
        self.ticketTypeName = ticketTypeName

    def setStatus(self, status):
        """
        :param status: (Optional) 工单状态 pendingReview:待审核 revoked:已撤销 processing:处理中 pendingVerification:待核验 pendingClose:待关单 rejected:已拒绝 completed:已完成 cancelled:已取消 draft:草稿中
        """
        self.status = status

    def setTicketNo(self, ticketNo):
        """
        :param ticketNo: (Optional) 工单编号
        """
        self.ticketNo = ticketNo

    def setTicketTemplateName(self, ticketTemplateName):
        """
        :param ticketTemplateName: (Optional) 工单名称
        """
        self.ticketTemplateName = ticketTemplateName

    def setDescription(self, description):
        """
        :param description: (Optional) 描述
        """
        self.description = description

    def setStartTime(self, startTime):
        """
        :param startTime: (Optional) 创建开始时间，遵循ISO8601标准，使用UTC时间，格式为：yyyy-MM-ddTHH:mm:ssZ
        """
        self.startTime = startTime

    def setEndTime(self, endTime):
        """
        :param endTime: (Optional) 创建结束时间，遵循ISO8601标准，使用UTC时间，格式为：yyyy-MM-ddTHH:mm:ssZ
        """
        self.endTime = endTime

    def setFilters(self, filters):
        """
        :param filters: (Optional) ticketNo - 工单编号，精确匹配，支持多个

        """
        self.filters = filters

    def setSorts(self, sorts):
        """
        :param sorts: (Optional) createdTime - 创建时间 closedTime - 关闭时间
        """
        self.sorts = sorts


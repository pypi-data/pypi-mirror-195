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


class InstanceTemplateNetworkInterface(object):

    def __init__(self, subnetId, securityGroups=None, sanityCheck=None, ipv6AddressCount=None):
        """
        :param subnetId:  子网ID。
        :param securityGroups: (Optional) 安全组ID列表。
        :param sanityCheck: (Optional) PortSecurity，源和目标IP地址校验，取值为0或者1。
        :param ipv6AddressCount: (Optional) 自动分配的ipv6地址数量，取值范围[0,1]，默认为0
        """

        self.subnetId = subnetId
        self.securityGroups = securityGroups
        self.sanityCheck = sanityCheck
        self.ipv6AddressCount = ipv6AddressCount

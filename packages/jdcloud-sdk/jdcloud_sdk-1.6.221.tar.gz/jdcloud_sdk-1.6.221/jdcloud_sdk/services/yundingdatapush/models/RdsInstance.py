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


class RdsInstance(object):

    def __init__(self, instanceId=None, regionId=None, vpcId=None, vpcName=None, instanceName=None, instanceStatus=None, instanceType=None, instanceClass=None):
        """
        :param instanceId: (Optional) RDS实例ID
        :param regionId: (Optional) 地域
        :param vpcId: (Optional) 所属私有网络ID
        :param vpcName: (Optional) 所属私有网络名称
        :param instanceName: (Optional) RDS实例名称
        :param instanceStatus: (Optional) RDS实例状态
        :param instanceType: (Optional) RDS实例类型
        :param instanceClass: (Optional) RDS实例规格
        """

        self.instanceId = instanceId
        self.regionId = regionId
        self.vpcId = vpcId
        self.vpcName = vpcName
        self.instanceName = instanceName
        self.instanceStatus = instanceStatus
        self.instanceType = instanceType
        self.instanceClass = instanceClass

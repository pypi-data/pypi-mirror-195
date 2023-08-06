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


class DescribeThingModelRequest(JDCloudRequest):
    """
    根据物类型Code查看物模型完整信息
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(DescribeThingModelRequest, self).__init__(
            '/regions/{regionId}/coreinstances/{instanceId}/thingModel:describe', 'GET', header, version)
        self.parameters = parameters


class DescribeThingModelParameters(object):

    def __init__(self, regionId, instanceId, thingTypeCode, ):
        """
        :param regionId: 区域id
        :param instanceId: 实例Id
        :param thingTypeCode: 物类型Code
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.thingTypeCode = thingTypeCode
        self.thingModelVersion = None

    def setThingModelVersion(self, thingModelVersion):
        """
        :param thingModelVersion: (Optional) 版本号。如果为空，则返回最新版本
        """
        self.thingModelVersion = thingModelVersion


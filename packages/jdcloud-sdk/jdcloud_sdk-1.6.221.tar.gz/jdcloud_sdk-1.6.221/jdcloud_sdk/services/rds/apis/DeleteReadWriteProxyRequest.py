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


class DeleteReadWriteProxyRequest(JDCloudRequest):
    """
    删除RDS 实例的读写分离代理<br>- 仅支持MySQL
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DeleteReadWriteProxyRequest, self).__init__(
            '/regions/{regionId}/readWriteProxy/{readWriteProxyId}', 'DELETE', header, version)
        self.parameters = parameters


class DeleteReadWriteProxyParameters(object):

    def __init__(self, regionId, readWriteProxyId, ):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        :param readWriteProxyId: 读写分离代理服务ID
        """

        self.regionId = regionId
        self.readWriteProxyId = readWriteProxyId


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


class RebootPodRequest(JDCloudRequest):
    """
    重启实例的某类节点。重启采用滚动重启的方式，如果该类节点有多个，通常不会中断实例的服务。
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(RebootPodRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}:rebootpod', 'POST', header, version)
        self.parameters = parameters


class RebootPodParameters(object):

    def __init__(self,regionId, instanceId, nodeType):
        """
        :param regionId: 地域代码
        :param instanceId: 实例ID
        :param nodeType: 重启指定类型的pod,支持Tikv,TiDB,PD,TiFlash
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.nodeType = nodeType


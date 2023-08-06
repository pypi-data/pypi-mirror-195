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


class CheckPodNameRequest(JDCloudRequest):
    """
    podName 是否符合命名规范，以及查询指定 podName 区域内是否已经存在。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CheckPodNameRequest, self).__init__(
            '/regions/{regionId}/pods:checkPodName', 'POST', header, version)
        self.parameters = parameters


class CheckPodNameParameters(object):

    def __init__(self,regionId, podName, ):
        """
        :param regionId: Region ID
        :param podName: 用户定义的 pod 名称，符合 DNS-1123 subdomain 规范。
        """

        self.regionId = regionId
        self.podName = podName
        self.maxCount = None

    def setMaxCount(self, maxCount):
        """
        :param maxCount: (Optional) 需要创建的 pod 总数，默认创建一个，不同的总数会对校验结果产生影响。
        """
        self.maxCount = maxCount


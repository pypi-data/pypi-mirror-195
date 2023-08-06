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


class StopPrefetchTaskRequest(JDCloudRequest):
    """
    停止预热任务接口
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(StopPrefetchTaskRequest, self).__init__(
            '/prefetchTask:stop', 'POST', header, version)
        self.parameters = parameters


class StopPrefetchTaskParameters(object):

    def __init__(self,):
        """
        """

        self.urls = None
        self.region = None
        self.isp = None

    def setUrls(self, urls):
        """
        :param urls: (Optional) 待停止预热的url
        """
        self.urls = urls

    def setRegion(self, region):
        """
        :param region: (Optional) 地区[huabei huadong dongbei huazhong huanan xinan xibei gangaotai]中的一个
        """
        self.region = region

    def setIsp(self, isp):
        """
        :param isp: (Optional) 运营商[ct uni cm]中的一个,分别代表电信 联通 移动
        """
        self.isp = isp


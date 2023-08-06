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


class PurgeFilesByURLRequest(JDCloudRequest):
    """
    通过指定URL，从星盾的缓存中细化删除一个或多个文件。
要清除带有自定义缓存key的文件，请包括用于计算缓存key的报头。
例如要清除缓存key中含有${geo}或${devicetype}的文件，请包括CF-Device-Type或CF-IPCountry报头。
注意：当包含源报头时，请确保包括scheme协议和hostname主机名。如果是默认端口，可以省略端口号（http为80，https为443），否则必须包含端口号。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(PurgeFilesByURLRequest, self).__init__(
            '/zones/{identifier}/purge_cache__purgeFilesByURL', 'POST', header, version)
        self.parameters = parameters


class PurgeFilesByURLParameters(object):

    def __init__(self,identifier, ):
        """
        :param identifier: 
        """

        self.identifier = identifier
        self.files = None

    def setFiles(self, files):
        """
        :param files: (Optional) 应从缓存中删除的URL数组
        """
        self.files = files


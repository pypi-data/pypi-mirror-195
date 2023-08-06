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


class ModifyInstancePasswordRequest(JDCloudRequest):
    """
    
修改云主机密码。

详细操作说明请参考帮助文档：[重置密码](https://docs.jdcloud.com/cn/virtual-machines/reset-password)

## 接口说明
- 实例没有正在进行中的任务时才可操作。
- 重置密码后，需要重启云主机后生效。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ModifyInstancePasswordRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}:modifyInstancePassword', 'POST', header, version)
        self.parameters = parameters


class ModifyInstancePasswordParameters(object):

    def __init__(self,regionId, instanceId, password):
        """
        :param regionId: 地域ID。
        :param instanceId: 云主机ID。
        :param password: 实例密码。
可用于SSH登录和VNC登录。
长度为8\~30个字符，必须同时包含大、小写英文字母、数字和特殊符号中的三类字符。特殊符号包括：`\(\)\`~!@#$%^&\*\_-+=\|{}\[ ]:";'<>,.?/，`。
更多密码输入要求请参见 [公共参数规范](https://docs.jdcloud.com/virtual-machines/api/general_parameters)。

        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.password = password


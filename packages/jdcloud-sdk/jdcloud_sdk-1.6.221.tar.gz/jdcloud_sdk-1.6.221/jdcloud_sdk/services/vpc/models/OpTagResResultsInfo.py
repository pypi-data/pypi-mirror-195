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


class OpTagResResultsInfo(object):

    def __init__(self, resourceId=None, success=None, msg=None):
        """
        :param resourceId: (Optional) 资源id
        :param success: (Optional) 操作标签与资源关系结果状态

        :param msg: (Optional) 操作标签与资源关系结果描述
操作成功时msg为操作成功
操作失败时msg为失败的原因
        """

        self.resourceId = resourceId
        self.success = success
        self.msg = msg

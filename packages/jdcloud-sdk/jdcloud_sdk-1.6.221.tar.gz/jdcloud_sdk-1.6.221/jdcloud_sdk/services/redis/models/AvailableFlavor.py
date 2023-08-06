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


class AvailableFlavor(object):

    def __init__(self, shardNumber=None, ipNumber=None, recommended=None, instanceClasses=None, detail=None):
        """
        :param shardNumber: (Optional) 分片数
        :param ipNumber: (Optional) IP数
        :param recommended: (Optional) 是否推荐
        :param instanceClasses: (Optional) 规格代码，标准版为实例的规格代码；集群版为单分片规格代码
        :param detail: (Optional) 规格详情
        """

        self.shardNumber = shardNumber
        self.ipNumber = ipNumber
        self.recommended = recommended
        self.instanceClasses = instanceClasses
        self.detail = detail

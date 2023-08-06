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


class ServerGroup(object):

    def __init__(self, loadBalancerId=None, serverGroupId=None, name=None):
        """
        :param loadBalancerId: (Optional) 负载均衡ID
        :param serverGroupId: (Optional) 虚拟服务器组ID
        :param name: (Optional) 虚拟服务器组名称
        """

        self.loadBalancerId = loadBalancerId
        self.serverGroupId = serverGroupId
        self.name = name

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


class VserverGroupDetail(object):

    def __init__(self, cloudID=None, vserverGroupId=None, vserverGroupName=None, backendServers=None):
        """
        :param cloudID: (Optional) 所属云ID
        :param vserverGroupId: (Optional) 服务器组ID
        :param vserverGroupName: (Optional) 服务器组名称
        :param backendServers: (Optional) 
        """

        self.cloudID = cloudID
        self.vserverGroupId = vserverGroupId
        self.vserverGroupName = vserverGroupName
        self.backendServers = backendServers

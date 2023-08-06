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


class SendMessageToUserRequest(JDCloudRequest):
    """
    发送自定义信令给房间内的人员
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(SendMessageToUserRequest, self).__init__(
            '/message/{appId}/toUser/{roomId}', 'POST', header, version)
        self.parameters = parameters


class SendMessageToUserParameters(object):

    def __init__(self, appId,roomId,):
        """
        :param appId: 应用ID
        :param roomId: 房间ID
        """

        self.appId = appId
        self.roomId = roomId
        self.eventName = None
        self.message = None
        self.peerId = None

    def setEventName(self, eventName):
        """
        :param eventName: (Optional) 事件名称
        """
        self.eventName = eventName

    def setMessage(self, message):
        """
        :param message: (Optional) 自定义信令消息
        """
        self.message = message

    def setPeerId(self, peerId):
        """
        :param peerId: (Optional) peerId
        """
        self.peerId = peerId


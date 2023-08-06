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


class OSSAuthInfo(object):

    def __init__(self, accessKey=None, secretKey=None, bucketName=None, objectName=None):
        """
        :param accessKey: (Optional) 密钥
        :param secretKey: (Optional) 密钥的加密密钥
        :param bucketName: (Optional) 默认为/tt-video
        :param objectName: (Optional) 
        """

        self.accessKey = accessKey
        self.secretKey = secretKey
        self.bucketName = bucketName
        self.objectName = objectName

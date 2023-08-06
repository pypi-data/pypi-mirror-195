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


class OriSchedRule(object):

    def __init__(self, id=None, customName=None, oriSource=None, serviceNode=None, sourceType=None, sources=None, createTime=None, updateTime=None):
        """
        :param id: (Optional) 
        :param customName: (Optional) 域名； 如果值为* 表示，所有域名在此节点上遵循此条回源规则，如果为某个特定域名，表示只有此域名，在该节点上遵循此条回源规则
        :param oriSource: (Optional) 回源信息，支持主备, json序列话后的字符串"{\"Master\":[\"10.226.193.9\"],\"Slave\":[]}"
        :param serviceNode: (Optional) 节点信息
        :param sourceType: (Optional) 回源类型：目前只支持 ips
        :param sources: (Optional) 回源ip； 为 OriSource 字段master中 之一
        :param createTime: (Optional) 创建时间
        :param updateTime: (Optional) 更新时间
        """

        self.id = id
        self.customName = customName
        self.oriSource = oriSource
        self.serviceNode = serviceNode
        self.sourceType = sourceType
        self.sources = sources
        self.createTime = createTime
        self.updateTime = updateTime

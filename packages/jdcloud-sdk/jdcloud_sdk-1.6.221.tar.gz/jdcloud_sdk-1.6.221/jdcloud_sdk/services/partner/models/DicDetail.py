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


class DicDetail(object):

    def __init__(self, id=None, codeType=None, code=None, name=None, value=None, useFlag=None, systemType=None, refValue=None, seq=None, remark=None, createTime=None, createUser=None, updateTime=None, updateUser=None, yn=None):
        """
        :param id: (Optional) ID
        :param codeType: (Optional) 字典类型
        :param code: (Optional) 字典编码
        :param name: (Optional) 字典编码名称
        :param value: (Optional) 字典编码值
        :param useFlag: (Optional) null
        :param systemType: (Optional) 系统类型
        :param refValue: (Optional) 引用值
        :param seq: (Optional) 顺序
        :param remark: (Optional) 字典说明
        :param createTime: (Optional) 创建时间
        :param createUser: (Optional) 创建人
        :param updateTime: (Optional) 修改时间
        :param updateUser: (Optional) 修改人
        :param yn: (Optional) 是否删除0未删除,1已删除
        """

        self.id = id
        self.codeType = codeType
        self.code = code
        self.name = name
        self.value = value
        self.useFlag = useFlag
        self.systemType = systemType
        self.refValue = refValue
        self.seq = seq
        self.remark = remark
        self.createTime = createTime
        self.createUser = createUser
        self.updateTime = updateTime
        self.updateUser = updateUser
        self.yn = yn

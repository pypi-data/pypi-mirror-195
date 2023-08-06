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


class ThingModelTemplate(object):

    def __init__(self, thingModelTemplateId=None, thingModelTemplateName=None, productCategoryNames=None, productCategoryIds=None, updatedTime=None, userPin=None, ossPath=None):
        """
        :param thingModelTemplateId: (Optional) 物模型模板ID
        :param thingModelTemplateName: (Optional) 模型模板名称
        :param productCategoryNames: (Optional) 产品分类名称数组，索引0为一级产品分类名称
        :param productCategoryIds: (Optional) 产品分类ID数组，索引0为一级产品分类ID
        :param updatedTime: (Optional) 更新时间，时间为东八区（UTC/GMT+08:00）
        :param userPin: (Optional) 操作人
        :param ossPath: (Optional) 物模型文件在oss上的存储路径
        """

        self.thingModelTemplateId = thingModelTemplateId
        self.thingModelTemplateName = thingModelTemplateName
        self.productCategoryNames = productCategoryNames
        self.productCategoryIds = productCategoryIds
        self.updatedTime = updatedTime
        self.userPin = userPin
        self.ossPath = ossPath

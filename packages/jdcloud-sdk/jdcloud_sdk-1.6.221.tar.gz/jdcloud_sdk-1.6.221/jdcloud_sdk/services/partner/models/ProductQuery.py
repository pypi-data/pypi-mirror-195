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


class ProductQuery(object):

    def __init__(self, id=None, productType=None, productId=None, productName=None, productNameLike=None, productIdList=None, status=None, remark=None, createUser=None, updateUser=None, pageIndex=None, pageSize=None, offset=None):
        """
        :param id: (Optional) ID
        :param productType: (Optional) 产品类型
        :param productId: (Optional) 产品ID
        :param productName: (Optional) 产品名称
        :param productNameLike: (Optional) 产品名称(模糊查询)
        :param productIdList: (Optional) 产品ID列表
        :param status: (Optional) 状态
        :param remark: (Optional) 备注
        :param createUser: (Optional) 创建人
        :param updateUser: (Optional) 修改人
        :param pageIndex: (Optional) 当前页序号
        :param pageSize: (Optional) 每页结果数量
        :param offset: (Optional) 
        """

        self.id = id
        self.productType = productType
        self.productId = productId
        self.productName = productName
        self.productNameLike = productNameLike
        self.productIdList = productIdList
        self.status = status
        self.remark = remark
        self.createUser = createUser
        self.updateUser = updateUser
        self.pageIndex = pageIndex
        self.pageSize = pageSize
        self.offset = offset

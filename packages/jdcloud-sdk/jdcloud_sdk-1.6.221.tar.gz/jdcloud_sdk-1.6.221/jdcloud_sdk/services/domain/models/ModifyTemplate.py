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


class ModifyTemplate(object):

    def __init__(self, nationCodeCh=None, nationCodeEn=None, provinceCodeCh=None, provinceCodeEn=None, cityCodeCh=None, cityCodeEn=None, addressCh=None, addressEn=None, zipCode=None, phone=None, fax=None, email=None, ownerType=None):
        """
        :param nationCodeCh: (Optional) 国家及地区（中文）
        :param nationCodeEn: (Optional) 国家及地区（英文）中国：china
        :param provinceCodeCh: (Optional) 省份（中文）
        :param provinceCodeEn: (Optional) 省份（英文）
        :param cityCodeCh: (Optional) 城市（中文）
        :param cityCodeEn: (Optional) 城市（英文）
        :param addressCh: (Optional) 通信地址（中文）
        :param addressEn: (Optional) 通信地址（英文）
        :param zipCode: (Optional) 邮编 6位数字
        :param phone: (Optional) 联系电话，国家区号-地区区号(或手机号码前3位)-电话号码（或手机号码后8位) 例:86-138-12345678
        :param fax: (Optional) 传真，国家区号-地区区号(或手机号码前3位)-电话号码（或手机号码后8位) 例:86-138-12345678
        :param email: (Optional) 邮件
        :param ownerType: (Optional) 所有者类型  1个人 2企业
        """

        self.nationCodeCh = nationCodeCh
        self.nationCodeEn = nationCodeEn
        self.provinceCodeCh = provinceCodeCh
        self.provinceCodeEn = provinceCodeEn
        self.cityCodeCh = cityCodeCh
        self.cityCodeEn = cityCodeEn
        self.addressCh = addressCh
        self.addressEn = addressEn
        self.zipCode = zipCode
        self.phone = phone
        self.fax = fax
        self.email = email
        self.ownerType = ownerType

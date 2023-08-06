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


class RuleSet(object):

    def __init__(self, id=None, name=None, description=None, kind=None, phase=None, last_updated=None, rules=None, version=None, source=None):
        """
        :param id: (Optional) 规则集的标识。
        :param name: (Optional) 规则集的名称。
        :param description: (Optional) 规则集的描述。
        :param kind: (Optional) 规则集的类型，有效值zone。
        :param phase: (Optional) 执行规则集的阶段，有效值http_ratelimit。
        :param last_updated: (Optional) 规则集最近修改时间。
        :param rules: (Optional) 规则集中的所有规则。
        :param version: (Optional) 规则集的版本。
        :param source: (Optional) 
        """

        self.id = id
        self.name = name
        self.description = description
        self.kind = kind
        self.phase = phase
        self.last_updated = last_updated
        self.rules = rules
        self.version = version
        self.source = source

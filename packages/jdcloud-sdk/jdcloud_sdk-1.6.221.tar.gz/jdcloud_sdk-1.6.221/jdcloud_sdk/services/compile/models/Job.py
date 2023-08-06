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


class Job(object):

    def __init__(self, uuid=None, createdAt=None, updatedAt=None, name=None, codeType=None, codeRepoUrl=None, codeRepoUrlLabel=None, codeRepoBranch=None, createUserName=None, codeRepoPrivate=None, createUserPin=None, ossPath=None, ossHost=None, ossBucket=None, buildImage=None, buildImageLabel=None, isUserBuildSetConfig=None, buildSetConfig=None, buildTimeOut=None, buildResourceCpu=None, buildResourceMem=None, noticeMail=None, noticeType=None, compilerType=None, dockerRegistry=None, dockerRepository=None, dockerRegistryUri=None):
        """
        :param uuid: (Optional) 构建任务uuid
        :param createdAt: (Optional) 创建时间戳
        :param updatedAt: (Optional) 最后一次更新时间
        :param name: (Optional) 构建名称
        :param codeType: (Optional) 代码存储类型，目前只支持github
        :param codeRepoUrl: (Optional) 代码clone路径
        :param codeRepoUrlLabel: (Optional) 代码名称的显示Label
        :param codeRepoBranch: (Optional) 分支
        :param createUserName: (Optional) 创建者
        :param codeRepoPrivate: (Optional) 是否是私有仓库
        :param createUserPin: (Optional) 最后一次更细者
        :param ossPath: (Optional) 用户云存储路径，如果为空，使用公用的云存储
        :param ossHost: (Optional) 用户云存储主机，实际为用户云存储所在地域
        :param ossBucket: (Optional) 用户云存储bucket，如果为空，使用公用的云存储
        :param buildImage: (Optional) 编译镜像地址
        :param buildImageLabel: (Optional) 编译镜像的显示Label
        :param isUserBuildSetConfig: (Optional) 是否在页面配置构建方式，这项为true，则buildSetConfig需要有内容，如果这项为false，即使buildSetConfig有内容，也不生效
        :param buildSetConfig: (Optional) 见isUserBuildSetConfig的说明
        :param buildTimeOut: (Optional) 超时时间，单位秒
        :param buildResourceCpu: (Optional) cpu分配核数
        :param buildResourceMem: (Optional) 内存分配大小，单位MB
        :param noticeMail: (Optional) 通知邮件
        :param noticeType: (Optional) 通知频率， MAIL_FAILED失败时通知，MAIL_EVERY每次构建就通知
        :param compilerType: (Optional) 构建类型
        :param dockerRegistry: (Optional) 镜像注册表名
        :param dockerRepository: (Optional) 镜像仓库名
        :param dockerRegistryUri: (Optional) 注册表的URI
        """

        self.uuid = uuid
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.name = name
        self.codeType = codeType
        self.codeRepoUrl = codeRepoUrl
        self.codeRepoUrlLabel = codeRepoUrlLabel
        self.codeRepoBranch = codeRepoBranch
        self.createUserName = createUserName
        self.codeRepoPrivate = codeRepoPrivate
        self.createUserPin = createUserPin
        self.ossPath = ossPath
        self.ossHost = ossHost
        self.ossBucket = ossBucket
        self.buildImage = buildImage
        self.buildImageLabel = buildImageLabel
        self.isUserBuildSetConfig = isUserBuildSetConfig
        self.buildSetConfig = buildSetConfig
        self.buildTimeOut = buildTimeOut
        self.buildResourceCpu = buildResourceCpu
        self.buildResourceMem = buildResourceMem
        self.noticeMail = noticeMail
        self.noticeType = noticeType
        self.compilerType = compilerType
        self.dockerRegistry = dockerRegistry
        self.dockerRepository = dockerRepository
        self.dockerRegistryUri = dockerRegistryUri

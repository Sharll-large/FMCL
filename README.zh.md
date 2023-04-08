# FMCL —— 一个100%开源的，轻量级的，跨平台的《我的世界》启动器
[英文版(English Verison)](https://github.com/Sharll-large/FMCL/blob/main/README.md)

### 全名：First Minecraft Launcher

### 简介
> 这是一个由 *Python3(.10)* 编写的《我的世界》启动器  
> 我们的目标是为Python开发者开辟启动器开发的道路。  

### 支持的平台
> 架构\操作系统|Windows|Linux|MacOS|
> |-|-|-|-|
> |x64|✔|❔|❔|
> |x86|❔|❔|❌|
> |ARM64|📌|📌|📌|
> |ARM32|❌|❌|❌|
> 
> 符号含义：  
> ✔ - 支持: 经过验证，功能完整  
> ❔ - 支持: 未经测试，功能可能不完整或有更多的bug  
> 📌 - 不支持: 计划中  
> ❌ - 不支持: 不做计划  

### 基于FMCL的核心制作自己的启动器？ 
> FMCL的核心功能（FMCLCore）完全不依赖Gui，因此您可以使用它制作您自己的启动器。  
> 我们使用MIT开源协议，因此您的自由度非常高。  

### 下载本程序
> 您可以在Releases中下载打包好的.pyzw文件，它可以在安装有Python3(.10)的任何设备上运行。  
> 如果您想下载源码并自行搭建或随您所愿地修改，请下载仓库， **不过请记住MIT协议！**。  

### 依赖项
> pyperclip: 用于复制文本
> urllib: 下载和API调用
> json: JSON解析
> threading: 多线程下载
> os, platform, sys: 获取系统信息
> subprocess: 执行命令
> tkinter: GUI

### 开发计划
> | 目标 | 进度 |
> | - | - |
> | 代码规范化重构 | 75% |
> | 稳定版启动核心 | 100% |
> | 稳定版下载核心 | 100% |
> | Forge/ Fabric/ Optifine/ Quilt 自动安装 | 0% |
> | Mod 搜索和下载（by LJS80） | 50% |
> | 完成版本下载功能 | 0% |
> | 替换ARM平台的LWJGL | 0% |
> | 微软账户登录 | 100% |
> | 支持日志系统 | 100% |
> | 重构新UI（by pxinz） | 100% |

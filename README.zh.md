# FMCL —— 一个100%开源的，轻量级的，跨平台的《我的世界》启动器

[英文版(English Verison)](https://github.com/Sharll-large/FMCL/blob/main/README.md)  
`全名:` First Minecraft Launcher

## 简介

这是一个使用`Python3(.10)`编写的《我的世界》启动器  
我们的目标是为Python开发者开辟启动器开发的道路。

## 支持的平台

| 架构\操作系统 | Windows | Linux | MacOS |
|---------|---------|-------|-------|
| x64     | ✔       | ❔     | ❔     |
| x86     | ❔       | ❔     | ❌     |
| ARM64   | 📌      | 📌    | 📌    |
| ARM32   | ❌       | ❌     | ❌     |

符号含义:
> ✔ - 支持: 经过验证，功能完整  
> ❔ - 支持: 未经测试，功能可能不完整或有更多的bug  
> 📌 - 不支持: 计划中  
> ❌ - 不支持: 不做计划

## 基于FMCL的核心制作自己的启动器

FMCL的核心功能(src/core)完全不依赖GUI来运行, 因此您可以使用它制作您自己的启动器。  
因此, 我们致力于让代码变得更加易懂, 所以可能会频繁地重构。重构对于代码的影响将是极大的, 在正式版发布前, 我们暂时不建议您使用核心制作自己的启动器。  
我们使用MIT开源协议, 因此您的自由度非常高。

## 下载本程序

您可以在Releases中下载打包好的.pyzw文件, 它可以在安装有Python3(.10)的任何设备上运行。  
如果您想下载源码并自行搭建或随您所愿地修改, 请下载仓库, **不过请记住MIT协议!**

## 依赖项

| 依赖库                   | 用途        | 来源                                                                        |
|-----------------------|-----------|---------------------------------------------------------------------------|
| os, pathlib           | 操作文件      | [asweigart/pyperclip](https://github.com/asweigart/pyperclip/tree/master) |
| platform, sys         | 获取系统信息    | Python3.10                                                                |
| subprocess            | 执行命令      | Python3.10                                                                |
| concurrent, threading | 多线程功能     | Python3.10                                                                |
| urllib                | 下载与API调用  | Python3.10                                                                |
| json                  | JSON解析与写入 | Python3.10                                                                |
| pyperclip(准备弃用)       | 复制文本      | Python3.10                                                                |
| smt                   | 小工具       | SMDC                                                                      |
| tkinter               | GUI       | Python3.10                                                                |

## 开发计划

| 目标                                            | 进度  | 状态  |
|-----------------------------------------------|-----|-----|
| 代码规范化, 单例化重构                                  | 75% | 进行中 |
| Mod 搜索和下载(核心)(by LJS80)                       | 50% | 进行中 |
| 重构新UI(计划: 使用tkinter Canvas)                   | 0%  | 规划中 |
| 完成版本下载功能(UI)                                  | 0%  | 搁置  |
| Forge / Fabric / Optifine / Quilt 自动安装(核心+UI) | 0%  | 搁置  |
| 替换ARM平台的LWJGL(核心)                             | 0%  | 搁置  |

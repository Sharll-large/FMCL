# FMCL —— An Open Source, Lite, Multi-Platform Minecraft Launcher

[Chinese Version(简体中文版)](https://github.com/Sharll-large/FMCL/blob/main/README.zh.md)  
`Full Name:` First Minecraft Launcher

## Description

A Minecraft(JE) launcher written by [Python3(.10)](https://github.com/python/cpython/tree/3.10).  
Our target: To create a new minecraft launcher developing period for python developers.

## Supported Platforms

| CPU Arch\OS | Windows | Linux | MacOS |  
|-------------|---------|-------|-------|  
| x64         | ✔       | ❔     | ❔     |  
| x86         | ❔       | ❔     | ❌     |  
| ARM64       | 📌      | 📌    | 📌    |  
| ARM32       | ❌       | ❌     | ❌     |  

Symbols:
> ✔ - Full support (completed and verified)  
> ❔ - Full support (not completed or verified)  
> 📌 - Plan to do  
> ❌ - Won't support

`Tip: All x86_32 machines may be given up someday.`

## Making Minecraft launcher, you can do it too!

The FMCL core(src/core) doesn't rely on the GUI module. So, you can use the core in your project easily.  
Therefore, we are committed to making the code more understandable, so there may be frequent refactoring. Refactoring
will have a significant impact on the code, so we do not recommend using the core to create your own launcher until the
official version is released.  
The MIT License has been used. So you're highly free to use the core.
`The usage of core is on writing.`

## Download This Program

You can download built files in [Releases](https://github.com/Sharll-large/FMCL/releases), then run it on supported
computer that installed Python3(.10).  
You can also download the source.

```bash  
git clone https://github.com/Sharll-large/FMCL
cd FMCL
__main__.py  
```

## Depencies

| Depency                | Usage                              | Source                                                                    |  
|------------------------|------------------------------------|---------------------------------------------------------------------------|  
| os, pathlib            | Processing files                   | Python 3.10                                                               |  
| platform, sys          | Geting system informations         | Python3.10                                                                |  
| subprocess             | Executing commands                 | Python3.10                                                                |  
| concurrent, threading  | Multi-threading capabilities       | Python3.10                                                                |  
| urllib                 | Downloading files & Executing APIs | Python3.10                                                                |  
| json                   | JSON dumping&writing               | Python3.10                                                                |  
| pyperclip(deprecating) | Copying text                       | [asweigart/pyperclip](https://github.com/asweigart/pyperclip/tree/master) |  
| smt                    | Tools                              | SMDC                                                                      |  
| tkinter                | GUI                                | Python3.10                                                                |  

## Plans

| Target                                                  | Progress | Statement   |  
|---------------------------------------------------------|----------|-------------|  
| Standardize code, refactor into singletons              | 75%      | In progress |  
| Mod search and download (core)(by LJS80)                | 50%      | In progress |  
| Refactor new UI (Plan: use tkinter Canvas)              | 0%       | Planning    |  
| Complete version download feature (UI)                  | 0%       | On hold     |  
| Forge / Fabric / Optifine / Quilt auto-install(core+UI) | 0%       | On hold     |  
| Replace LWJGL for ARM platform (core)                   | 0%       | On hold     |

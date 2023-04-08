# FMCL —— An Open Source, Lite, Cross Platform Minecraft Launcher.
[简体中文版(Simplified Chinese Version)](https://github.com/Sharll-large/FMCL/blob/main/README.zh.md)

### #Full name: First Minecraft Launcher#

### About:
  > A simple Java Edition minecraft launcher wriiten by *Python(3.10)*.
  > Our dream is to create a new minecraft launcher developing period for python developers.

### Platform support
> |CPU Arch\OS|Windows|Linux|MacOS|
> |-|-|-|-|
> |x64|✔|❔|❔|
> |x86|❔|❔|❌|
> |ARM64|📌|📌|📌|
> |ARM32|❌|❌|❌|
> 
> 
> ✔ - Full support (verified)  
> ❔ - Done but unverified (Some functions may not be available, There may be more bugs)  
> 📌 - Plan to do  
> ❌ - Won't support  


### Making Minecraft launcher, you can do it too!
  > The FMCL core does not completely rely on the GUI module, so you can write your own GUI!
  > Because we chose the MIT open source license, you are nearly free to distribute the software however you want.

### Download this programme
  > You can download packed [.pyzw](https://docs.python.org/3/library/zipapp.html) files in Releases. You can run this on any computer installed Python3(.10).
  > If you want to build the programme by yourself or do something you like to do, you can download the repo and do what you want. **But remember the MIT License!**

### Depencies
  > pyperclip: use for copy text
  > urllib: download and api call
  > json: json parse
  > threading: multi thread download
  > os, platform, sys: system info
  > subprocess: Shell commands run
  > tkinter: GUI making

### Coding plans
1. Make stable launching core(Done) 
2. Make stable downloading core(Done)
3. Make Forge/ Fabric/ Optifine/ Quilt auto-install
4. Make Mods search & install（by LJS80）
5. version json download 
6. find resource of LWJGL arm
7. Microsoft account auth(Done)
8. Logging(Done)
9. Rebuild New UI(by pxinz) (Done)

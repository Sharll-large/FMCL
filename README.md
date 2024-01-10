# FMCL —— An Open Source, Lite, Multi-Platform Minecraft Launcher.

###### [简体中文](https://github.com/Sharll-large/FMCL/blob/main/README.zh.md)

### About:

A Minecraft(JE) launcher written by [Python3.10](https://github.com/python/cpython/tree/3.10).

Target: To create a new minecraft launcher developing period for python developers.

### Platform support

> | CPU Arch\OS | Windows | Linux | MacOS |
> |-------------|---------|-------|-------|
> | x86_64      | ✔       | ❔     | ❔     |
> | x86         | ❔      | ❔     | ❔     |
> | ARM64(RasPi)| 📌      | 📌     | 📌     |
> | ARM32       | ❌      | ❌     | ❌     |
>
> ✔ - Full support (verified)
> 
> ❔- Full support (not verified)
> 
> 📌 - Plan to do
> 
> ❌ - Won't support
> 
*all x86 machines may be given up some day*

### Making Minecraft launcher, you can do it too!
The FMCL core does not rely on the gui module, so you can use the core in your project easily.
The usage of core is on writing.

### Run this programme
You can download built files in [Releases](https://github.com/Sharll-large/FMCL/releases). You can run this on supported computer installed Python3(.10).
```bash
git clone https://github.com/Sharll-large/FMCL
cd FMCL
__main__.py
```

### Depencies

pyperclip: use for copy text(on removing)

dearpygui: use for gui(on adding)

the other depencies are all default packages of Python3.

### Coding plans

1. Edit codes(for longer developing)
2. Use dearpygui for UI(discussing)

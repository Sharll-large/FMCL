import tkinter.messagebox

import FMCLCore.Download.MinecraftVanillaDownload
import FMCLCore.System.CoreConfigIO
import FMCLView.Const
import FMCLView.main

if __name__ == "__main__":
    try:
        FMCLCore.System.CoreConfigIO.fixdepend() # 修复配置文件
        FMCLCore.Download.MinecraftVanillaDownload.get([], FMCLCore.System.CoreConfigIO.read()["Source"], True) # 缓存版本信息
        FMCLView.Const.lang = FMCLCore.System.CoreConfigIO.read()["Language"] # 加载语言配置
        FMCLView.main.main()
    except Exception as e:
        tkinter.messagebox.showerror("FMCL Exception", repr(e))

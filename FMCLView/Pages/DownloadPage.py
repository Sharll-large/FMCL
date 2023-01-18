import tkinter as tk
import tkinter.ttk
import FMCLCore.Download.MinecraftVanillaDownload
import FMCLCore.System.CoreConfigIO
import FMCLView.Const
import tkinter.messagebox
import time

def main():
    def getversions():
        buf = FMCLCore.Download.MinecraftVanillaDownload.get(["snapshot", "old_alpha"], FMCLCore.System.CoreConfigIO.read()["Source"], False)[2]
        verlist = []
        for i in buf:
            verlist.append(i["id"])
        versions["values"] = verlist

    def refresh():
        FMCLCore.Download.MinecraftVanillaDownload.get([], FMCLCore.System.CoreConfigIO.read()["Source"], True)

    def download():
        print(versions.get() + " as " + version_name.get())
        target = {}
        buf = FMCLCore.Download.MinecraftVanillaDownload.get(["snapshot", "old_alpha"], FMCLCore.System.CoreConfigIO.read()["Source"], False)[2]
        for i in buf:
            if i["id"] == versions.get():
                target = i
                break
        tk.messagebox.askokcancel("FMCL", "即将下载" + versions.get() + "as" + version_name.get())


    def showinfo(virtual):
        def format_time(t_str: str) ->str:
            return time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(t_str, "%Y-%m-%dT%H:%M:%S+00:00"))
        buf = FMCLCore.Download.MinecraftVanillaDownload.get(["snapshot", "old_alpha"], FMCLCore.System.CoreConfigIO.read()["Source"], False)[2]
        for i in buf:
            if i["id"] == versions.get():
                 version_type["text"] = i['type']
                 release_time["text"] = format_time(i['releaseTime'])
                 version_name.delete(0, "end")
                 version_name.insert(0, i["id"])
                 break


    f = tk.ttk.Frame()
    tk.ttk.Label(f, text="Root version").grid(row=0, column=0)
    versions = tk.ttk.Combobox(f, postcommand=getversions, state="readonly")
    versions.grid(row=0, column=1)
    versions.bind("<<ComboboxSelected>>", showinfo)
    tk.ttk.Button(f, text=FMCLView.Const.get("Download.Refresh"), command=refresh).grid(row=0, column=2)

    tk.ttk.Label(f, text="Version name").grid(row=1, column=0)
    version_name = tk.ttk.Entry(f)
    version_name.grid(row=1, column=1)
    tk.ttk.Button(f, text=FMCLView.Const.get("Download.Download"), command=download).grid(row=1, column=2)

    tk.ttk.Label(f, text="Version type").grid(row=2, column=0)
    version_type = tk.ttk.Label(f)
    version_type.grid(row=2, column=1)

    tk.ttk.Label(f, text="Release time").grid(row=3, column=0)
    release_time = tk.ttk.Label(f)
    release_time.grid(row=3, column=1)

    getversions()
    return f

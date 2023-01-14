import tkinter as tk
import tkinter.ttk
import FMCLCore.System.CoreVersionGet
import FMCLCore.System.CoreConfigIO
import FMCLCore.Launch.CoreLaunchTaskSub
import FMCLView.Const
import FMCLView.Low.Launch

def main():
    def refresh1():
        versions["values"] = FMCLCore.System.CoreVersionGet.local_version(FMCLCore.System.CoreConfigIO.read()[".mc"])
    def refresh2():
        accounts["values"] = FMCLCore.System.CoreConfigIO.get_account()
    def launch():
        account = FMCLCore.System.CoreConfigIO.read()["Accounts"][accounts.current()]
        if account["type"] == "microsoft":
            FMCLView.Low.Launch.launch(FMCLCore.Launch.CoreLaunchTaskSub.launch(
                game_directory=FMCLCore.System.CoreConfigIO.read()[".mc"],
                version_name=versions.get(),
                playername=account["name"],
                java=FMCLCore.System.CoreConfigIO.read()["java"],
                UUID=account["uuid"],
                TOKEN=account["token"]
            ))
        else:
            FMCLView.Low.Launch.launch(FMCLCore.Launch.CoreLaunchTaskSub.launch(
                game_directory=FMCLCore.System.CoreConfigIO.read()[".mc"],
                version_name=versions.get(),
                playername=account["name"],
                java=FMCLCore.System.CoreConfigIO.read()["java"]
            ))


    f = tk.ttk.Frame()
    tk.ttk.Label(f, text=FMCLView.Const.get("Launch.Choose")).grid(row=0, column=0)
    versions = tk.ttk.Combobox(f, postcommand=refresh1, state='readonly')
    versions.grid(row=0, column=1)
    tk.ttk.Label(f, text=FMCLView.Const.get("Launch.Account")).grid(row=1, column=0)
    accounts = tk.ttk.Combobox(f, postcommand=refresh2, state='readonly')
    accounts.grid(row=1, column=1)
    tk.ttk.Button(f, text=FMCLView.Const.get("Launch.Launch"), command=launch).grid(row=2, column=0)

    return f
import subprocess
import threading
import tkinter.messagebox

import FMCLView.Const
import FMCLCore.System.CoreConfigIO
import FMCLCore.Launch.CoreLaunchTaskSub


def launch(account: dict, version: str):
    def call():
        if account["type"] == "microsoft":
            command = FMCLCore.Launch.CoreLaunchTaskSub.launch(
                game_directory=FMCLCore.System.CoreConfigIO.read()[".mc"],
                version_name=version,
                playername=account["name"],
                java=FMCLCore.System.CoreConfigIO.read()["java"],
                UUID=account["uuid"],
                TOKEN=account["token"]
        )
        else:
            command = FMCLCore.Launch.CoreLaunchTaskSub.launch(
                game_directory=FMCLCore.System.CoreConfigIO.read()[".mc"],
                version_name=version,
                playername=account["name"],
                java=FMCLCore.System.CoreConfigIO.read()["java"]
            )
        if command:
            print(command)
            tkinter.messagebox.showinfo("FMCL", FMCLView.Const.get("Launch.Wait").replace("$0", version))
            result = subprocess.getstatusoutput(command)
            if result[0] != 0:
                tkinter.messagebox.showerror(FMCLView.Const.get("Launch.Error") + str(result[0]),
                                             FMCLView.Const.get("Launch.ErrorText"))
        else:
            tkinter.messagebox.showerror("FMCL", FMCLView.Const.get("Launch.NativeError"))

    if tkinter.messagebox.askokcancel("FMCL", FMCLView.Const.get("Launch.Ask")):
        threading.Thread(target=call).start()


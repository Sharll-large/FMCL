import subprocess
import threading
import tkinter.messagebox

import FMCLView.Const


def launch(command: list):
    def call():
        print(command)
        result = subprocess.getstatusoutput(command)
        if result[0] != 0:
            tkinter.messagebox.showerror(FMCLView.Const.get("Launch.Error") + str(result[0]),
                                         FMCLView.Const.get("Launch.ErrorText"))

    if tkinter.messagebox.askokcancel("FMCL", FMCLView.Const.get("Launch.Ask")):
        threading.Thread(target=call).start()
        tkinter.messagebox.showinfo("FMCL", FMCLView.Const.get("Launch.Wait"))


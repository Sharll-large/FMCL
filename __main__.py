# FMCL Boot Entry.
import sys
import tkinter.messagebox
import FMCLCore.System.CoreConfigIO
import FMCLView.main
import FMCLView.Const

if __name__ == "__main__":
    try:
        FMCLCore.System.CoreConfigIO.fixdepend()
        FMCLView.Const.lang = FMCLCore.System.CoreConfigIO.read()["Language"]
        FMCLView.main.main()
    except Exception as e:
        tkinter.messagebox.showerror("FMCL Exception", repr(e))

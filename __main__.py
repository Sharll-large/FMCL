# FMCL Boot Entry.
import sys
import FMCLCore.System.CoreConfigIO
import FMCLView.main
import tkinter.messagebox
if __name__ == "__main__":
    try:
        sys.stdout = open("FMCL.log", "w+")
        sys.stderr = open("FMCL.log", "w+")
        FMCLCore.System.CoreConfigIO.fixdepend()
        FMCLView.main.main()
    except Exception as e:
        tkinter.messagebox.showerror("FMCL Exception", repr(e))

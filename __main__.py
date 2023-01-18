# FMCL Boot Entry.
import sys
import FMCLCore.System.CoreConfigIO
import FMCLCore.System.Logging
import FMCLView.main
import tkinter.messagebox
import traceback

if __name__ == "__main__":
    try:
        sys.stdout = open("FMCL.log", "w")
        sys.stderr = open("FMCL.log", "w")
        FMCLCore.System.CoreConfigIO.fix_depend()
        FMCLView.main.main()
    except:
        error_msg=traceback.format_exc()
        print(FMCLCore.System.Logging.showerror("Error happend! Error message:"))
        print(error_msg)
        tkinter.messagebox.showerror("FMCL Error","Error message:\n"+error_msg)


import tkinter as tk
import tkinter.ttk
import tkinter.filedialog

import FMCLView.Const
import FMCLCore.System.CoreVersionGet
import FMCLCore.System.CoreConfigIO

def main():
    def browseJRE():
        JRE.set(tk.filedialog.askopenfilename())

    def browseMINECRAFT():
        MINECRAFT.delete(0, "end")
        MINECRAFT.insert(0, tk.filedialog.askdirectory())

    def scan(): JRE["values"] = FMCLCore.System.CoreVersionGet.java_versions()

    def refresh():
        JRE.set(FMCLCore.System.CoreConfigIO.read()["java"])
        LANG.set(FMCLCore.System.CoreConfigIO.read()["Language"])
        SOURCE.set(FMCLCore.System.CoreConfigIO.read()["Source"])
        MINECRAFT.delete(0, "end")
        THREADS.delete(0, "end")
        MEMORY.delete(0, "end")
        MINECRAFT.insert(0, FMCLCore.System.CoreConfigIO.read()[".mc"])
        THREADS.insert(0, str(FMCLCore.System.CoreConfigIO.read()["threads"]))
        MEMORY.insert(0, str(FMCLCore.System.CoreConfigIO.read()["ram"]))
        IFBOOST.set(FMCLCore.System.CoreConfigIO.read()["Boost"])
        IFALONE.set(FMCLCore.System.CoreConfigIO.read()["Alone"])

    def save():
        FMCLCore.System.CoreConfigIO.overridejson({
            ".mc": MINECRAFT.get(),
            "java": JRE.get(),
            "threads": int(THREADS.get()),
            "ram": int(MEMORY.get()),
            "Language": LANG.get(),
            "Source": SOURCE.get(),
            "Alone": IFALONE.get(),
            "Boost": IFBOOST.get()
        })

    f = tk.ttk.Frame()

    tk.ttk.Label(f, text=FMCLView.Const.get("Option.JRE")).grid(row=0, column=0)
    JRE = tk.ttk.Combobox(f, postcommand=scan)
    JRE.grid(row=0, column=1)
    tk.ttk.Button(f, text=FMCLView.Const.get("Option.Browse"), command=browseJRE).grid(row=0, column=2)

    tk.ttk.Label(f, text=FMCLView.Const.get("Option.MINECRAFT")).grid(row=1, column=0)
    MINECRAFT = tk.ttk.Entry(f)
    MINECRAFT.grid(row=1, column=1)
    tk.ttk.Button(f, text=FMCLView.Const.get("Option.Browse"), command=browseMINECRAFT).grid(row=1, column=2)

    tk.ttk.Label(f, text=FMCLView.Const.get("Option.Threads")).grid(row=2, column=0)
    THREADS = tk.ttk.Entry(f)
    THREADS.grid(row=2, column=1)

    tk.ttk.Label(f, text=FMCLView.Const.get("Option.Memory")).grid(row=3, column=0)
    MEMORY = tk.ttk.Entry(f,)
    MEMORY.grid(row=3, column=1)

    tk.ttk.Label(f, text=FMCLView.Const.get("Option.Language")).grid(row=4, column=0)
    LANG = tk.ttk.Combobox(f, values=("简体中文", "English"), state='readonly')
    LANG.grid(row=4, column=1)

    tk.ttk.Label(f, text=FMCLView.Const.get("Option.Source")).grid(row=5, column=0)
    SOURCE = tk.ttk.Combobox(f, values=("Default", "BMCLAPI", "MCBBS"), state="readonly")
    SOURCE.grid(row=5, column=1)

    IFALONE, IFBOOST = tk.BooleanVar(), tk.BooleanVar()
    tk.ttk.Checkbutton(f, text=FMCLView.Const.get("Option.Alone"), variable=IFALONE).grid(row=6, column=0)
    tk.ttk.Checkbutton(f, text=FMCLView.Const.get("Option.Boost"), variable=IFBOOST).grid(row=6, column=1)

    tk.ttk.Button(f, text=FMCLView.Const.get("Option.Save"), command=save).grid(row=7, column=0)
    tk.ttk.Button(f, text=FMCLView.Const.get("Option.Refresh"), command=refresh).grid(row=7, column=1)


    refresh()
    return f



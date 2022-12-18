import Core.Launch.CoreLaunchTask
import Core.System.CoreConfigIO
import Core.System.CoreVersionGet
import os
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk


def main():
    print(__file__+": load launch page")

    def start():
        """
        This function is used to launch a game,
        """
        command = Core.Launch.CoreLaunchTask.launch(Core.System.CoreConfigIO.read()[".mc"], launch_version.get(), Core.System.CoreConfigIO.read()["java"],
                                                    Core.System.CoreConfigIO.read()["playername"])
        print(command)
        if command == 0:
            tk.messagebox.showerror("Null.")
        elif command == 1:
            tk.messagebox.showerror("Error", "This is not a complete game.")
        else:
            if os.system(command) != 0:
                tk.messagebox.showerror("Error", "Unable to launch. \nPlease upload the logs to issue.")

    def drop():
        # refresh version choose
        launch_version["values"] = Core.System.CoreVersionGet.local_version(Core.System.CoreConfigIO.read()[".mc"])

    launch_view = tk.ttk.Frame()
    launch_title = tk.ttk.Label(launch_view, text="FMCL")
    launch_title.place(x=20, y=5)

    launch_about = tk.ttk.Label(launch_view,
                                text="FMCL is a free minecraft launcher.\n" \
                                     "Version: Public preview 3\n" \
                                     "Author:  Sharll\n" \
                                     "Do not decompile or crack this software")
    launch_about.place(x=20, y=35)
    launch_launch = tk.ttk.Button(launch_view, text="launch", command=start, width=20)
    launch_launch.place(x=200, y=200)
    launch_version = tk.ttk.Combobox(launch_view, postcommand=drop, width=20)
    launch_version.place(x=200, y=180)

    return launch_view

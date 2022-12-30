import tkinter as tk
import tkinter.ttk

import Core.Launch.CoreLaunchTaskSub
import Core.System.CoreConfigIO
import Core.System.CoreVersionGet
import View.ToCoreGui.LaunchGui


def main():
    print(__file__+": load launch page")

    def start():
        command = Core.Launch.CoreLaunchTaskSub.launch(Core.System.CoreConfigIO.read()[".mc"], launch_version.get(),
                                Core.System.CoreConfigIO.read()["java"], Core.System.CoreConfigIO.read()["playername"])
        View.ToCoreGui.LaunchGui.main(command)

    def drop():
        # refresh version choose
        launch_version["values"] = Core.System.CoreVersionGet.local_version(Core.System.CoreConfigIO.read()[".mc"])

    launch_view = tk.ttk.Frame()
    launch_launch = tk.ttk.Button(launch_view, text="launch", command=start, width=20)
    launch_launch.place(x=230, y=180)
    launch_version = tk.ttk.Combobox(launch_view, postcommand=drop, width=20)
    launch_version.place(x=20, y=180)

    return launch_view

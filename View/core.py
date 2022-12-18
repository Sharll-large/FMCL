import os
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk

import Core.Launch.CoreLaunchTask
import Core.System.CoreConfigIO
import Core.System.CoreVersionGet
import View.Themes.AboutPage
import View.Themes.AccountManagePage
import View.Themes.DownloadPage
import View.Themes.LaunchPage
import View.Themes.SettingPage


def getpicture(name):
    return tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "Resources", name))


def main():
    def start():
        command = Core.Launch.CoreLaunchTask.launch(Core.System.CoreConfigIO.read()[".mc"], version_choose.get(), Core.System.CoreConfigIO.read()["java"],
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
        version_choose["values"] = Core.System.CoreVersionGet.local_version(Core.System.CoreConfigIO.read()[".mc"])

    root = tk.Tk()

    img_icon = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "Resources", "Sharll.png"))

    root.geometry('640x360')
    root.title("Sharll's Craft Launcher")
    root.resizable(False, False)
    root.iconphoto(False, img_icon)

    notebook = tk.ttk.Notebook(root, width=400, height=300)

    img_launch = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "Resources", "launch.png"))
    img_download = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "Resources", "download.png"))
    img_setting = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "Resources", "setting.png"))
    img_account = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "Resources", "account.png"))
    img_about = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "Resources", "about.png"))

    notebook.add(View.Themes.AboutPage.main(), text="About", image=img_about, compound="left")
    notebook.add(View.Themes.DownloadPage.main(), text='Download', image=img_download, compound="left")
    notebook.add(View.Themes.SettingPage.main(), text='Settings', image=img_setting, compound="left")
    notebook.add(View.Themes.AccountManagePage.main(), text="Accounts", image=img_account, compound="left")


    tk.ttk.Label(root, image=img_icon).place(x=50, y=40)
    launch_button = tk.ttk.Button(root, text="Launch!", image=img_launch, compound="left", width=20, command=start)
    version_choose = tk.ttk.Combobox(root, width=20, postcommand=drop)

    launch_button.place(x=50, y=180)
    version_choose.place(x=50, y=160)

    notebook.place(x=240, y=0)
    #notebook.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)

    root.mainloop()

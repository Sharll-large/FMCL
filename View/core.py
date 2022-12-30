import os
import tkinter as tk
import tkinter.ttk
import webbrowser

import View.Themes.AboutPage
import View.Themes.AccountManagePage
import View.Themes.DownloadPage
import View.Themes.LaunchPage
import View.Themes.SettingPage
import View.ToCoreGui.LaunchGui
import View.ToCoreGui.ShowAboutGui


def getpicture(name):
    return tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "Resources", name))

def main():
    def open_kook_url():
        webbrowser.open("https://kook.top/9ccRg6")

    def open_github_repo():
        webbrowser.open("https://github.com/Sharll-large/SSCL")

    _workpath = os.path.dirname(__file__)

    root = tk.Tk()

    main_menu = tk.Menu(root)

    Urls_menu = tk.Menu(main_menu, tearoff=False)
    Urls_menu.add_command(label="Our community", command=open_kook_url)
    Urls_menu.add_command(label="Repo on github", command=open_github_repo)

    About_menu = tk.Menu(main_menu, tearoff=False)
    About_menu.add_command(label="LICENSE",command=View.ToCoreGui.ShowAboutGui.show_license)
    About_menu.add_command(label="About software", command=View.ToCoreGui.ShowAboutGui.show_about)

    img_launch = tk.PhotoImage(file=os.path.join(_workpath, "Resources", "launch.png"))
    img_download = tk.PhotoImage(file=os.path.join(_workpath, "Resources", "download.png"))
    img_setting = tk.PhotoImage(file=os.path.join(_workpath, "Resources", "option.png"))
    img_account = tk.PhotoImage(file=os.path.join(_workpath, "Resources", "account.png"))

    root.geometry('400x300')
    root.title("Sharll's Craft Launcher")
    root.resizable(False, False)
    #  root.iconphoto(False, img_icon)

    notebook = tk.ttk.Notebook(root, width=400, height=300)

    notebook.add(View.Themes.LaunchPage.main(), text="Main", image=img_launch, compound="left")
    notebook.add(View.Themes.DownloadPage.main(), text='Download', image=img_download, compound="left")
    notebook.add(View.Themes.SettingPage.main(), text='Settings', image=img_setting, compound="left")
    notebook.add(View.Themes.AccountManagePage.main(), text="Accounts", image=img_account, compound="left")

    notebook.place(x=0, y=0)

    main_menu.add_cascade(label="Websites", menu=Urls_menu)
    main_menu.add_cascade(label="About", menu=About_menu)
    root.config(menu=main_menu)
    root.mainloop()

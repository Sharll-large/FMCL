import tkinter as tk
import tkinter.ttk
import FMCLView.Const
import FMCLView.Pages.UnderDevelop
def main():
    lang = "English"
    root = tk.Tk()
    root.title("First Minecraft Launcher")
    root.geometry("640x360")
    maintab = tk.ttk.Notebook(root, width=600, height=300)

    maintab.add(FMCLView.Pages.UnderDevelop.main(), text=FMCLView.Const.get(lang, "Main.Notebook.Launch"))
    maintab.add(FMCLView.Pages.UnderDevelop.main(), text=FMCLView.Const.get(lang, "Main.Notebook.Download"))
    maintab.add(FMCLView.Pages.UnderDevelop.main(), text=FMCLView.Const.get(lang, "Main.Notebook.Option"))
    maintab.add(FMCLView.Pages.UnderDevelop.main(), text=FMCLView.Const.get(lang, "Main.Notebook.Mods"))
    maintab.add(FMCLView.Pages.UnderDevelop.main(), text=FMCLView.Const.get(lang, "Main.Notebook.Accounts"))
    maintab.add(FMCLView.Pages.UnderDevelop.main(), text=FMCLView.Const.get(lang, "Main.Notebook.Gaming"))
    maintab.add(FMCLView.Pages.UnderDevelop.main(), text=FMCLView.Const.get(lang, "Main.Notebook.About"))


    maintab.place(x=20, y=10)

    root.mainloop()

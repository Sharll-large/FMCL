import tkinter as tk
import tkinter.ttk
import tkinter.filedialog
import Core.System.CoreConfigIO
import Core.System.CoreVersionGet


def main():
    print(__file__+": load setting page")

    def conf():
        # simple write config
        Core.System.CoreConfigIO.write(setting_playername.get(), setting_dotmc.get(), setting_java.get(), setting_ram_give.get(),
                                       int(setting_threads.get()))

    def refresh():
        setting_java.delete(0, "end")
        setting_java.insert(0, Core.System.CoreConfigIO.read()["java"])
        setting_dotmc.delete(0, "end")
        setting_dotmc.insert(0, Core.System.CoreConfigIO.read()[".mc"])
        setting_playername.delete(0, "end")
        setting_playername.insert(0, Core.System.CoreConfigIO.read()["playername"])
        setting_ram_give.delete(0, "end")
        setting_ram_give.insert(0, Core.System.CoreConfigIO.read()["ram"])
        setting_threads.delete(0, "end")
        setting_threads.insert(0, Core.System.CoreConfigIO.read()["threads"])

    def choosefile():
        jpath = tk.filedialog.askopenfilenames(filetypes=[('java/javaw程序', '.exe')])
        if jpath:
            setting_java.delete(0, "end")
            setting_java.insert(0, jpath[0])

    def choosefolder():
        dpath = tk.filedialog.askdirectory()
        if dpath:
            setting_dotmc.delete(0, "end")
            setting_dotmc.insert(0, dpath)

    def javascan():
        setting_java["values"] = Core.System.CoreVersionGet.java_versions()

    # Setting page #
    setting_view = tk.ttk.Frame()
    tk.Label(setting_view, text="Java Runtime Path:").grid(column=0, row=0)
    setting_java = tk.ttk.Combobox(setting_view, show=None, postcommand=javascan, width=50)
    setting_java.grid(column=0, row=1, columnspan=2)
    setting_choose_java_button = tk.ttk.Button(setting_view, text="Browse...", command=choosefile)
    setting_choose_java_button.grid(column=1, row=0)

    # minecraft
    tk.Label(setting_view, text=".minecraft Game Folder: ").grid(column=0, row=2)
    setting_dotmc = tk.ttk.Entry(setting_view, show=None, width=50)
    setting_dotmc.grid(column=0, row=3, columnspan=2)
    setting_choose_dmc_button = tk.ttk.Button(setting_view, text="Browse...", command=choosefolder)
    setting_choose_dmc_button.grid(column=1, row=2)

    # 玩家名模块
    tk.Label(setting_view, text="playername:").grid(column=0, row=4)
    setting_playername = tk.ttk.Entry(setting_view, show=None)
    setting_playername.grid(column=1, row=4)

    # 内存分配模块
    tk.Label(setting_view, text="RAM given:").grid(column=0, row=5)
    setting_ram_give = tk.ttk.Entry(setting_view, show=None)
    setting_ram_give.grid(column=1, row=5)

    tk.Label(setting_view, text="Download threads max count:").grid(column=0, row=6)
    setting_threads = tk.ttk.Entry(setting_view, show=None)
    setting_threads.grid(column=1, row=6)

    setting_save_button = tk.ttk.Button(setting_view, text="Save", command=conf)
    setting_refresh_button = tk.ttk.Button(setting_view, text="Refresh", command=refresh)

    setting_refresh_button.grid(column=0, row=7)
    setting_save_button.grid(column=1, row=7)

    refresh()

    return setting_view

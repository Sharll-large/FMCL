import tkinter as tk
import tkinter.ttk
import Core.System.CoreConfigIO
import Core.Download.MinecraftVanillaDownload
import Core.System.CoreVersionGet
import Core.Download.ForgeLoaderInstallTask


def main():
    print(__file__+": load download page")

    def downmc():
        dotmc = Core.System.CoreConfigIO.read()[".mc"]

        Core.Download.MinecraftVanillaDownload.download(download_as.get(), download_versions.get(), dotmc, int(
            Core.System.CoreConfigIO.read()["threads"]))
        print("Ok")

    def get_versions():
        vers = []
        if r.get() == 1:
            vers.append("release")
        if b.get() == 1:
            vers.append("snapshot")
        if o.get() == 1:
            vers.append("old_alpha")
        download_versions["values"] = Core.System.CoreVersionGet.get_version_list(vers)

    def get_forge_versions():
        addon_type["values"] = Core.Download.ForgeLoaderInstallTask._get_forge_versions(download_versions.get())

    def auto_fill_download_as(a):
        print(a)
        download_as.delete(0, tk.END)
        download_as.insert(0, download_versions.get())

    download_view = tk.ttk.Frame()

    download_versions_text = tk.ttk.Label(download_view, text="Game version:")
    download_versions_text.grid(column=0, row=0)

    r = tk.IntVar()
    if_release = tk.ttk.Checkbutton(download_view, text="Release", variable=r)
    if_release.grid(column=0, row=1)

    b = tk.IntVar()
    if_beta = tk.ttk.Checkbutton(download_view, text="Snapshot", variable=b)
    if_beta.grid(column=1, row=1)

    o = tk.IntVar()
    if_old_alpha = tk.ttk.Checkbutton(download_view, text="Old Alpha", variable=o)
    if_old_alpha.grid(column=2, row=1)

    download_versions = tk.ttk.Combobox(download_view, postcommand=get_versions)
    download_versions.bind('<<ComboboxSelected>>', auto_fill_download_as)
    download_versions.grid(column=1, row=0)

    download_as_text = tk.ttk.Label(download_view, text="Download as:")
    download_as_text.grid(column=0, row=2)

    download_as = tk.ttk.Entry(download_view)
    download_as.grid(column=1, row=2)

    download_button = tk.ttk.Button(download_view, text="Download", command=downmc)
    download_button.grid(column=2, row=3)

    addon_type_text = tk.ttk.Label(download_view, text="Forge Version:")
    addon_type_text.grid(column=0, row=3)
    addon_type = tk.ttk.Combobox(download_view, postcommand=get_forge_versions)
    addon_type.bind()
    addon_type["values"] = ["Vanilla", "Optifine", "Forge Mod Loader", "Fabric Mod Loader", "Quilt Mod Loader"]
    addon_type.grid(column=1, row=3)

    return download_view

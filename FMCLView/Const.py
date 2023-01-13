def get(lang: str, thing: str):
    objects = {
        "English": {
            "Main.Notebook.Launch": "Launch",
            "Main.Notebook.Download": "Download",
            "Main.Notebook.Option": "Option",
            "Main.Notebook.About": "About FMCL",
            "Main.Notebook.Mods": "Mods download",
            "Main.Notebook.Accounts": "Account manage",
            "Main.Notebook.Gaming": "Multiplayer"
        },
        "简体中文": {
            "Main.Notebook.Launch": "启动游戏",
            "Main.Notebook.Download": "下载游戏",
            "Main.Notebook.Option": "启动器设置",
            "Main.Notebook.About": "关于FMCL",
            "Main.Notebook.Mods": "模组下载",
            "Main.Notebook.Accounts": "账户管理",
            "Main.Notebook.Gaming": "多人联机"
        }
    }
    return objects[lang][thing]
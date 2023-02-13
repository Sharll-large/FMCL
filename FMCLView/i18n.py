# coding:utf-8
# Translate by xlsx2py by pxinz.
import FMCLCore.system.CoreConfigIO as config


class Lang(object):
    def __init__(self, name: str, n2w: dict):
        self.name = name
        self.name2word = n2w

    def get(self, word):
        return self.name2word[word]


class Langs(object):
    def __init__(self, lang, default_lang, *all_langs):
        self.lang = lang
        self.default = default_lang
        self.langs = {}
        if isinstance(all_langs[0], list) or isinstance(all_langs[0], tuple):
            all_langs = all_langs[0]
        for lang in all_langs:
            self.langs[lang.name] = lang

    def get(self, word, lang=None):
        if lang and word in self.langs[lang].name2word.keys():
            return self.langs[lang].name2word[word]
        elif word in self.langs[self.lang].name2word.keys():
            return self.langs[self.lang].name2word[word]
        elif word in self.langs[self.default].name2word.keys():
            return self.langs[self.default].name2word[word]
        else:
            return False

    def get_langs(self):
        return list(self.langs.keys())

    def __getitem__(self, item):
        if isinstance(item, slice):
            if item.stop:
                # langs["word","lang"]
                return self.get(word=item.start, lang=item.stop)
            else:
                # langs["word"]
                return self.get(word=item.start)
        elif isinstance(item, str):
            word = self.get(word=item)
            if word:
                return word


lang0 = Lang(
    name="简体中文",
    n2w={
        "Launch.Ask.Launch_Game": "确定要启动版本\"{}\"吗?",
        "Launch.GUI.Choose_Account_Comb.Default": "- 选择账号 -",
        "Launch.GUI.Choose_Version_Comb.Default": "- 选择版本 -",
        "Launch.GUI.Launch_Btn": "启动游戏",
        "Launch.GUI.New_Account_Btn": "新建账号",
        "Launch.GUI.Version_List_Btn": "版本列表",
        "Launch.GUI.Version_Settings_Btn": "版本设置",
        "Launch.Tips.Error": "游戏非正常退出, 错误代码: {}\n请将FMCL.log发送给他人求助, 而不是这个窗口的截图",
        "Launch.Tips.NativeError": "版本检查出错, 请重新选择或手动检查游戏版本",
        "Launch.Tips.NullError": "版本或账号不存在!",
        "Launch.Tips.Wait": "按下确定将启动游戏, 请耐心等待游戏窗口出现, 然后畅玩Minecraft吧!",
        "Settings.Account.Ask.AccountName": "请输入账号名:",
        "Settings.Account.Ask.DeleteAccount": "你确定要删除账号\"{}\"吗?",
        "Settings.Account.Ask.Url": "请输入重定向到的url:",
        "Settings.Account.GUI.Delete_Active_Account_Btn": "删除所选账号",
        "Settings.Account.GUI.New_Microsoft_Account_Btn": "新建微软账号",
        "Settings.Account.GUI.New_Offline_Account_Btn": "新建离线账号",
        "Settings.Account.Name.AccountName": "账号名",
        "Settings.Account.Tips.AddAccountSuccess": "账号添加成功!",
        "Settings.Account.Tips.AddMicrosoftAccount": "添加Microsoft账号的方法:\n1. 打开登陆链接\n2. 完成登陆后将重定向到的url复制过来\n点击确定键打开链接",
        "Settings.Account.Tips.NetworkError": "访问出错, 请检查你输入的url与你的网络",
        "Settings.Account.Tips.UnknownError": "发生未知错误, 报错信息如下:\n{}",
        "Settings.Account.Tips.URLError": "请输入正确的url",
        "Settings.Account.Tips.Wait": "关闭该窗口后进行登陆, 请耐心等待不要关闭启动器窗口",
        "Settings.Download.GUI.Threads": "下载线程数\n(0表示单线程)",
        "Settings.Download.GUI.Source": "下载源",
        "Settings.Lang.Tips.Restart": "语言更改成功! 请重启程序以显示",
        "Settings.Launch.GUI.Boost": "启用优化参数",
        "Settings.Launch.GUI.Browse_Btn": "浏览",
        "Settings.Launch.GUI.McPath": ".minecraft路径",
        "Settings.Launch.GUI.Save_Btn": "保存",
        "Settings.Launch.GUI.Standalone": "版本隔离",
        "Settings.Launch.Tips.ChangeSuccess": "修改成功!",
        "Settings.Launch.Tips.PathError": "请输入正确的目录!",
        "Settings.Launch.Tips.RefreshAvatar": "单击刷新头像, 离线账号没有头像",
        "Settings.Launcher.GUI.AutoUpdate": "自动更新",
        "Settings.Menu.Account": "账号",
        "Settings.Menu.Download": "下载",
        "Settings.Menu.Lang": "语言",
        "Settings.Menu.Launch": "启动",
        "Settings.Menu.Launcher": "FMCL设置",
        "Update.Ask.Update": "检测到新的FMCL版本: {}\n{}\n是否需要更新?",
        "Update.Tips.UnZipWarning": "您似乎解压了FMCL, 如果你不是开发者, 并不推荐这种做法。自动更新已停用!",
    }
)
lang1 = Lang(
    name="English(US)",
    n2w={
        "Launch.Ask.Launch_Game": "Are you sure to launch version \"{}\"?",
        "Launch.GUI.Choose_Account_Comb.Default": "- Choose Account -",
        "Launch.GUI.Choose_Version_Comb.Default": "- Choose Version -",
        "Launch.GUI.Launch_Btn": "Launch Minecraft",
        "Launch.GUI.New_Account_Btn": "New Account",
        "Launch.GUI.Version_List_Btn": "Versions List",
        "Launch.GUI.Version_Settings_Btn": "Version Settings",
        "Launch.Tips.Error": "Game exited unexpectedly. Error code: {}\nPlease send FMCL.log but not this window to other who can help you.",
        "Launch.Tips.NativeError": "Can't pass version check. Please re-choose or manual check minecraft version.",
        "Launch.Tips.NullError": "Version or account doesn't exist!",
        "Launch.Tips.Wait": "We'll launch game after you click the OK button. Please wait for the game window to appear patiently, Then enjoy Minecraft!",
        "Settings.Account.Ask.AccountName": "Please entry the name of account:",
        "Settings.Account.Ask.DeleteAccount": "Are you sure to delete the account names \"{}\"?",
        "Settings.Account.Ask.Url": "Please enter the url what redirct from the page.",
        "Settings.Account.GUI.Delete_Active_Account_Btn": "Delete Active Account",
        "Settings.Account.GUI.New_Microsoft_Account_Btn": "New Microsoft Account",
        "Settings.Account.GUI.New_Offline_Account_Btn": "New Offline Account",
        "Settings.Account.Name.AccountName": "Account Name",
        "Settings.Account.Tips.AddAccountSuccess": "Account appended successfully!",
        "Settings.Account.Tips.AddMicrosoftAccount": "To add a Microsoft Account:\n1. Open login link;\n2. Copy the redircted link to FMCL;\nClick \"OK\" to open login link.",
        "Settings.Account.Tips.NetworkError": "Access Error, Please check the URL you entered and the network.",
        "Settings.Account.Tips.UnknownError": "An unknown error has occurred. Below are error messages:\n{}",
        "Settings.Account.Tips.URLError": "Please enter correct url.",
        "Settings.Account.Tips.Wait": "We'll login after you close this window, please wait us for login patiently, don't close the launcher window!",
        "Settings.Download.GUI.Threads": "Download\nThreads\n(0=Single)",
        "Settings.Download.GUI.Source": "Download Source",
        "Settings.Lang.Tips.Restart": "Lang changed successfully! Please restart the program.",
        "Settings.Launch.GUI.Boost": "Enable Boost Args",
        "Settings.Launch.GUI.Browse_Btn": "Browse",
        "Settings.Launch.GUI.McPath": ".minecraft Path",
        "Settings.Launch.GUI.Save_Btn": "Save",
        "Settings.Launch.GUI.Standalone": "Versions Standalone",
        "Settings.Launch.Tips.ChangeSuccess": "Change successfully!",
        "Settings.Launch.Tips.PathError": "Please enter correct path!",
        "Settings.Launch.Tips.RefreshAvatar": "Click to refresh avatar, offline accounts haven't avatar.",
        "Settings.Launcher.GUI.AutoUpdate": "Auto-Update",
        "Settings.Menu.Account": "Account",
        "Settings.Menu.Download": "Download",
        "Settings.Menu.Lang": "Languages",
        "Settings.Menu.Launch": "Launch",
        "Settings.Menu.Launcher": "FMCL Settings",
        "Update.Ask.Update": "Detected update of FMCL: {}\n{}\nDo you wang to update?",
        "Update.Tips.UnZipWarning": "It looks like you unzipped FMCL, if you aren’t a  developer, we don't recommand this. Auto-Update hase been deactivated!",
    }
)
langs = Langs(config.get("language"), "English(US)", lang0, lang1)

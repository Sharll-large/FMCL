import FMCLCore.System.CoreConfigIO as config


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
            return getattr(self, item)


zh_CN = Lang(name="简体中文",
             n2w={
                 # Launch页
                 "Launch.GUI.Choose_Account_Comb.Default": "- 选择账号 -",
                 "Launch.GUI.New_Account_Btn": "新建账号",
                 "Launch.GUI.Choose_Version_Comb.Default": "- 选择版本 -",
                 "Launch.GUI.Version_List_Btn": "版本列表",
                 "Launch.GUI.Version_Settings_Btn": "版本设置",
                 "Launch.GUI.Launch_Btn": "启动游戏",
                 "Launch.Ask": "确定要启动版本\"{}\"吗?",
                 "Launch.Wait": "按下确定将启动游戏, 请耐心等待游戏窗口出现, 然后畅玩Minecraft吧!",
                 "Launch.Error": "游戏非正常退出, 错误代码: {}\n错误信息:{}\n请将FMCL.log发送给他人求助, 而不是这个窗口的截图",
                 "Launch.NativeError": "版本检查出错, 请重新选择或手动检查游戏版本。",
                 "Launch.NullError": "版本或账号不存在!",
                 # Settings页
                 "Settings.Menu.Lang": "语言",
                 "Settings.Menu.Account": "账号",
                 "Settings.Lang.Tip": "语言更改成功! 请重启程序",
                 "Settings.Account.New_Microsoft_Account_Btn": "新建微软账号",
                 "Settings.Account.New_Offline_Account_Btn": "新建离线账号",
                 "Settings.Account.Delete_Active_Account_Btn": "删除所选账号",
                 "Settings.Account.Name.AccountName": "账号名",
                 "Settings.Account.Ask_AccountName": "请输入账号名",
                 "Settings.Account.Ask_DeleteAccount": "你确定要删除账号{}吗?",
                 "Settings.Account.AddAccountSuccess": "账号添加成功!",
                 "Settings.Account.NetworkError": "访问出错, 请检查你输入的url与你的网络",
                 "Settings.Account.KeyError": "回调出错, 请检查是否输入了正确的url",
                 "Settings.Account.UnknownError": "发生未知错误, 报错信息如下:\n{}",
                 "Settings.Account.URLError": "请输入正确的url",
             })

en_US = Lang(name="English(US)",
             n2w={
                 # Launch页
                 "Launch.GUI.Choose_Account_Comb.Default": "- Choose Account -",
                 "Launch.GUI.New_Account_Btn": "New Account",
                 "Launch.GUI.Choose_Version_Comb.Default": "- Choose Version -",
                 "Launch.GUI.Version_List_Btn": "Versions List",
                 "Launch.GUI.Version_Settings_Btn": "Version Settings",
                 "Launch.GUI.Launch_Btn": "Launch Minecraft",
                 "Launch.Ask": "Are you sure to launch version \"{}\"?",
                 "Launch.Wait": "We'll launch game after you click the OK button. Please wait for the game "
                                "window to appear patiently, Then enjoy Minecraft! ",
                 "Launch.Error": "Game exited unexpectedly. Error code: {}\nError message:{}\nPlease send "
                                 "FMCL.log but not this window to other who can help you.",
                 "Launch.NativeError": "Can't pass version check. Please re-choose or manual check minecraft "
                                       "version.",
                 "Launch.NullError": "Version or account doesn't exist!",
                 # Settings页
                 "Settings.Menu.Lang": "Lang",
                 "Settings.Menu.Account": "Account",
                 "Settings.Lang.Tip": "Lang changed successfully! Please restart the program.",
                 "Settings.Account.New_Microsoft_Account_Btn": "New Microsoft Account",
                 "Settings.Account.New_Offline_Account_Btn": "New Offline Account",
                 "Settings.Account.Delete_Active_Account_Btn": "Delete Active Account",
                 "Settings.Account.Name.AccountName": "Account Name",
                 "Settings.Account.Ask_AccountName": "Please entry the name of account",
                 "Settings.Account.Ask_DeleteAccount": "Are you sure to delete the account names {}?",
                 "Settings.Account.AddAccountSuccess": "Account appended successfully!",
                 "Settings.Account.NetworkError": "Access Error, Please check the URL you entered and the network.",
                 "Settings.Account.KeyError": "Callback Error, Please check that you have entered the correct URL.",
                 "Settings.Account.UnknownError": "An unknown error has occurred. Below are error messages:\n{}",
                 "Settings.Account.URLError": "Please enter correct url.",
             })
langs = Langs(config.get("language"), "English(US)", zh_CN, en_US)

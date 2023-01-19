import FMCLCore.System.CoreConfigIO as config


class Lang(object):
    def __init__(self, name: str, n2w: dict):
        self.name = name
        self.name2word = n2w

    def get(self, word):
        return self.name2word[word]


class Langs(object):
    def __init__(self, initial_lang, default_lang, *langs):
        self.lang = initial_lang
        self.default = default_lang
        self.langs = {}
        if isinstance(langs[0], list) or isinstance(langs[0], tuple):
            langs = langs[0]
        for lang in langs:
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
        return [i.name for i in self.langs]

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
                 "Launch.Tips.Ask": "确定要启动版本\"{}\"吗?",
                 "Launch.Tips.Wait": "按下确定将启动游戏, 请耐心等待游戏窗口出现, 然后畅玩Minecraft吧!",
                 "Launch.Tips.Error": "游戏非正常退出, 错误代码: {}\n错误信息:{}\n请将FMCL.log发送给他人求助, 而不是这个窗口的截图。",
                 "Launch.Tips.NativeError": "版本检查出错, 请重新选择或手动检查游戏版本。",
                 "Launch.Tips.NullError": "版本或账号不存在!",
                 # Settings页
                 "Settings.Menu1.Account": "账号设置"
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
                 "Launch.Tips.Ask": "Are you sure to launch version \"{}\"?",
                 "Launch.Tips.Wait": "We'll launch game after you click the OK button. Please wait for the game "
                                     "window to appear patiently, Then enjoy Minecraft! ",
                 "Launch.Tips.Error": "Game exited unexpectedly. Error code: {}\nError message:{}\nPlease send FMCL.log but not this window to other who can help you.",
                 "Launch.Tips.NativeError": "Can't pass version check. Please re-choose or manual check minecraft version.",
                 "Launch.Tips.NullError": "Version or account doesn't exist!",
                 # Settings页
                 "Settings.Menu1.Account": "Account"
             })
langs = Langs(config.get("language"), "English(US)", zh_CN, en_US)

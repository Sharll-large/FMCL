# coding:utf-8
# Translate by xlsx2py by pxinz.
import src.core.local.config as config


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
        "Settings.Account.Tips.AddMicrosoftAccount": "点击确定打开登录链接，设备代码会被自动添加到你的剪切板。",
        "Settings.Account.Tips.NetworkError": "访问出错, 请检查你输入的url与你的网络",
        "Settings.Account.Tips.UnknownError": "发生未知错误, 报错信息如下:\n{}",
        "Settings.Account.Tips.URLError": "请输入正确的url",
        "Settings.Account.Tips.Wait": "关闭该窗口后进行登陆, 请耐心等待不要关闭启动器窗口",
        "Settings.Download.GUI.Threads": "下载线程数\n(0表示单线程)",
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
        "Header.GUI.Launch": "Launch\n-\n启动",
        "Header.GUI.Download": "Download\n-\n资源下载",
        "Header.GUI.Settings": "Settings\n-\n设置",
        "Header.GUI.Else": "Else\n-\n其他",
        "Settings.Account.Timeout": "登录超时",
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
        "Settings.Account.Tips.AddMicrosoftAccount": "Click \"OK\" to open login link, device code will be automatically copied .",
        "Settings.Account.Tips.NetworkError": "Access Error, Please check the URL you entered and the network.",
        "Settings.Account.Tips.UnknownError": "An unknown error has occurred. Below are error messages:\n{}",
        "Settings.Account.Tips.URLError": "Please enter correct url.",
        "Settings.Account.Tips.Wait": "We'll login after you close this window, please wait us for login patiently, don't close the launcher window!",
        "Settings.Download.GUI.Threads": "Download\nThreads\n(o=Single)",
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
        "Header.GUI.Launch": "启动\n-\nLaunch",
        "Header.GUI.Download": "下载\n-\nDownload",
        "Header.GUI.Settings": "设置\n-\nSettings",
        "Header.GUI.Else": "其他\n-\nElse",
        "Settings.Account.Timeout": "Log in time out",
    }
)
lang2 = Lang(
    name="繁體中文",
    n2w={
        "Launch.Ask.Launch_Game": "確認要啓動游戲\"{}\"嗎？",
        "Launch.GUI.Choose_Account_Comb.Default": "- 選擇賬戶  - ",
        "Launch.GUI.Choose_Version_Comb.Default": "- 選擇版本 -",
        "Launch.GUI.Launch_Btn": "啓動游戲",
        "Launch.GUI.New_Account_Btn": "新建賬戶",
        "Launch.GUI.Version_List_Btn": "版本列表",
        "Launch.GUI.Version_Settings_Btn": "游戲設定",
        "Launch.Tips.Error": "游戲非正常退出，錯誤代碼是{}\n請將您的FMCL.log發送給其他人尋求幫助，而不是這個彈窗的截圖。",
        "Launch.Tips.NativeError": "版本檢查出現錯誤，請重新選擇或者手動檢查。",
        "Launch.Tips.NullError": "版本或賬戶不存在！",
        "Launch.Tips.Wait": "按下確認會啓動游戲，請耐心等待游戲窗口出現，然後游玩Minecraft！",
        "Settings.Account.Ask.AccountName": "請輸入賬戶名稱：",
        "Settings.Account.Ask.DeleteAccount": "您確定要刪除賬戶“{}”嗎？",
        "Settings.Account.Ask.Url": "請鍵入重定向鏈接。",
        "Settings.Account.GUI.Delete_Active_Account_Btn": "刪除所選賬戶",
        "Settings.Account.GUI.New_Microsoft_Account_Btn": "新建Microsoft賬戶",
        "Settings.Account.GUI.New_Offline_Account_Btn": "新建離綫賬戶",
        "Settings.Account.Name.AccountName": "賬戶昵稱",
        "Settings.Account.Tips.AddAccountSuccess": "添加賬戶成功！",
        "Settings.Account.Tips.AddMicrosoftAccount": "點擊確定打開登錄鏈接，設備代碼會被自動添加到前鐵板。",
        "Settings.Account.Tips.NetworkError": "訪問出錯，請檢查你的鏈接和網絡鏈接。",
        "Settings.Account.Tips.UnknownError": "發生未知錯誤，報錯信息如下：\n{}",
        "Settings.Account.Tips.URLError": "請輸入正確的鏈接。",
        "Settings.Account.Tips.Wait": "關閉窗口后進行登錄，請耐心等待，期間不要關閉啓動器。",
        "Settings.Download.GUI.Threads": "下載綫程並發數\n()（0為單綫程）",
        "Settings.Lang.Tips.Restart": "更改語言成功！請重啓啓動器。",
        "Settings.Launch.GUI.Boost": "使用優化游戲參數",
        "Settings.Launch.GUI.Browse_Btn": "瀏覽本地文件",
        "Settings.Launch.GUI.McPath": ".minecraft游戲路徑",
        "Settings.Launch.GUI.Save_Btn": "保存",
        "Settings.Launch.GUI.Standalone": "版本隔離",
        "Settings.Launch.Tips.ChangeSuccess": "修改成功！",
        "Settings.Launch.Tips.PathError": "請輸入正確的路徑！",
        "Settings.Launch.Tips.RefreshAvatar": "點擊此處刷新頭像，離綫賬戶沒有頭像。",
        "Settings.Launcher.GUI.AutoUpdate": "啓動器自動更新",
        "Settings.Menu.Account": "賬戶",
        "Settings.Menu.Download": "下載",
        "Settings.Menu.Lang": "語言",
        "Settings.Menu.Launch": "啓動",
        "Settings.Menu.Launcher": "啓動器設定",
        "Update.Ask.Update": "檢測到新的FMCL版本：{}\n{}\n是否進行更新？",
        "Update.Tips.UnZipWarning": "您似乎解壓了啓動器，如果你不是開發者，請不要這麽做。自動更新已經停用。",
        "Header.GUI.Launch": "Launch\n-\n啓動",
        "Header.GUI.Download": "Download\n-\n資源下載",
        "Header.GUI.Settings": "Settings\n-\n設定",
        "Header.GUI.Else": "Else\n-\n其他",
        "Settings.Account.Timeout": "登錄超時",
    }
)
langs = Langs(config.get("language"), "English(US)", lang0, lang1, lang2)

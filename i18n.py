# coding:utf-8
"""
    将xlsx文件转换i18n的py文件
    文件格式：
    Settings | ID | [语言名]
    after=   |    |
    lang=    |    |
    default= |    |
    注: 若语言名为#开头, 则不会被加入py文件
    after: 文件开头要加什么
    lang: 最初选择什么语言
    default: 当ID在当前语言没有, 自动选择什么语言替代
"""
import pandas


def main(input, output):
    data = pandas.read_excel(input)
    after = data["Settings"][0].split("=", 1)[1]
    init_lang = data["Settings"][1].split("=", 1)[1]
    default_lang = data["Settings"][2].split("=", 1)[1]
    langs = list(data.keys())
    langs.remove("Settings")
    langs.remove("ID")
    f = open(output, "w", encoding="utf-8")
    f.write("# coding:utf-8\n# Translate by xlsx2py by pxinz.\n")
    if after:
        f.write(after + "\n\n\n")
    f.write(
        'class Lang(object):\n    def __init__(self, name: str, n2w: dict):\n        self.name = name\n        '
        'self.name2word = n2w\n\n    def get(self, word):\n        return self.name2word[word]\n\n\nclass Langs('
        'object):\n    def __init__(self, lang, default_lang, *all_langs):\n        self.lang = lang\n        '
        'self.default = default_lang\n        self.langs = {}\n        if isinstance(all_langs[0], list) or isinstance('
        'all_langs[0], tuple):\n            all_langs = all_langs[0]\n        for lang in all_langs:\n            '
        'self.langs[lang.name] = lang\n\n    def get(self, word, lang=None):\n        if lang and word in self.langs['
        'lang].name2word.keys():\n            return self.langs[lang].name2word[word]\n        elif word in self.langs['
        'self.lang].name2word.keys():\n            return self.langs[self.lang].name2word[word]\n        elif word in '
        'self.langs[self.default].name2word.keys():\n            return self.langs[self.default].name2word[word]\n        '
        'else:\n            return False\n\n    def get_langs(self):\n        return list(self.langs.keys())\n\n    '
        'def __getitem__(self, item):\n        if isinstance(item, slice):\n            if item.stop:\n                # '
        'langs["word","lang"]\n                return self.get(word=item.start, lang=item.stop)\n            else:\n      '
        '          # langs["word"]\n                return self.get(word=item.start)\n        elif isinstance(item, '
        'str):\n            word = self.get(word=item)\n            if word:\n                return word\n\n\n'
    )
    l_id = 0
    ids = data["ID"]
    for lang in langs:
        if "#" != lang[0]:
            f.write("lang{} = Lang(\n    name=\"{}\",\n    n2w={{\n".format(l_id, lang))
            lang = data[lang]
            j = 0
            for i in lang:
                f.write("        \"{}\": \"{}\",\n".format(ids[j], i.replace("\"", "\\\"")))
                j += 1
            f.write("    }\n)\n")
            l_id += 1
    f.write("langs = Langs({}, {}, {})\n".format(init_lang,
                                                 default_lang,
                                                 ", ".join("lang{}".format(i) for i in range(l_id))))
    f.close()


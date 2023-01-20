import tkinter as tk
import tkinter.dialog as dialog


class DefaultStyle(object):
    default_root_args = {}
    default_label_args = {}
    default_button_args = {}
    default_entry_args = {}


class ButtonBox(tk.Tk):
    def __init__(self, message: str = "Please choose:", title: str = "Button box",
                 choices: list[str] | tuple[str,] = None, arrange: str = tk.VERTICAL, root_args: dict = None,
                 label_args: dict = None, button_args: dict = None):
        super(ButtonBox, self).__init__()
        # 初始化样式
        root_args = (root_args if root_args else DefaultStyle.default_root_args)
        label_args = (label_args if label_args else DefaultStyle.default_label_args)
        self.button_args = (button_args if button_args else DefaultStyle.default_button_args)
        # 默认选项与变量存储
        if choices is None:
            choices = ["A", "B"]
        self.arrange = arrange
        self.button_count = 0
        # 回调
        self.r = None
        # 布局
        self.attributes("-toolwindow", 2)
        self.root = tk.Frame(self, **root_args)
        self.root.pack(fill="both", expand=True)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", lambda: self.ret(None))
        tk.Label(self.root, text=message, **label_args).grid(
            column=0, row=0, columnspan=(len(choices) if self.arrange == tk.HORIZONTAL else 1), padx=10, pady=5
        )
        for choice in choices:
            self.create_button(choice)

    def create_button(self, text: str):
        # 创建按钮
        btn = tk.Button(self.root, text=" {} ".format(text), command=lambda: self.ret(text), **self.button_args)

        btn.grid(
            column=(self.button_count if self.arrange == tk.HORIZONTAL else 0),
            row=(self.button_count + 1 if self.arrange == tk.VERTICAL else 1),
            padx=(40 if self.arrange == tk.VERTICAL else 10),
            pady=(0, 5)
        )
        self.button_count += 1

    def ret(self, ret):
        # 回调
        self.r = ret
        self.quit()
        self.destroy()

    def main(self):
        # 运行
        self.mainloop()
        return self.r


def button_box(message: str = "Please choose:", title: str = "Button box",
               choices: list[str] | tuple[str,] = None, arrange: str = tk.VERTICAL, root_args: dict = None,
               label_args: dict = None, button_args: dict = None) -> str:
    return ButtonBox(message, title, choices, arrange, root_args, label_args, button_args).main()


class EntryBox(tk.Tk):
    def __init__(self, message: str = "Please input:", title: str = "Entry box",
                 entries: str | list[str] | tuple[str,] = None,
                 defaults: str | list[str] | tuple[str,] = None,
                 root_args: dict = None, label_args: dict = None,
                 entry_args: dict = None, button_args: dict = None):
        super(EntryBox, self).__init__()
        # 初始化样式
        root_args = (root_args if root_args else DefaultStyle.default_root_args)
        self.label_args = (label_args if label_args else DefaultStyle.default_label_args)
        self.entry_args = (entry_args if entry_args else DefaultStyle.default_entry_args)
        button_args = (button_args if button_args else DefaultStyle.default_button_args)
        # 默认选项与变量存储
        if entries is None:
            entries = ("item",)
        elif isinstance(entries, str):
            entries = (entries,)
        if defaults is None:
            defaults = ["" for i in range(len(entries))]
        elif isinstance(defaults, str):
            defaults = (defaults,) + tuple("" for i in range(len(entries) - 1))
        elif len(defaults) < len(entries):
            defaults = tuple(defaults) + tuple("" for i in range(len(entries) - len(defaults)))
        self.entries_count = 0
        self.entries = []
        # 回调
        self.r = None
        # 布局
        self.attributes("-toolwindow", 2)
        self.root = tk.Frame(self, **root_args)
        self.root.pack(fill="both", expand=True)
        self.title(title)
        tk.Label(self.root, text=message, **self.label_args).grid(
            column=0, row=0, columnspan=2, padx=10, pady=5
        )
        for i in range(len(entries)):
            self.create_entry(entries[i], defaults[i])
        self.protocol("WM_DELETE_WINDOW", lambda: self.ret(None))
        tk.Button(
            self.root, text="OK", command=lambda: self.ret([entry.get() for entry in self.entries]),
            **button_args
        ).grid(column=0, row=self.entries_count + 1, columnspan=2, padx=10, pady=(0, 5))

    def create_entry(self, name: str, default: str):
        tk.Label(self.root, text=name, justify="right", **self.label_args).grid(
            column=0, row=self.entries_count + 1, padx=(10, 5), pady=(0, 5)
        )
        entry = tk.Entry(self.root)
        entry.insert(0, default)
        entry.grid(column=1, row=self.entries_count + 1, padx=(5, 10), pady=(0, 5))
        self.entries_count += 1
        self.entries.append(entry)

    def ret(self, ret):
        self.r = ret
        self.quit()
        self.destroy()

    def main(self):
        self.mainloop()
        return self.r


def entry_box(message: str = "Please input:", title: str = "Entry box",
              entries: str | list[str] | tuple[str,] = None,
              defaults: str | list[str] | tuple[str,] = None,
              root_args: dict = None, label_args: dict = None,
              entry_args: dict = None, button_args: dict = None) -> list:
    return EntryBox(message, title, entries, defaults, root_args, label_args, entry_args, button_args).main()

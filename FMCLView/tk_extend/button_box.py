import tkinter as tk


class ButtonBox(tk.Tk):
    default_root_args = {}
    default_text_args = {}
    default_btn_args = {}

    def __init__(self, message: str = "Please choose:", title: str = "Button box", choices: list | tuple = None,
                 root_args: dict = None, text_args: dict = None, btn_args: dict = None):
        super().__init__()
        root_args = (root_args if root_args else ButtonBox.default_root_args)
        text_args = (text_args if text_args else ButtonBox.default_text_args)
        self.btn_args = (btn_args if btn_args else ButtonBox.default_btn_args)
        if choices is None:
            choices = ["A", "B"]
        self.r = None
        self.root = tk.Frame(self, **root_args)
        self.root.pack()
        self.title(title)
        tk.Label(self.root, text=message, **text_args).pack()
        for choice in choices:
            self.create_button(choice)

    def create_button(self, text: str):
        btn = tk.Button(self.root, text=text, command=lambda: self.ret(text), **self.btn_args)
        btn.pack(padx=40, pady=5, expand=True, fill=tk.BOTH)

    def ret(self, ret):
        self.r = ret
        self.destroy()

    def main(self):
        self.mainloop()
        return self.r


def buttonbox(message: str = "Please choose:", title: str = "Button box", choices: list | tuple = None,
              root_args: dict = None, text_args: dict = None, btn_args: dict = None):
    if choices is None:
        choices = ["A", "B"]
    return ButtonBox(message, title, choices, root_args, text_args, btn_args).main()

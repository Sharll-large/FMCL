# coding:utf-8
"""
    一键添加# coding:utf-8
"""
import os


def add_comment(path):
    for i in os.walk(path):
        for j in i[2]:
            if j.split(".")[-1] == "py":
                pth = os.path.join(i[0], j)
                with open(pth, "r", encoding="utf-8") as f:
                    content: str = f.read()
                if content.split("\n", 1)[0] != "# coding:utf-8":
                    with open(pth, "w", encoding="utf-8") as f:
                        f.write("# coding:utf-8\n")
                        f.write(content)
                        print("Added comment: " + pth)


if __name__ == '__main__':
    add_comment("../")

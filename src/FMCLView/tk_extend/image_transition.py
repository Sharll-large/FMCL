# coding:utf-8
"""
    裁剪PhotoImage图片
"""
import tkinter


def to_hex(r: int, g: int, b: int) -> str:
    return "#{0:0>2}{1:0>2}{2:0>2}".format(hex(r)[2:], hex(g)[2:], hex(b)[2:])


def cut(image: tkinter.PhotoImage, result: tkinter.PhotoImage,
        x1: int, y1: int,
        x2: int, y2: int) -> tkinter.PhotoImage:
    """
        裁剪图片
        :param image: 原图
        :param result: 可恶的tkinter在函数结束后就tm把result给回收了, 所以你得传个指针进来
        :param x1: 左上角x
        :param y1: 左上角y
        :param x2: 右下角x
        :param y2: 右下角y
        :return: 被裁剪好的图片
    """
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    width = x2 - x1
    height = y2 - y1
    # 先提取pixel后放置pixel, 这样可以原图转换
    pixels = [[to_hex(*image.get(x, y)) for y in range(y1, y2)] for x in range(x1, x2)]
    [[result.put(pixels[x][y], (x, y)) for y in range(height)] for x in range(width)]
    return result


def resize(image: tkinter.PhotoImage, result: tkinter.PhotoImage,
           from_width: int, from_height: int,
           to_width: int, to_height: int) -> tkinter.PhotoImage:
    """
        缩放图片
        :param image: 原图
        :param result: 可恶的tkinter在函数结束后就tm把result给回收了, 所以你得传个指针进来
        :param from_width: 原宽度
        :param from_height: 原高度
        :param to_width: 目标宽度
        :param to_height: 目标高度
        :return: 缩放后的图片
    """
    # 先提取pixel后放置pixel, 这样可以原图转换
    pixels = [[to_hex(*image.get(x, y)) for y in range(from_height)] for x in range(from_width)]
    for x in range(to_width):
        for y in range(to_height):
            result.put(pixels[x * from_width // to_width][y * from_height // to_height], (x, y))
    return result

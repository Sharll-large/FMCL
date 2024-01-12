# coding:utf-8
"""
    Struct 结构体
    可直接用需要的键来创建, 用于储存数据
"""
from typing import Any, Dict, Iterable, List

__all__ = ["StructKeysMissingException", "BaseStruct", "struct"]


class StructKeysMissingException(BaseException):
    """
        当结构体初始化缺少键时抛出
    """

    def __init__(self, missing_keys):
        super().__init__(f"Struct keys missing: {', '.join(missing_keys)}.")


class BaseStruct(dict):
    """
        结构体父类, 用于定义基础功能
    """

    def __init__(self, keys: Iterable[str], args: List[Any], kwargs: Dict[str, Any]):
        super().__init__()
        keys_cp = list(keys)
        for (k, v) in kwargs.items():
            if k in keys_cp:
                self[k] = v
                keys_cp.remove(k)
        for (k, v) in list(zip(keys_cp, args)):
            self[k] = v
            keys_cp.remove(k)
        if keys_cp:
            raise StructKeysMissingException(keys_cp)

    def __getattr__(self, item):
        return self[item]


def struct(keys: List[str]):
    """
        创建结构体子类
        :param keys: 子类的键
        :return: 子类
    """

    class _S(BaseStruct):
        """
            结构体子类, 用于自定义键
        """

        def __init__(self, *args, **kwargs):
            super().__init__(keys, args, kwargs)

    return _S


if __name__ == '__main__':
    main_struct = struct(["a", "b"])
    print(main_struct(1, 2).a)
    print(main_struct(2, 3).b)

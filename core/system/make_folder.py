# coding:utf-8
# TODO: 重构为单例
import os


def make_dir(path_):
    if not os.path.exists(path_) and path_ != '':
        os.mkdir(path_)


def make_long_dir(path_: str):
    path_ = os.path.normpath(path_).split(os.sep)
    path__ = path_[0]
    make_dir(path__)
    for d in path_[1:]:
        path__ += os.sep + d
        make_dir(path__)
    del path_
    del path__


def make_mc_dir(path: str):
    make_long_dir(path)
    make_long_dir(os.path.join(path, "versions"))

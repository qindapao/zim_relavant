# -*- coding: utf-8 -*-

# 这个文件的作用是删除范围内的文件

import sys
import pathlib
import re

TEXT, PAPER_NAME = sys.argv[1], sys.argv[2]


def deal_pics():
    # zim中所有页面名字都去掉了下划线，要转换过来
    real_path = pathlib.Path.cwd().joinpath(PAPER_NAME.split(':')[-1].replace(' ', '_'))
    pic_iter = re.finditer(r"\{\{\.\\([^{]+\.(?:png|jpg|jpeg|svg))\}\}", TEXT, re.M)
    for sub_pic in pic_iter:
        pic_path = real_path.joinpath(sub_pic.group(1))
        pic_path.unlink(missing_ok=True)


if __name__ == '__main__':
    deal_pics()


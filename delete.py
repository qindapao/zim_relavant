# -*- coding: utf-8 -*-

# 所有的参数说明
#   %f 作为临时文件的页面源
#   %d 当前也的附件目录
#   %s 真实页面源文件(假如有的话)
#   %p 页面名
#   %n 笔记本位置(文件或文件夹)
#   %D 文档根目录(假如有的话)
#   %t 光标下选定的文本或者单词
#   %T 包含维基格式的选定文本
#
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

# 工具脚本配置方法：
#   工具 -> 自定义工具 -> 编辑自定义工具
#       名称: 删除选择附件
#       命令: python "%D/zim/tools/delete.py" "%T" "%p"
#
#       下面的复选框选择情况:
#           [ ] 命令不修改数据
#           [v] 执行结果会替换当前所选
#           [v] 显示在工具栏中


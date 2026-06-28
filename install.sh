#!/usr/bin/env bash

ZIM_SETUP_FINISH_FILE="zim_setup_finish.do_not_remove_me"

# 安装各种文件
install_files ()
{
    [[ -f ../"$ZIM_SETUP_FINISH_FILE" ]] || {
        # 拷贝批处理文件
        cp -f ./zim.bat ../zim/

        # 拷贝主题文件
        cp -rf ./gtk-3.0 ../zim/config/

        # 拷贝样式文件
        mv -f ../zim/config/zim/style.conf ../zim/config/zim/style.bak
        cp -f ./style.conf ../zim/config/zim/

        #  安装通过 vim 打开当前笔记
        cp -f ./open_in_gvim.py ../zim/_internal/share/zim/plugins/
        
        # 安装附件删除小工具
        mkdir -p ../zim/tools
        cp -f ./delete.py ../zim/tools/

        # 安装更加好看的 Print.html
        mv -f ../zim/_internal/share/zim/templates/html/Print.html ../zim/_internal/share/zim/templates/html/Print.bak
        cp -f ./Print.html ../zim/_internal/share/zim/templates/html/Print.html

        # 安装 svgconvertprinttobrowser.py 插件，正常显示能搜索的SVG图表
        cp -f ./svgconvertprinttobrowser.py ../zim/_internal/share/zim/plugins/

    }
}

install_files

# 需要手动配置的步骤
#   1. 在首选项的插件中，把 Gvim 选上。
#   2. 在快捷键的绑定中，把 open_in_gvim 绑定为 Ctrl + Shift + G
#   3. 打开 zim，然后 工具 -> 自定义工具 -> 编辑自定义工具
#       名称: 删除选择附件
#       命令: python "%D/zim/tools/delete.py" "%T" "%p"
#
#       下面的复选框选择情况:
#           [ ] 命令不修改数据
#           [v] 执行结果会替换当前所选
#           [v] 显示在工具栏中
#   4. 在首选项的插件中，把 svg_print_to_browser 选择上
#   5. 在快捷键的绑定中，把 svg_print_to_browser 绑定成 Ctrl + Shift + P
#       注意：这样操作后，原始的 print_to_browser 可能就失效了，不过没有关系，后面我们就使用 svg_print_to_browser 即可。
#


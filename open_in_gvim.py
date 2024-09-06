# -*- coding: utf-8 -*-
# This is a zim plugin to open the current file in gvim and jump to the current line
# You need to have emacsclient installed and running
# You can change the emacsclient path and arguments below
# You can also change the toolbar icon and the tooltip below

from zim.plugins import PluginClass
from zim.gui.pageview import PageViewExtension
from zim.actions import action
from zim.gui.widgets import ErrorDialog
import logging
import subprocess
import os

# gvim是需要设置环境变量才能找到的
os.environ['PATH'] += r";D:\programs\Vim\vim91"
logger = logging.getLogger('zim.plugins.gvim')

# The path and arguments of emacsclient
GVIMLIENT = 'gvim'

# The toolbar icon and the tooltip of the plugin
TOOLBAR_ICON = 'gtk-open' # You can use any stock icon or a custom icon file
TOOLBAR_TOOLTIP = 'Open in Gvim' # T: tooltip

class EmacsPlugin(PluginClass):

    plugin_info = {
        'name': 'Gvim', # T: plugin name
        'description': 'This plugin adds a toolbar button to open the current file in gvim and jump to the current line', # T: plugin description
        'author': 'Copilot', # T: plugin author
        'help': 'Plugins:Gvim',
    }

class GvimPageViewExtension(PageViewExtension):

    def __init__(self, plugin, pageview):
        PageViewExtension.__init__(self, plugin, pageview)
        self.connectto(pageview, 'page-changed')

    def on_page_changed(self, pageview, page, path):  # 新增这个方法
        self._set_action_sensitivity()

    def teardown(self):
        self.disconnect_from(self.pageview)

    def on_load_page(self, pageview, page):
        self._set_action_sensitivity()

    def _set_action_sensitivity(self):
        # Only enable the action when the page is not a placeholder
        page = self.pageview.page
        self.actiongroup.set_sensitive(not page.is_placeholder)

    @action(TOOLBAR_TOOLTIP, icon=TOOLBAR_ICON) # T: tooltip
    def open_in_gvim(self):
        # Get the current page and its file path
        page = self.pageview.page
        file_path = page.source_file.path

        # Get the current line number from the text buffer
        textview = self.pageview.textview
        buffer = textview.get_buffer()
        cursor = buffer.get_insert()
        buffer_iter = buffer.get_iter_at_mark(cursor)
        cur_line_number = buffer_iter.get_line()
        line_number = cur_line_number + 5

        # 防止代码中的'''导致得代码行号不准
        # :TODO: 下面的代码并没有作用,因为这里迭代的文本也是不包含收缩的字符的
        start_iter = buffer.get_start_iter()
        while start_iter.get_line() < cur_line_number:
            end_iter = start_iter.copy()
            end_iter.forward_to_line_end()
            line_text = start_iter.get_text(end_iter)
            if line_text.rstrip() == "'''":
                line_number += 1
            start_iter.forward_line()


        # Run gvimclient with the file path and the line number
        try:
            # :TODO: 如果出现问题,可能需要指定emacs的相关环境变量的路径($env:HOME = "C:\Users\q00208337\AppData\Roaming")
            #        但由于emacs是通过已有服务打开,所以不会有问题,gvim可能需要设置环境变量
            # :TODO: 当前有个问题是图标没有显示出来
            # :TODO: gvim也可以类似处理
            subprocess.Popen([GVIMLIENT, '--remote', f'+{line_number}', file_path])
        except:
            # Show an error dialog if something goes wrong
            ErrorDialog(self.pageview, 'Failed to run gvimclient').run()



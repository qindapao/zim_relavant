# -*- coding: utf-8 -*-
from zim.plugins import PluginClass
from zim.gui.pageview import PageViewExtension
from zim.actions import action
from zim.gui.widgets import ErrorDialog
import logging
import subprocess
import os

# 1. 安全地安全添加环境变量
GVIM_PATH = r"D:\programs\Vim\vim91"
if GVIM_PATH not in os.environ['PATH']:
    os.environ['PATH'] = os.environ['PATH'].rstrip(os.pathsep) + os.pathsep + GVIM_PATH

logger = logging.getLogger('zim.plugins.gvim')

# 如果加入 PATH 还是报错，可以直接把这里改成 r"D:\programs\Vim\vim91\gvim.exe"
GVIMLIENT = 'gvim' 

TOOLBAR_ICON = 'zim-page' # 更换为 Zim 较通用的图标
TOOLBAR_TOOLTIP = 'Open in Gvim' 

class GvimPlugin(PluginClass): # 重命名类名，避免与 Emacs 混淆
    plugin_info = {
        'name': 'Gvim', 
        'description': 'This plugin adds a toolbar button to open the current file in gvim and jump to the current line', 
        'author': 'Qindapao', 
        'help': 'Plugins:Gvim',
    }

class GvimPageViewExtension(PageViewExtension):

    def __init__(self, plugin, pageview):
        PageViewExtension.__init__(self, plugin, pageview)
        self.connectto(pageview, 'page-changed')

    def on_page_changed(self, pageview, page, path):  
        self._set_action_sensitivity()

    def teardown(self):
        self.disconnect_from(self.pageview)

    def on_load_page(self, pageview, page):
        self._set_action_sensitivity()

    def _set_action_sensitivity(self):
        page = self.pageview.page
        self.actiongroup.set_sensitive(not page.is_placeholder)

    @action(TOOLBAR_TOOLTIP, icon=TOOLBAR_ICON) 
    def open_in_gvim(self):
        page = self.pageview.page
        file_path = page.source_file.path

        textview = self.pageview.textview
        buffer = textview.get_buffer()
        cursor = buffer.get_insert()
        buffer_iter = buffer.get_iter_at_mark(cursor)
        cur_line_number = buffer_iter.get_line()
        line_number = cur_line_number + 5 # 保持你原本的偏移逻辑

        # 尝试调用 gvim
        try:
            # 加上 shell=True 允许 Windows 更好地检索环境变量
            subprocess.Popen([GVIMLIENT, '--remote', f'+{line_number}', file_path], shell=True)
        except Exception as e:
            logger.exception("Failed to launch gvim")
            # 这里的弹窗会带上具体的报错原因（例如：[Error 2] 系统找不到指定的文件）
            ErrorDialog(self.pageview, f'Failed to run gvimclient\nError: {e}').run()


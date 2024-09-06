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
import time

logger = logging.getLogger('zim.plugins.refresh_and_move')

# The path and arguments of emacsclient
GVIMLIENT = 'gvim'

# The toolbar icon and the tooltip of the plugin
TOOLBAR_ICON = 'gtk-open' # You can use any stock icon or a custom icon file
TOOLBAR_TOOLTIP = 'refresh and move' # T: tooltip

class EmacsPlugin(PluginClass):

    plugin_info = {
        'name': 'refresh_and_move', # T: plugin name
        'description': 'refresh and move', # T: plugin description
        'author': 'qindapao', # T: plugin author
        'help': 'Plugins:refresh_and_move',
    }

class RefreshAndMovePageViewExtension(PageViewExtension):

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
    def refresh_and_move(self):
        self.pageview.reload_page()
        # :TODO:位置不准确的时候需要向右然后向左移动,目前不知道调用哪个函数
        # set_cursor_pos 函数可能是没有正常导出，无法调用到


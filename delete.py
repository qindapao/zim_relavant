# -*- coding: utf-8 -*-
# This is a zim plugin to delete only the selected text and the attachments within that selection.

from zim.plugins import PluginClass
from zim.gui.pageview import PageViewExtension
from zim.actions import action
from zim.gui.widgets import ErrorDialog, QuestionDialog
import logging
import pathlib
import re

logger = logging.getLogger('zim.plugins.delete_selection_scope')

TOOLBAR_ICON = 'gtk-delete' 
TOOLBAR_TOOLTIP = '删除选中范围内的文本和附件' 

class DeleteSelectionScopePlugin(PluginClass):
    plugin_info = {
        'name': 'Delete Selection Scope', 
        'description': '通过行号比对，完美兼容 Zim 0.77.0 删除选区文本及其中包含的图片/附件', 
        'author': '秦大炮', 
        'help': 'Plugins:DeleteSelectionScope',
    }

class DeleteSelectionScopePageViewExtension(PageViewExtension):

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
        self.actiongroup.set_sensitive(page is not None and not page.is_placeholder)

    @action(TOOLBAR_TOOLTIP, icon=TOOLBAR_ICON) 
    def delete_selected_scope(self):
        page = self.pageview.page
        if not page or not page.source_file:
            return

        # 1. 获取选中的文本区域行号
        textview = self.pageview.textview
        buffer = textview.get_buffer()
        
        has_selection = buffer.get_selection_bounds()
        if not has_selection:
            ErrorDialog(self.pageview, '未检测到选区，请先用鼠标选中一段文本！').run()
            return
            
        start_iter, end_iter = has_selection
        
        # 精准拿到鼠标框选的起始行和结束行（从 0 开始算）
        start_line = start_iter.get_line()
        end_line = end_iter.get_line()

        # 2. 弹出确认，防止误删
        dialog = QuestionDialog(
            self.pageview,
            f"确定要删除选中行（第 {start_line+1} 行 到 第 {end_line+1} 行）内的文本及包含的附件吗？"
        )
        if not dialog.run():
            return 

        try:
            # 3. 定位附件文件夹路径
            txt_file_path = pathlib.Path(page.source_file.path)
            current_dir = txt_file_path.parent
            paper_name = page.name
            real_path = current_dir.joinpath(paper_name.split(':')[-1].replace(' ', '_'))

            # 4. 读取底层源码（因为 GTK 内存里吞图，物理源码永远说真话）
            if txt_file_path.exists():
                with open(txt_file_path, 'r', encoding='utf-8') as f:
                    source_lines = f.readlines()

                # 5. 精准切片：只在用户选中的这几行源码里抓取图片
                # end_line + 1 是为了包含最后一行
                selected_source_lines = source_lines[start_line:end_line + 1]
                source_text_content = "".join(selected_source_lines)

                # 6. 在选中的源码区间里匹配图片
                pic_iter = re.finditer(r"\{\{\.[\\/]([^{]+\.(?:png|jpg|jpeg|svg))\}\}", source_text_content, re.M)
                
                if real_path.exists():
                    deleted_count = 0
                    for sub_pic in pic_iter:
                        matched_filename = sub_pic.group(1).replace('\\', '/')
                        clean_filename = matched_filename.split('/')[-1]
                        pic_path = real_path.joinpath(clean_filename)
                        
                        if pic_path.exists():
                            pic_path.unlink()
                            deleted_count += 1
                    logger.info(f"成功物理删除了选区内的 {deleted_count} 个附件。")

            # 7. 无论源码对齐如何，界面选中的文本和图片必须立刻抹掉
            buffer.delete(start_iter, end_iter)

        except Exception as e:
            logger.exception("删除选区附件时发生错误")
            ErrorDialog(self.pageview, f'删除失败\n错误原因: {e}').run()

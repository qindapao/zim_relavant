
# Copyright 2008-2020 Jaap Karssenberg <jaap.karssenberg@gmail.com>

'''Plugin to serve as work-around for the lack of printing support'''
import urllib.parse
import re
from urllib.request import unquote
from gi.repository import Gtk

from functools import partial


from zim.plugins import PluginClass
from zim.actions import action
from zim.newfs import TmpFile

import zim.templates
import zim.formats

from zim.export.template import ExportTemplateContext
from zim.export.linker import StaticExportLinker

from zim.gui.pageview import PageViewExtension
from zim.gui.applications import open_url

from zim.plugins.tasklist.gui import TaskListWindowExtension

import logging
logger = logging.getLogger('zim.plugins.myplugin')

def deal_div(origin_str):
    obj_iter = re.finditer("(<div style='[^<]+)('>)", origin_str)
    right, final_str, last_part = 0, '', origin_str
    for obj_sub in obj_iter:
        if obj_sub.span()[0] > right:
            final_str += origin_str[right:obj_sub.span()[0]]
        right = obj_sub.span()[1]
        part_1, part_2 = obj_sub.group(1), obj_sub.group(2)
        semicolon_fit = ';' if part_1[-1] != ';' else ''
        final_str += part_1 + semicolon_fit + 'margin: 0; font-family:"sarasa mono sc"; white-space: pre;' + part_2
        last_part = origin_str[right:]
    final_str += last_part
    return final_str


class PrintToBrowserPlugin(PluginClass):

	plugin_info = {
		'name': _('my plugin'), # T: plugin name
		'description': _('''\
qinqing modify fo future use
'''), # T: plugin description
		'author': 'Jaap Karssenberg',
		'help': 'Plugins:Print to Browser'
	}

	def print_to_file(self, notebook, page):
		file = TmpFile('print-to-browser.html', persistent=True, unique=False)
		template = zim.templates.get_template('html', 'Print')

		linker_factory = partial(StaticExportLinker, notebook, template.resources_dir)
		dumper_factory = zim.formats.get_format('html').Dumper # XXX
		context = ExportTemplateContext(
			notebook, linker_factory, dumper_factory,
			page.basename, [page]
		)

		lines = []
		template.process(lines, context)
		new_lines = []

		for single_line in lines:
			svg_iter = re.finditer("<p>\r?\n<img src=\"([^<]+\.svg)\">\r?\n</p>", single_line)
			right, final_str, last_part = 0, '', single_line
			for svg_sub in svg_iter:
				if svg_sub.span()[0] > right:
					final_str += deal_div(single_line[right:svg_sub.span()[0]])
				right = svg_sub.span()[1]
				real_path = urllib.parse.unquote(svg_sub.group(1)[8:])
				with open(real_path, mode='r', encoding='utf8') as svg_text:
					final_str += svg_text.read()
				last_part = single_line[right:]
			final_str += deal_div(last_part)
			new_lines.append(final_str)
			
		file.writelines(new_lines)

		return file


class PrintToBrowserPageViewExtension(PageViewExtension):

	@action(_('_Print to Browser'), accelerator='<Primary>P', menuhints='page') # T: menu item
	def print_to_browser(self, page=None):
		notebook = self.pageview.notebook
		page = page or self.pageview.page
		file = self.plugin.print_to_file(notebook, page)
		open_url(self.pageview, 'file://%s' % file) # XXX
			# Try to force web browser here - otherwise it goes to the
			# file browser which can have unexpected results


class PrintTaskListWindowExtension(TaskListWindowExtension):

	@action(_('_Print'), icon='document-print-symbolic', menuhints='headerbar:tools:is_important', tooltip=_('Print tasklist to browser')) # T: menu item
	def print_tasklist(self):
		html = self.window.tasklisttreeview.get_visible_data_as_html()
		file = TmpFile('print-to-browser.html', persistent=True, unique=False)
		file.write(html)
		open_url(self.window, 'file://%s' % file) # XXX
			# Try to force web browser here - otherwise it goes to the
			# file browser which can have unexpected results

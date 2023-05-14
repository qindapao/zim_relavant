
# Copyright 2008-2020 Jaap Karssenberg <jaap.karssenberg@gmail.com>

'''Plugin to serve as work-around for the lack of printing support'''

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


class PrintToBrowserPlugin(PluginClass):

	plugin_info = {
		'name': _('Print to Browser Convert Svg'), # T: plugin name
		'description': _('''\
This plugin provides a workaround for the lack of
printing support in zim. It exports the current page
to html and opens a browser. Assuming the browser
does have printing support this will get your
data to the printer in two steps. 

This is a core plugin shipping with zim.
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
			# <img src="file:///E:/zim_notebook/svg%E6%B5%8B%E8%AF%95/bob.svg">
			svg_iter = re.finditer("<img src=\"([^<]+\.svg)\">", single_line)
			right, final_str, svg_exist_flag, last_part = 0, '', False, ''
			for sub_svg in svg_iter:
				svg_exist_flag = True
				if sub_svg.span()[0] > right:
					final_str += single_line[right:sub_svg.span()[0]]
				right = sub_svg.span()[1]
				svg_path = unquote(sub_svg.group(1)[8:])
				with open(svg_path, mode='r', encoding='utf8') as svg_text:
					final_str += svg_text.read()
				last_part = single_line[right:]
			if svg_exist_flag and last_part:
				final_str += last_part
			if not svg_exist_flag:
				final_str += single_line
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

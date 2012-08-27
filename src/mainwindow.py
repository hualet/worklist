#!/usr/bin/env python 


import os
import datetime
import logging
from gi.repository import Gtk, Pango

from dataparse import WorkListParser
from datatype import *
from util.constants import *
from util.debug import log_func
from util.worklist_settings import WorkListSettings
from widgets.dialogs import QuestionDialog
from widgets.preference import PreferenceDialog
from widgets.time_picker import TimePicker

class MainWindow():

	log = logging.Logger('WorkList')

	def __init__(self, master):
		

		self.parser = master.work_dataparser
		self.worklist = self.parser._works

		builder = Gtk.Builder()
		builder.add_from_file(os.path.join(DATA_PATH, 'ui/WorkList.glade'))

		self.win = builder.get_object('window1')
		self.win.set_default_size(800, 400)
		try:
			self.win.set_icon_from_file(os.path.join(DATA_PATH, 'icons', 'WorkList.png'))
		except Exception:
			print "There's no picture at all."

		agr = Gtk.AccelGroup()
		self.win.add_accel_group(agr)

		#self.toolbar = builder.get_object('toolbar')
		#context = self.toolbar.get_style_context()
		#context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
		self.tool_new = builder.get_object('toolbutton1')
		self.tool_new.connect('clicked', self.tool_new_clicked)
		key_new, mod_new = Gtk.accelerator_parse("<Control>N")
		self.tool_new.add_accelerator('clicked', agr, key_new, mod_new, Gtk.AccelFlags.VISIBLE)
		self.tool_save = builder.get_object('toolbutton2')
		self.tool_save.connect('clicked', self.tool_save_clicked)
		key_save, mod_save = Gtk.accelerator_parse("<Control>S")
		self.tool_save.add_accelerator('clicked', agr, key_save, mod_save, Gtk.AccelFlags.VISIBLE)

		self.tool_preference = builder.get_object('preference')
		self.tool_preference.connect('clicked', self.tool_preference_clicked)
		key_preference, mod_preference = Gtk.accelerator_parse("<Control>P")
		self.tool_preference.add_accelerator('clicked', agr, key_preference, mod_preference, Gtk.AccelFlags.VISIBLE)

		self.tool_about = builder.get_object('about')
		self.tool_about.connect('clicked', self.tool_about_clicked)
		key_about, mod_about = Gtk.accelerator_parse("<Control>A")
		self.tool_about.add_accelerator('clicked', agr, key_about, mod_about, Gtk.AccelFlags.VISIBLE)



		self.unlock_button = builder.get_object('unlock')
		self.unlock_button.connect('toggled', self.unlock_button_toggled)


		paned = builder.get_object('paned')
		paned.set_position(200)

		self.his_scroll = Gtk.ScrolledWindow()
		self.his_align = builder.get_object('alignment1')
		self.his_align.add(self.his_scroll)

		self.treeview = self.create_tree_view()
		self.his_scroll.add(self.treeview)

		self.title_entry = builder.get_object('entry1')
		self.title_entry.set_editable(False)
		self.title_entry.set_alignment(0.5)
		self.delete_button = builder.get_object('delete')
		self.delete_button.connect('clicked', self.delete_button_clicked)

		self.alarm_entry = builder.get_object('alarm')
		self.alarm_entry .set_editable(False)
		self.alarm_entry .set_alignment(0.5)
		self.reset_button = builder.get_object('reset')
		self.reset_button.connect('clicked', self.reset_button_clicked)

		self.text_view = Gtk.TextView()
		self.text_view.set_editable(False)
		font_name = WorkListSettings.get_value('editor-font')
		self.view_font = Pango.FontDescription(font_name)
		self.text_view.modify_font(self.view_font)
		self.con_scroll = Gtk.ScrolledWindow()
		self.con_scroll.set_property('margin-right', 5)
		self.con_scroll.add(self.text_view)
		self.con_box = builder.get_object('box3')
		self.con_box.pack_start(self.con_scroll, True, True, 3)

		self.status_bar = builder.get_object('statusbar')

		try:
			self.show_work(self.worklist[0])
			self.current_work = self.worklist[0]
		except IndexError:
			self.show_nothing()
			self.current_work = None

		self.win.connect('delete-event', self.win_destroy)
		self.win.show_all()

	def win_destroy(self, widgets, event):
		self.win.destroy()

	def enable_edit(self, value):
		if value:
			self.win.set_title('*WorkList')
		else:
			self.win.set_title('WorkList')
		self.unlock_button.set_active(value)
		self.title_entry.set_editable(value)
		self.delete_button.set_sensitive(value)
		self.reset_button.set_sensitive(value)
		self.text_view.set_editable(value)

	
	def unlock_button_toggled(self, widget):
		active = widget.get_active()
		self.enable_edit(active)


	def delete_button_clicked(self, widget):
		if self.current_work == None:
			return 

		work = self.current_work
		self.parser.remove(work._id)
		try:
			self.current_work = self.worklist[0]
			self.show_work(self.current_work)
		except IndexError:
			self.current_work = None
			self.show_nothing()
		self.his_scroll.remove(self.treeview)
		self.treeview = self.create_tree_view()
		self.his_scroll.add(self.treeview)
		self.his_scroll.show_all()
		self.enable_edit(False)

	def reset_button_clicked(self, widget):
		if self.current_work == None:
			return

		time_picker = TimePicker(self)

	def tool_new_clicked(self, widget):
		now = datetime.datetime.now().timetuple()
		start = '-'.join([str(x) for x in now[0:5]])
		work = Work(title='Untitled', start_time=start, alarm_time='9999-12-31-23-59', work_content=' ')

		if self.unlock_button.get_active() == True:

			question = QuestionDialog(self.win, Gtk.ButtonsType.YES_NO, QuestionDialog.UNSAVED_Q)

			result = question.display()
			if result == True:
				self.tool_save_clicked(self.tool_save)

		w_id = self.parser.add(work)
		work.set_id(w_id)
		self.current_work = work
		self.show_work(self.current_work)
		self.enable_edit(True)
	@log_func(log)	
	def tool_save_clicked(self, widget):
		if self.unlock_button.get_active() == False:
			return 

		self.current_work.set_title(self.title_entry.get_text())
		alarm_time = datetime.datetime.strptime(self.alarm_entry.get_text(), 
													'%x, %H:%M')
		alarm_time = [str(x) for x in alarm_time.timetuple()[0:5]]
		alarm_time = '-'.join(alarm_time)
		self.current_work.set_alarm_time(alarm_time)
		start, end = self.text_view.get_buffer().get_bounds()
		self.current_work.set_work_content(self.text_view.get_buffer().
											get_text(start, end, False))
		print str(self.current_work)
		self.parser.update(self.current_work._id, self.current_work)
		self.enable_edit(False)

		context_id = self.status_bar.get_context_id('button_clicked')
		status_message = self.current_work._title + ' has saved! ;-)'
		message_id = self.status_bar.push(context_id, status_message)
		self.status_bar.pop(message_id)
		self.status_bar.remove_all(context_id)

	def tool_preference_clicked(self, widget):
		PreferenceDialog()

	def tool_about_clicked(self, widget):
		builder = Gtk.Builder()
		builder.add_from_file(os.path.join(DATA_PATH, 'ui/about.glade'))
		about_win = builder.get_object('aboutdialog')
		about_win.set_transient_for(self.win)
		about_win.run()
		about_win.destroy()

	@log_func(log)
	def sortByStartDay(self):
		result = dict()
		for work in self.worklist:
			start_time = work._start_time
			start_day = '-'.join(start_time.split('-')[0:3])
			if start_day in result:
				result[start_day].append(work)
			else:
				result.setdefault(start_day, [work])

		return result

	@log_func(log)
	def create_tree_view(self):
		tree = Gtk.TreeView()


		history = Gtk.TreeViewColumn()
		history.set_title('Work in progress')
		#history.set_sort_order(Gtk.SortType.ASCENDING)
		history.set_sort_column_id(0)

		cell = Gtk.CellRendererText()
		history.pack_start(cell, True)
		history.add_attribute(cell, 'text', 0)

		treestore = Gtk.TreeStore(str)

		sortedWorks = self.sortByStartDay()
		for start_day in sortedWorks:
			prettyTime = TimeFormatter(start_day).format_time()

			it = treestore.append(None, [prettyTime])
			for work in sortedWorks[start_day]:
				title = work._title
				treestore.append(it, [title])

		tree.append_column(history)
		tree.set_model(treestore)
		tree.connect('row-activated', self.treeview_row_activated)
		tree.connect('cursor-changed', self.treeview_cursor_changed)
		return tree
	
	def show_work(self, work):
		self.title_entry.set_text(work._title)

		alarm_time = TimeFormatter(work._alarm_time).format_time() \
											if work._alarm_time != ' ' else ' '

		self.alarm_entry.set_text(alarm_time)
		self.text_view.get_buffer().set_text(work._work_content)
	def show_nothing(self):
		self.title_entry.set_text('')
		self.alarm_entry.set_text('')
		self.text_view.get_buffer().set_text('')
		

	def treeview_row_activated(self, widget, path, col):
		if path.get_depth() > 1:
			return
		
		expanded = widget.row_expanded(path)
		if expanded:
			widget.collapse_row(path)
		else:
			widget.expand_row(path, False)

	def treeview_cursor_changed(self, widget):
		#some 'return' appear here all because of the trigger of this method on 			window closing.

		if hasattr(self, 'unlock_button') and \
			self.win.get_focus() and \
			self.current_work != None and \
			self.unlock_button.get_active():

			question = QuestionDialog(self.win, Gtk.ButtonsType.YES_NO, QuestionDialog.UNSAVED_Q)

			result = question.display()
			if result == True:
				self.tool_save_clicked(self.tool_save)

		path, col = widget.get_cursor()
		if path == None:
			return 
		if path.get_depth() == 1:
			return 

		model = widget.get_model()

		for work in self.worklist:
			if work._title == model[path][0]:
				self.show_work(work)
				self.current_work = work
	


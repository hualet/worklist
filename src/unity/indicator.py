import os

from gi.repository import Gtk, AppIndicator3

from mainwindow import MainWindow
from daemon import WorkListDaemon
from dataparse import WorkListParser
from color_pop import ColorPop
from util.constants import DATA_PATH
from widgets.preference import PreferenceDialog


class WorkListIndicator():
	def __init__(self):

		self.status = {
			'active' : AppIndicator3.IndicatorStatus.ACTIVE,
			'attention' : AppIndicator3.IndicatorStatus.ATTENTION
		}

		self.work_dataparser = WorkListParser(os.path.join(DATA_PATH, 'work_list.xml'))
		self.worklist = self.work_dataparser._works

		self.overdue_work_dataparser = WorkListParser(os.path.join(DATA_PATH, 'overdue_work_list.xml'))

		self.overdue_worklist = self.overdue_work_dataparser._works

		self.app_indicator = AppIndicator3.Indicator.new('WorkList', 
					os.path.join(DATA_PATH, 'icons', 'WorkList-mono-dark-panel.png'),
					self.status['active'])

		self.app_indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		self.app_indicator.set_attention_icon(
				os.path.join(DATA_PATH, 'icons', 'WorkList-attention-panel.png')
		)
		
		self.app_indicator.set_title('WorkList')
		
		self.indicator_menu = Gtk.Menu()
	
		add = Gtk.MenuItem('New/Edit Work')
		add.connect('activate', self.menu_add_clicked)
		works = Gtk.MenuItem('Overdue Works')

		if len(self.overdue_worklist) != 0:
			overdue_menu = Gtk.Menu()
			works.set_submenu(overdue_menu)

			for work in self.overdue_worklist:
				overdue_work_item = Gtk.MenuItem(work._title)
				overdue_work_item.connect('activate', self.show_bubble, 
											work, overdue_menu)
				overdue_menu.append(overdue_work_item)
			self.app_indicator.set_status(self.status['attention'])

		preference = Gtk.MenuItem('Preference')
		preference.connect('activate', self.menu_preference_clicked)
		about = Gtk.MenuItem('About')
		about.connect('activate', self.menu_about_clicked)
		quit = Gtk.ImageMenuItem('Quit')
		quit.connect('activate', self.menu_quit_clicked)

		self.indicator_menu.append(add)
		self.indicator_menu.append(works)
		self.indicator_menu.append(Gtk.SeparatorMenuItem())
		self.indicator_menu.append(preference)
		self.indicator_menu.append(Gtk.SeparatorMenuItem())
		self.indicator_menu.append(about)
		self.indicator_menu.append(quit)

		self.indicator_menu.show_all()

		self.app_indicator.set_menu(self.indicator_menu)

	
	def show_bubble(self, widget, work, overdue_menu):
		print 'show_bubble'
		self.overdue_work_dataparser.remove(work._id)
		overdue_menu.remove(widget)
		if len(overdue_menu.get_children()) == 0:
			self.app_indicator.set_status(self.status['active'])
		ColorPop(work)


	def menu_add_clicked(self, widget):
		MainWindow(self)
	
	def menu_preference_clicked(self, widget):
		PreferenceDialog()

	def menu_about_clicked(self, widget):
		builder = Gtk.Builder()
		builder.add_from_file(os.path.join(DATA_PATH, 'ui/about.glade'))
		about_win = builder.get_object('aboutdialog')
		about_win.set_position(Gtk.WindowPosition.CENTER)
		try:
			about_win.set_icon_from_file(os.path.join(DATA_PATH, 'icons', 'WorkList.png'))
		except Exception:
			print 'No that picture at all.'


		about_win.run()
		about_win.destroy()

	def menu_quit_clicked(self, widget):
		Gtk.main_quit()

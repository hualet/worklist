from threading import Thread, Event
from subprocess import call
import datetime
import os

from gi.repository import Gtk, Notify

from util.constants import DATA_PATH
from util.worklist_settings import WorkListSettings


class Timer(Thread):
	"""Call a function after a specified number of seconds:
	
	t = Timer(30.0, f, args=[], kwargs={})
	t.start()
	t.cancel() # stop the timer's action if it's still waiting
	"""
	
	def __init__(self, interval, function, args=[], kwargs={}):
		Thread.__init__(self)
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.finished = Event()
	
	def cancel(self):
		"""Stop the timer if it hasn't finished yet"""
		self.finished.set()
	
	def run(self):
		while True:
			self.finished.wait(self.interval)
			if not self.finished.is_set():
				self.function(*self.args, **self.kwargs)


class WorkListDaemon(Timer):

	def __init__(self, master):
		super(WorkListDaemon, self).__init__(30, self.check_time)

		self.master = master
		self.setDaemon(True)

		Notify.init('WorkList')
		self.current_notification = None
		
	def play_sound(self):
		alarm_ring = WorkListSettings.get_value('alarm-ring')
		call(['paplay', os.path.join(DATA_PATH, 'sound', alarm_ring)])

	def check_time(self):
		print 'check_time'

		worklist = self.master.worklist
		overdue_worklist = self.master.overdue_worklist

		if len(worklist) == 0:
			return
		else:
			for work in worklist:
				alarm_time = work._alarm_time
				str_timetuple = alarm_time.split('-')
				int_timetuple = [int(x) for x in str_timetuple]
				alarm_datetime = datetime.datetime(*int_timetuple)
		
				now_datetime = datetime.datetime.now()

				delta = now_datetime - alarm_datetime

				if delta.total_seconds() >= 0:
					Thread(target=self.play_sound).start()
					self.current_notification = Notify.Notification.new(
						'Time To Work Now',
						"\n" + work._title + "\n",
						os.path.join(DATA_PATH, 'icons', 'WorkList-mono-dark.png')
					)
					self.current_notification.set_hint_string('append','allowed')
					self.current_notification.show()

					self.master.work_dataparser.remove(work._id)
					self.master.overdue_work_dataparser.add(work)
			

			menu_works = self.master.indicator_menu.get_children()[1]
			overdue_menu = menu_works.get_submenu()
			if overdue_menu == None:
				overdue_menu = Gtk.Menu()
				menu_works.set_submenu(overdue_menu)
			else:
				for i in overdue_menu.get_children():
					overdue_menu.remove(i)
			for work in overdue_worklist:
				overdue_work_item = Gtk.MenuItem(work._title)
				overdue_work_item.connect('activate', self.master.show_bubble,
											work, overdue_menu)
				overdue_menu.append(overdue_work_item)
			menu_works.show_all()
			if len(overdue_worklist) != 0:
				self.master.app_indicator.set_status(
										self.master.status['attention'])

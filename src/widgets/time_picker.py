import os
from datetime import datetime

from gi.repository import Gtk

from util.constants import DATA_PATH

class TimePicker():
	def __init__(self, parent):
		self.parent = parent

		builder = Gtk.Builder()
		builder.add_from_file(os.path.join(DATA_PATH, 'ui/set_time.glade'))
		
		self.win = builder.get_object('time_setter')
		self.win.set_transient_for(self.parent.win)
		self.win.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
		self.calendar = builder.get_object('calendar1')

		self.hour_spin = builder.get_object('spinbutton1')
		self.hour_spin.set_range(0, 23)
		self.hour_spin.set_increments(1, 10)

		self.hour_label = builder.get_object('label3')
		self.hour_label.set_text('Hour : ')

		self.minu_spin = builder.get_object('spinbutton2')
		self.minu_spin.set_range(0, 59)
		self.minu_spin.set_increments(1, 10)

		self.minu_label = builder.get_object('label4')
		self.minu_label.set_text('Minute')
		self.set_now_time_for_widgets()
		self.ok_button = builder.get_object('ok')
		self.ok_button.connect('clicked', self.reset_ok_clicked)
		self.cancel_button = builder.get_object('cancel')
		self.cancel_button.connect('clicked', self.reset_cancel_clicked)

		self.win.show_all()
	
	def reset_ok_clicked(self, widget):
		self.parent.current_work._title =self.parent.title_entry.get_text()

		start, end = self.parent.text_view.get_buffer().get_bounds()
		self.parent.current_work.set_work_content(
				self.parent.text_view.get_buffer().get_text(start, end, False)
		)
		
		alarm_time = self.get_time_from_widgets()
		self.parent.current_work._alarm_time = alarm_time
		self.parent.show_work(self.parent.current_work)
		self.win.destroy()
	
	def reset_cancel_clicked(self, widget, win):
		self.win.destroy()

	def set_time_for_widgets(self, date_time):
		self.calendar.select_month(date_time.year, date_time.month - 1)
		self.calendar.select_day(date_time.day)

		self.hour_spin.set_value(date_time.hour)
		self.minu_spin.set_value(date_time.minute)

	def set_now_time_for_widgets(self):
		now = datetime.now()
		self.set_time_for_widgets(now)

	def get_time_from_widgets(self):
		tuple_date = self.calendar.get_date()
		date = list(tuple_date)
		date[1] += 1
		time = self.hour_spin.get_text() + '-' + self.minu_spin.get_text()

		alarm_time = '-'.join([str(x) for x in date]) + '-' + time
		return alarm_time


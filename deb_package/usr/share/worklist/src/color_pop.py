import os

from gi.repository import Gtk, Gdk

import datatype
from datatype import *
from util.constants import DATA_PATH

class ColorPop(Gtk.Window):
	
	def __init__(self, work):
		super(ColorPop, self).__init__()
		self.set_default_size(200, 250)
		self.set_title(work._title)
		self.set_border_width(5)
		try:
			self.set_icon_from_file(os.path.join(DATA_PATH, 'icons', 'WorkList.png'))
		except Exception:
			print "There's no picture at all."
		#self.set_decorated(False)
		self.set_position(Gtk.WindowPosition.MOUSE)

		self.content = Gtk.ScrolledWindow()
		self.content.set_policy(Gtk.PolicyType.AUTOMATIC, 
								Gtk.PolicyType.AUTOMATIC)

		self.view = Gtk.TextView()
		self.view.modify_bg(Gtk.StateType.NORMAL, 
								Gdk.Color(62207, 61951, 61695))
		self.view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
		self.view.set_editable(False)
		self.view.set_cursor_visible(False)
		self.view.set_justification(Gtk.Justification.CENTER)
		buffer = self.view.get_buffer()
		buffer.set_text(work._work_content)
		self.content.add(self.view)
		self.connect("delete-event", Gtk.main_quit)

		self.add(self.content)
		self.show_all()

		Gtk.main()

import os

from gi.repository import Gtk, Gio


from util.worklist_settings import WorkListSettings
from util.constants import DATA_PATH

class PreferenceDialog(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)

		self.set_title('Preference')

		try:
			self.set_icon_from_file(os.path.join(DATA_PATH, 'icons', 'WorkList.png'))
		except Exception:
			print 'No that picture at all.'

		self.set_default_size(300, 400)
		self.set_border_width(10)
		self.set_position(Gtk.WindowPosition.CENTER)

		self.main_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

		self.settings = Gtk.Notebook()

		self.advanced_grid = Gtk.Grid()
		self.advanced_grid.set_margin_top(8)
		self.advanced_grid.set_margin_left(8)
		self.advanced_grid.set_margin_right(8)
		self.advanced_grid.set_margin_bottom(8)

		self.start_label = Gtk.Label()
		self.start_label.set_markup('<b>Start</b>')
		self.auto_start_label = Gtk.Label('Auto Start : ')
		self.auto_start_switch = Gtk.Switch()
		switch = WorkListSettings.get_value('auto-start')
		self.auto_start_switch.set_active(switch)
		self.auto_start_switch.connect('activate', self.auto_start_set)
		self.advanced_grid.attach(self.start_label, 0, 0, 1, 1)
		self.advanced_grid.attach(self.auto_start_label, 1, 1, 1, 1)
		self.advanced_grid.attach(self.auto_start_switch, 2, 1, 1, 1)

		self.common_grid = Gtk.Grid()
		self.common_grid.set_margin_top(8)
		self.common_grid.set_margin_left(8)
		self.common_grid.set_margin_right(8)
		self.common_grid.set_margin_bottom(8)

		self.font_label = Gtk.Label()
		self.font_label.set_markup('<b>Fonts and Colors</b>')
		self.editor_font_label = Gtk.Label('Editor Font : ')
		self.editor_font_button = Gtk.FontButton()
		self.editor_font_button.set_font_name(WorkListSettings.get_value('editor-font'))
		self.editor_font_button.set_show_style(True)
		self.editor_font_button.set_show_size(True)
		self.editor_font_button.set_use_font(True)
		self.editor_font_button.set_use_size(True)
		self.editor_font_button.connect('font-set', self.editor_font_set)
		self.common_grid.attach(self.font_label, 0, 0, 1, 1)
		self.common_grid.attach(self.editor_font_label, 0, 1, 1, 1)
		self.common_grid.attach(self.editor_font_button, 1, 1, 1, 1)

		self.popup_font_label = Gtk.Label('Popup Font : ')
		self.popup_font_button = Gtk.FontButton()
		self.popup_font_button.set_font_name(WorkListSettings.get_value('popup-font'))
		self.popup_font_button.set_show_style(True)
		self.popup_font_button.set_show_size(True)
		self.popup_font_button.set_use_font(True)
		self.popup_font_button.set_use_size(True)
		self.popup_font_button.connect('font-set', self.popup_font_set)
		self.common_grid.attach(self.popup_font_label, 0, 2, 1, 1)
		self.common_grid.attach(self.popup_font_button, 1, 2, 1, 1)


		self.settings.append_page(self.common_grid, Gtk.Label('Common'))
		self.settings.append_page(self.advanced_grid, Gtk.Label('Advanced'))

		self.button_grid = Gtk.Grid()
		self.button_grid.set_margin_top(5)
		self.button_grid.set_column_homogeneous(True)
		self.apply_button = Gtk.Button.new_from_stock(Gtk.STOCK_APPLY)
		self.apply_button.connect('clicked', self.apply_clicked)
		self.close_button = Gtk.Button.new_from_stock(Gtk.STOCK_CLOSE)
		self.close_button.connect('clicked', self.close_clicked)
		self.button_grid.attach(Gtk.Label(), 0, 0, 3, 1)
		self.button_grid.attach(self.apply_button, 5, 0, 2, 1)
		self.button_grid.attach(self.close_button, 7, 0, 2, 1)

		self.main_box.pack_start(self.settings, True, True, 0)
		self.main_box.pack_start(self.button_grid, False, True, 0)
		self.add(self.main_box)
		self.connect('delete-event', self.close_clicked)
		self.show_all()

	def editor_font_set(self, widget):
		self.editor_font_value = widget.get_font_name()
	
	def popup_font_set(self, widget):
		self.popup_font_value = widget.get_font_name()
		
	def auto_start_set(self, widget):
		self.auto_start_value = widget.get_active()
		
	def apply_clicked(self, widget):
		if hasattr(self, 'auto_start_value'):
			WorkListSettings.set_value('auto-start', self.auto_start_value)
		if hasattr(self, 'editor_font_value'):
			WorkListSettings.set_value('editor-font', self.editor_font_value)
		if hasattr(self, 'popup_font_value'):
			WorkListSettings.set_value('popup-font', self.popup_font_value)
		
	def close_clicked(self, widget, data=None):
		self.destroy()

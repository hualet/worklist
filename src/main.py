import os

from gi.repository import Gtk, Gdk, GObject

from unity.indicator import WorkListIndicator
from unity.daemon import WorkListDaemon
from util import WorkListSettings
	
auto_file_path = os.path.join(os.path.expanduser('~'), 
			'.config', 'autostart', 'WorkList.desktop')

if not os.path.exists(auto_file_path) and WorkListSettings.get_value('auto-start'):
	os.symlink('/usr/share/applications/WorkList.desktop', auto_file_path)

GObject.threads_init()
Gdk.threads_init()
indicator = WorkListIndicator()
WorkListDaemon(indicator).start()
Gtk.main()

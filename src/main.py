from gi.repository import Gtk, Gdk, GObject

from unity.indicator import WorkListIndicator
from unity.daemon import WorkListDaemon


GObject.threads_init()
Gdk.threads_init()
indicator = WorkListIndicator()
WorkListDaemon(indicator).start()
Gtk.main()

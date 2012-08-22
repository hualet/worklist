from gi.repository import Gtk, Gdk, GObject

from unity.indicator import WorkListIndicator
from unity.daemon import WorkListDaemon


GObject.threads_init()
Gdk.threads_init()
WorkListDaemon(indicator).start()
Gtk.main()

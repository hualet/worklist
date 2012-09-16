#!/usr/bin/env python

import os
import sys
import logging as log
import tempfile
import shutil
import subprocess

from gi.repository import Gtk, Gdk, GObject

from unity.indicator import WorkListIndicator
from unity.daemon import WorkListDaemon
from util.worklist_settings import WorkListSettings

log.basicConfig(level=log.DEBUG)

class SingleInstance(object):
	""" Class to ensure, that single instance of the applet is run for each user """
	# Initialize, specifying a path to store pids
	def __init__(self, pidPath):
		self.pidPath=pidPath
		# See if pidFile exists
		if os.path.exists(pidPath):
			# Make sure it is not a "stale" pidFile
			pid=open(pidPath, 'r').read().strip()
			# Check list of running pids, if not running it is stale so overwrite
			pidRunning = not subprocess.call('ls -1 /proc | grep ^%s$' % pid, shell=True)
			self.lasterror = False if pidRunning else True
		else:
			self.lasterror = True

		if self.lasterror:
			# Create a temp file, copy it to pidPath and remove temporary file
			(fp, temp_path)=tempfile.mkstemp()
			try:
			    os.fdopen(fp, "w+b").write(str(os.getpid()))
			    shutil.copy(temp_path, pidPath)
			    os.unlink(temp_path)
			except Exception as e:
				print e
	
	def is_alreay_running(self):
		return not self.lasterror
	
	def __del__(self):
		if self.lasterror:
			os.unlink(self.pidPath)

myApp = SingleInstance('/tmp/worklist-%d.pid' % os.getuid())
if myApp.is_alreay_running():
	sys.exit('Another instance of this program is already running!')

GObject.threads_init()
Gdk.threads_init()
indicator = WorkListIndicator()
WorkListDaemon(indicator).start()
Gtk.main()

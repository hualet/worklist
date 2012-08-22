import datetime


class Work():
	def __init__(self, title = None, start_time = None, 
					alarm_time = None, work_content = None, id = None):
		
		self._id = id
		self._title = title
		self._start_time = start_time
		self._alarm_time = alarm_time
		self._work_content = work_content

	def set_id(self, id):
		self._id = id

	def set_title(self, title):
		self._title = title

	def set_start_time(self, start_time):
		self._start_time = start_time
	def get_formatted_start_time(self):
		return TimeFormatter(self._start_time).format_time()

	def set_alarm_time(self, alarm_time):
		self._alarm_time = alarm_time
	def get_formatted_alarm_time(self):
		return TimeFormatter(self._alarm_time).format_time()



	def set_work_content(self, work_content):
		self._work_content = work_content

	def __str__(self):
		return 'Work %s %s %s %s %s' % \
					(str(self._id), self._title, self._start_time, self._alarm_time, self._work_content)

		
class TimeFormatter():
	
	def __init__(self, time_str):
		self._time_str = time_str
	
	def format_time(self):
		if self._time_str != None and self._time_str != '':
			timetuple = self._time_str.split('-')
			timetuple = [int(x) for x in timetuple]
			date = datetime.datetime(*timetuple)

			if len(timetuple) == 3:
				return date.strftime('%x')

			return date.strftime('%x, %H:%M')
		else:
			return ''

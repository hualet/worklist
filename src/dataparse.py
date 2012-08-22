from xml.dom import minidom
import os
import logging

from datatype import Work
from util.debug import log_func
from util.constants import DATA_PATH

XML_HEADER = '''<?xml version="1.0" ?>
<worklist ever='1'>
</worklist>
'''

class WorkListParser():

	log = logging.Logger('WorkListParser')

	def __init__(self, path):
		
		self._works = list()
		self._path = path

		if not os.path.exists(self._path):
			self.new_file(self._path)

		file_content = minidom.parse(self._path)
		work_list = file_content.getElementsByTagName('work')

		for work in work_list:
				wo_rk = Work()
				wo_rk.set_id(work.getAttribute('id'))
				wo_rk.set_title(work.getElementsByTagName('title')[0].firstChild.nodeValue)
				wo_rk.set_start_time(work.getElementsByTagName('start_time')[0].firstChild.nodeValue)
				wo_rk.set_alarm_time(work.getElementsByTagName('alarm_time')[0].firstChild.nodeValue)
				wo_rk.set_work_content(work.getElementsByTagName('work_content')[0].firstChild.nodeValue)
				self._works.append(wo_rk)

	def remove(self, id):
		target = None
		for work in self._works:
			if id == str(work._id):
				target = work
		
		if target == None:
			return

		if os.path.exists(self._path):
			file_content = minidom.parse(self._path)
			root = file_content.documentElement
			works = file_content.getElementsByTagName('work')
			for work in works:
				if work.getAttribute('id') == id:
					root.removeChild(work)


			self.save(file_content, root, self._path)

		self._works.remove(target)

	def get(self, id):
		for work in self._works:
			if work._id == id:
				return work
		return None

	def update(self, id, work):
		print 'update'
		work._id = id
		for w in self._works:
			if str(w._id) == id:
				self.remove(id)
				self.add(work)
				return 
				
	def add(self, work):
		
		id = work._id
		title = work._title
		start_time = work._start_time
		alarm_time = work._alarm_time
		content = work._work_content

		if os.path.exists(self._path):
			file_content = minidom.parse(self._path)
			root = file_content.documentElement
			new_work = file_content.createElement('work')
			if id == None:
				ele_worklist = file_content.getElementsByTagName('worklist')[0]
				ever_id = ele_worklist.getAttribute('ever')
				new_work.setAttribute('id', ever_id)

				ele_worklist.setAttribute('ever', str(int(ever_id) + 1))
				work.set_id(ever_id)
			else:
				new_work.setAttribute('id', id)
				work.set_id(id)
			
			title = file_content.createTextNode(title)
			ele_title = file_content.createElement('title')
			ele_title.appendChild(title)

			start_time = file_content.createTextNode(start_time)
			ele_start = file_content.createElement('start_time')
			ele_start.appendChild(start_time)

			alarm_time = file_content.createTextNode(alarm_time)
			ele_alarm = file_content.createElement('alarm_time')
			ele_alarm.appendChild(alarm_time)

			content = file_content.createTextNode(content)
			content.normalize()
			ele_content = file_content.createElement('work_content')
			ele_content.normalize()
			ele_content.appendChild(content)
			
			new_work.appendChild(ele_title)
			new_work.appendChild(ele_start)
			new_work.appendChild(ele_alarm)
			new_work.appendChild(ele_content)

			root.appendChild(new_work)

			self.save(file_content, root, self._path)

			self._works.append(work)

			return work._id


	def new_file(self, path):
		new_file = open(path, 'w')
		new_file.write(XML_HEADER)
		new_file.close()
		

	def save(self, document, root, path):
		writer = open(path, 'w+')
		document.writexml(writer, '', '	', '\n')
		writer.flush()

		writer.seek(0)
		xml = str()
		for line in writer:
			if not line.split():
				pass
			else:
				xml += line

		writer.seek(0)
		writer.truncate()
		writer.write(xml)
		writer.close()



if __name__ == '__main__':

	parser = WorkListParser()
	works = parser._works
	for work in works:
		print str(work)

	print '*' * 20

	work = Work('title', '2012-8-7-20-10', '2012-8-7-20-10', 'Shut')
	parser.add(work)
	for work in works:
		print str(work)

	print '*' * 20

	work = parser.get('3')
	print str(work)

	print '*' * 20

	work = Work('title2', '2012-8-7-2-10', '2012-8-7-20-1', 'Shutup')
	parser.update('4', work)
	for work in works:
		print str(work)



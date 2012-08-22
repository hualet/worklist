import types

from gi.repository import Gio

class WorkListSettings():
	COMMON_PATH = 'apps.worklist.common'
	ADVANCED_PATH = 'apps.worklist.advanced'

	common = Gio.Settings.new_with_path(COMMON_PATH,'/' + '/'.join(COMMON_PATH.split('.')) + '/')
	advanced = Gio.Settings.new_with_path(ADVANCED_PATH,'/' + '/'.join(ADVANCED_PATH.split('.')) + '/')

	COMMON_KEYS = [ 'editor-font', 'popup-font' ]
	ADVANCED_KEYS = [ 'auto-start' ]
	
	KEY_TYPE = {
		'editor-font' : types.StringType,
		'popup-font' : types.StringType,
		'auto-start' : types.BooleanType,
	}

	@classmethod
	def get_value(cls, key):
		settings = None
		if key in cls.common.list_keys():
			settings = cls.common
		elif key in cls.advanced.list_keys():
			settings = cls.advanced
		else:
			return settings

		get_func = {
			types.StringType : settings.get_string,
			types.BooleanType : settings.get_boolean
		}
			
		return get_func[cls.KEY_TYPE[key]](key)

	@classmethod
	def set_value(cls, key, value):
		settings = None
		if key in cls.common.list_keys():
			settings = cls.common
		elif key in cls.advanced.list_keys():
			settings = cls.advanced
		else:
			return

		set_func = {
			types.StringType : settings.set_string,
			types.BooleanType : settings.set_boolean
		}
			
		return set_func[cls.KEY_TYPE[key]](key, value)

	def obj_bind(cls, key, obj, prop, flag = Gio.SettingsBindFlags.DEFAULT):
		if key not in cls.COMMON_KEYS or key not in cls.ADVANCED_KEYS:
			raise Exception('key not found')
		elif key in COMMON_KEYS:
			cls.common.bind(key, obj, prop, flag)
		else:
			cls.advanced.bind(key, obj, prop, flag)

if __name__ == '__main__':
	print WorkListSettings.get_value('editor-font')

from gi.repository import Gtk


class QuestionDialog(Gtk.MessageDialog):

	UNSAVED_Q = '''You have some changes unsaved,
Would you like to save them? '''

	def __init__(self, parent, buttonsType, body, flag=Gtk.DialogFlags.MODAL,
					messageType=Gtk.MessageType.QUESTION, 
					title='WorkList Remind You:'):

		super(QuestionDialog, self).__init__(parent, flag, messageType,
												buttonsType, title)

		self.format_secondary_text(body)
	
	def display(self):
		result = self.run()
		if result == Gtk.ResponseType.YES:
			result = True
		else:
			result = False

		self.destroy()

		return result

# firestore database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json
from PyQt5 import QtCore

class NoteDatabase(QtCore.QObject):
	user_changed = QtCore.pyqtSignal(str)
	_instance = None
	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super(NoteDatabase, cls).__new__(cls, *args, **kwargs)
		return cls._instance
	
	def __init__(self, *args, **kwargs):
		super(NoteDatabase, self).__init__(*args, **kwargs)
		path = os.path.dirname(os.path.abspath(__file__))
		path = os.path.join(path, 'secret/notesproject-a56c6-firebase-adminsdk-tx5ef-aa5ccd560b.json')
		cred = credentials.Certificate(path)
		if not firebase_admin._apps:
			firebase_admin.initialize_app(cred)
		self.db = firestore.client()
		self.current_user = None

		self.login('test', 123)

	def create_user(self, user_id:str, password:str) -> bool:
		# check if user exists
		user = self.db.collection(u'users').document(user_id)
		if user.get().exists:
			return False
		user.set({
			u'password': password
		})
		self.current_user = user_id
		return True

	def login(self, user_id:str, password:str) -> bool:
		user = self.db.collection(u'users').document(user_id).get()
		if not user.exists:
			return False

		res = (user.to_dict()['password'] == password)
		if res:
			self.current_user = user_id
		return res
	
	def logout(self) -> None:
		self.current_user = None

	def get_user(self) -> str:
		return self.current_user

	def save_notes(self, note:str) -> None:
		note_ref = self.db.collection(u'users').document(self.current_user).collection(u'notes').document(note['title'])
		note_ref.set(note, merge=True)
		return self.is_note_exists(note['title'])
		
	def get_notes(self) -> list:
		if self.current_user is None:
			return None
		notes = self.db.collection(u'users').document(self.current_user).collection(u'notes').get()
		notes = [note.to_dict() for note in notes]
		return notes
	
	def is_note_exists(self, note:str) -> bool:
		note_ref = self.db.collection(u'users').document(self.current_user).collection(u'notes').document(note)
		return note_ref.get().exists
	
	def get_pages(self, note:str) -> list:
		try:
			pages = self.db.collection(u'users').document(self.current_user).collection(u'notes').document(note).collection(u'pages').get()	
			pages = [page.to_dict() for page in pages]
			return pages
		except:
			return None

	def save_page(self, page:str) -> None:
		page_ref = self.db.collection(u'users').document(self.current_user).collection(u'notes').document(page['note']).collection(u'pages').document(page['page'])
		page_ref.set(page)
	
	def get_note_by_title(self, title:str) -> dict:
		note = self.db.collection(u'users').document(self.current_user).collection(u'notes').document(title).get()
		note = note.to_dict()
		return note
	
	def save_widget(self, widget:str) -> None:
		widget = json.loads(widget)
		widget_ref = self.db.collection(u'users').document(self.current_user).collection(u'notes').document(widget['note']).\
			collection(u'pages').document(widget['page']).collection(u'widgets').document(widget['cell'])
		widget_ref.set(widget['widget'], merge=True)

	def delete_widget(self, cell:tuple, note:str, page:str) -> None:
		widget_ref = self.db.collection(u'users').document(self.current_user).collection(u'notes').document(note).\
			collection(u'pages').document(page).collection(u'widgets').document(f'{cell}')
		widget_ref.delete()

	def get_widgets(self, note:str, page:str) -> list:
		try:
			widgets = self.db.collection(u'users').document(self.current_user).collection(u'notes').document(note).collection(u'pages').document(page).collection(u'widgets').get()
			widgets = [widget.to_dict() for widget in widgets]
			return widgets
		except:
			return None

if __name__ == '__main__':
	db = NoteDatabase()
	db.create_user('test', 123)
	print(db.login('test', 123))

	db.save_notes({
		'title': 'test',
	})
	print(db.get_notes())
	db.save_page({
		'note': 'test',
		'page': 'Page-1',
		'page_number': 1,
		'row': 1,
		'col': 1,
	})
	db.save_page({
		'note': 'test',
		'page': 'Page-2',
		'page_number': 1,
		'row': 1,
		'col': 1,
	})
	print(db.get_pages('test'))
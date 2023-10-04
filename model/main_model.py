from PyQt5 import QtCore, QtWidgets, QtGui

from menu_bar_model import MenuControl
from widget_container_model import WidgetContainerModel
from database import NoteDatabase

class MainModel(QtCore.QObject):
	log_res = QtCore.pyqtSignal(bool, bool)
	def __init__(self, *args, **kwargs):
		view = kwargs.pop('view', None)
		super(MainModel, self).__init__(*args, **kwargs)
		self._view = view
		self.db = NoteDatabase()

		self.menu_bar_model = MenuControl(view=self._view)
		self.widget_container_model = WidgetContainerModel(view=self._view)

		# Mengolah data untuk login user
		login = self._view._central_widget.login_page
		login.login_signal.connect(self.login)
		login.signup_signal.connect(self.signup)

		# menghubungkan signal hasil login ke halaman login
		self.log_res.connect(login.login_res)
		# untuk mengeluarkan halaman login
		self._view._central_widget._widget_menubar.acc_button.clicked.connect(self._view._central_widget.login_page.show)
		# mengubah note ketika user mengganti halaman
		self._view._central_widget._widget_menubar.page_changed.connect(self.page_changed)
		# untuk menyimpan note
		self._view._central_widget._widget_menubar.save_button.clicked.connect(self.save_page)

	def save_page(self):
		if not self.db.get_user():
			print("no user")
			return
		self.menu_bar_model.save_note()
		self.menu_bar_model.save_pages()
		self.widget_container_model.save_widget()

	def page_changed(self, note, page):
		self.note = note
		self.page = page
		note = self.get_note_widget(note)
		page = self.get_page_widget(note, page)
		self.menu_bar_model.set_note_page(self.note, self.page)
		self.widget_container_model.set_note_page(self.note, self.page)
		self.widget_container_model.clear_widgets(note, page)
		self.widget_container_model.load_widget(note, page)

	def set_view(self, view):
		self._view = view
		
	def get_note_widget(self, note:str) -> QtWidgets.QWidget:
		notes = self._view._central_widget._widget_menubar.note
		for n in notes:
			if n.objectName() == note:
				return n

	def get_page_widget(self, note:QtWidgets.QWidget, page:str) -> QtWidgets.QWidget:
		for p in note.get_pages():
			if p.objectName() == page:
				return p
			
	def change_user(self, type:bool):
		self.menu_bar_model.load_notes()

		self.note = self._view._central_widget._widget_menubar.note[0]
		try:
			self.page = self.note.get_pages()[0].objectName()
		except:
			self.page = -1
		self.note = self.note.objectName()
		self.widget_container_model.set_note_page(self.note, self.page)
		note = self.get_note_widget(self.note)
		page = self.get_page_widget(note, self.page)
		self.widget_container_model.load_widget(note, page)

	def new_user(self):
		self.menu_bar_model.new_note()
		self.widget_container_model.new_page()
			
	def login(self, username, password):
		res = self.db.login(username, password)
		self.log_res.emit(res, 0)
		if res:
			self.change_user(True)

	def signup(self, username, password):
		res = self.db.create_user(username, password)
		self.log_res.emit(res, 1)
		if res:
			self.new_user()
			self.change_user(False)


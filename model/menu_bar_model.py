from PyQt5 import QtCore, QtWidgets, QtGui
import json
import os
from database import NoteDatabase

class MenuControl(QtCore.QObject):
	def __init__(self, *args, **kwargs) -> None:
		view = kwargs.pop('view', None)
		self.page = kwargs.pop('page', None)
		self.note = kwargs.pop('note', None)
		super(MenuControl, self).__init__(*args, **kwargs)
		self._view = view
		self.db = NoteDatabase()
		self.notes = self._view._central_widget._widget_menubar.note
		self.pages = []
		for note in self.notes:
			self.pages.append(note.get_pages())

	def set_note_page(self, note:str, page:str) -> None:
		self.note = note
		self.page = page

	def make_json(self, note: QtWidgets.QWidget)-> str:
		title = note.objectName()
		note_data = {
			'title': title,
			'pages': []
		}
		for i, page in enumerate(note.get_pages()):
			note_data['pages'].append({
				'page_title': page.objectName(),
				'page_number': i + 1,
			})

		note_data = json.dumps(note_data, indent=4)

		return note_data
	
	def save_note(self) -> bool:
		self.notes = self._view._central_widget._widget_menubar.note
		print(self.notes)
		for note in self.notes:
			data = {
				'title': note.objectName(),
			}

		r = self.db.save_notes(data)
		print("Success" if r else "Failed")

	def clear_notes(self) -> None:
		notes = self._view._central_widget._widget_menubar.note
		for note in notes:
			note.deleteLater()
		self._view._central_widget._widget_menubar.note = []

	def load_notes(self) -> None:
		notes_data = self.db.get_notes()
		self.clear_notes()
		if not notes_data:
			self.new_note()
			return
		for note_data in notes_data:
			note = self._view._central_widget._widget_menubar.add_note(note_data['title'])
			self.load_pages(note, note_data['title'])

	def load_pages(self, note:QtWidgets.QWidget, title:str) -> None:
		print(note.objectName())
		pages_data = self.db.get_pages(title)
		print(pages_data)
		for page_data in pages_data:
			page = self._view._central_widget._widget_menubar.add_new_page(note)
			page.set_title(page_data['page'])
			page.set_rowcol((page_data['row'], page_data['col']))
			page.set_page_num(page_data['page_number'])

	def save_pages(self) -> bool:
		old = self.note
		notes = self._view._central_widget._widget_menubar.note
		for note in notes:
			self.note = note.objectName()
			pages = self.get_pages()
			for page in pages:
				data = {
					'note': note.objectName(),
					'page': page.objectName(),
					'page_number': page.get_page_num(),
					'row': page.get_row(),
					'col': page.get_col(),
				}
				self.db.save_page(data)
		self.note = old

	def save_page(self) -> bool:
		page = self.get_page(self.page)
		data = {
			'note' : self.note,
			'page' : self.page,
			'page_number': page.get_page_num(),
			'row': page.get_row(),
			'col': page.get_col(),
		}
		self.db.save_page(data)

	def new_note(self, title:str=None) -> QtWidgets.QWidget:
		note = self._view._central_widget._widget_menubar.add_new_note(title)
		self.save_note()
		self.save_pages()
		return note

	def get_pages(self) -> list:
		notes = self._view._central_widget._widget_menubar.note
		
		for note in notes:
			if note.objectName() == self.note:
				return note.get_pages()
		return None

	def get_page(self, title:str):
		notes = self._view._central_widget._widget_menubar.note
		for note in notes:
			if note.objectName() == self.note:
				pages = note.get_pages()
				for page in pages:
					if page.objectName() == self.page:
						return page
					
		return None

		

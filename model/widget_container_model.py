from PyQt5 import QtCore, QtWidgets, QtGui
from database import NoteDatabase
from ui.custom_widget_enum import WidgetEnum
import json
import numpy as np

class WidgetContainerModel(QtCore.QObject):
	def __init__(self, *args, **kwargs):
		view = kwargs.pop('view', None)
		super(WidgetContainerModel, self).__init__(*args, **kwargs)
		self._view = view
		self.db = NoteDatabase()
		self.note = None
		self.page = None
		self._view._central_widget._widget_menubar.page_changed.connect(self.set_note_page)
		self._widget_container = self._view._central_widget._widget_container

		self._widget_container.widget_deleted.connect(self.delete_widget)
		self._widget_container.widget_added.connect(self.add_widget)

	def set_note_page(self, note:str, page:str):
		self.note = note
		self.page = page

	def set_note(self, note:str):
		self.note = note

	def set_page(self, page:str):
		self.page = page

	def make_json(self, widget:QtWidgets.QWidget) -> str:
		widget_data = {
			'note': self.note,
			'page': self.page,
			'cell': f'{widget.get_cell()}',
			'widget': {
				'widget_name': widget.objectName(),
				'widget_type': widget.get_type(),
				'widget_cell': widget.get_cell(),
				'widget_span': widget.get_span(),
				'widget_data': widget.get_data()
			}
		}
		widget_data = json.dumps(widget_data, indent=4)
		return widget_data

	def save_widget(self) -> None:
		widgets = self.get_widgets()
		widgets = np.array(widgets).flatten()

		for i, widget in enumerate(widgets):
			if not widget:
				continue
			widget_data = self.make_json(widget)
			self.db.save_widget(widget_data)
	
	def add_widget(self, row:int, coll:int) -> None:
		widget = self._widget_container.get_widget((row, coll))
		widget_data = self.make_json(widget)
		self.db.save_widget(widget_data)
	
	def delete_widget(self, row:int, coll:int) -> None:
		cell = (row, coll)
		self.db.delete_widget(cell, self.note, self.page)
	
	def clear_widgets(self, note:QtWidgets.QWidget, page:QtWidgets.QWidget) -> None:
		widgets = self._widget_container._widget.flatten()
		for widget in widgets:
			if widget:
				cell = widget.get_cell()
				self._widget_container.setSpan(cell[0], cell[1], 1, 1)
				self._widget_container.setCellWidget(cell[0], cell[1], None)
		self._widget_container._widget = np.empty(1, dtype=object)

	def load_widget(self, note:QtWidgets.QWidget, page:QtWidgets.QWidget) -> None:
		if note:
			self.note = note.objectName()
		if page:
			self.page = page.objectName()
		widgets = self.db.get_widgets(self.note, self.page)
		self._widget_container._widget = np.empty((page.get_row(), page.get_col()), dtype=object)
		if not widgets:
			return False
		for widget in widgets:
			widget_type = widget['widget_type']
			widget_cell = widget['widget_cell']
			widget_name = widget['widget_name']
			widget_span = widget['widget_span']
			widget_data = widget['widget_data']

			widget = WidgetEnum.get_widget(widget_type)
			self._widget_container.add_widget(widget, widget_cell, widget_span, widget_name, widget_data)
		
		return True

	def get_widgets(self) -> list:
		widgets = self._view._central_widget._widget_container._widget
		return widgets
	
	def new_page(self, row = 3, col = 2) -> None:
		self._widget_container.new_page(row, col)
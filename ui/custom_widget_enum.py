from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, QEvent, pyqtSignal, Qt, QDate
from PyQt5.QtGui import QPalette, QColor, QBrush, QFont, QTextOption
import json
	
class MCellWidget(QObject):
	def __init__(self, *args, **kwargs):
		self._cell = kwargs.pop("cell", None)
		self._rowspan = kwargs.pop("rowspan", 1)
		self._colspan = kwargs.pop("colspan", 1)
		self._type = kwargs.pop("type", -1)
		super(MCellWidget, self).__init__(*args, **kwargs)

	def set_cell(self, cell:tuple):
		self._cell = cell

	def get_cell(self) -> tuple:
		return self._cell
	
	def set_span(self, rowspan:int, colspan:int) -> None:
		self._rowspan = rowspan
		self._colspan = colspan

	def get_span(self) -> tuple:
		return self._rowspan, self._colspan
	
	def get_type(self):
		return self._type


class MPlainTextEdit(QPlainTextEdit, MCellWidget):
	text_overflow = pyqtSignal(tuple)
	def __init__(self, *args, **kwargs):
		super(MPlainTextEdit, self).__init__(*args, **kwargs)
		self.setObjectName("MPlainTextEdit")

		self.setStyleSheet("""
					 		MPlainTextEdit { border : none; border-radius: 5px; border-right: 3px solid rgba(35, 37, 40, 0); border-bottom: 3px solid rgba(35, 37, 40, 0);
					 		background-color: palette(base); }
					 		:hover { border : none; border-radius: 5px; border-right: 3px solid rgba(35, 37, 40, 100); border-bottom: 3px solid rgba(35, 37, 40, 100);}
					 		:focus { border : none; border-radius: 5px; border-right: 3px solid rgba(35, 37, 40, 200); border-bottom: 3px solid rgba(35, 37, 40, 200);}
					 	""")

		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.setWordWrapMode(True)
		self.setLineWrapMode(True)

		self.verticalScrollBar().valueChanged.connect(self.check_overflow)
		self._type = WidgetEnum.Widgets.TEXT
	
	def set_data(self, data:str) ->None:
		self.setPlainText(data)

	def get_data(self) -> str:
		data = self.toPlainText()
		return data

	def check_overflow(self) -> None:
		if self.verticalScrollBar().maximum() > 0:
			self.text_overflow.emit(self._cell)
	
	def resizeEvent(self, event):
		font = self.font()
		font.setPixelSize(self.height() // 15)
		self.setFont(font)

	def setup_widget(self, *args, **kwargs):
		cell = kwargs.pop('cell', None)
		if cell:
			self.set_cell(cell)
		data = kwargs.pop('data', None)
		if data:
			self.setPlainText(data[2])

class TransparentTable(QTableWidget):
	def __init__(self, *args, **kwargs):
		super(TransparentTable, self).__init__(*args, **kwargs)

	def mouseMoveEvent(self, event):
		event.ignore()

class MTableWidget(QWidget, MCellWidget):
	def __init__(self, *args, **kwargs):
		super(MTableWidget, self).__init__(*args, **kwargs)
		self.table = TransparentTable(self)
		self.setObjectName("MTableWidget")
		self.table.setColumnCount(2)
		self.table.setRowCount(3)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.setMouseTracking(True)
		self.installEventFilter(self)
		self.setMouseTracking(True)

		self.setStyleSheet("""
					 		*{ font-family : Arial; font-size : 20px; }
					 		*>QTableWidget { border : none; border-radius: 5px; border-right: 3px solid rgba(35, 37, 40, 0); border-bottom: 3px solid rgba(35, 37, 40, 0); }
					 		*>QTableWidget:focus { border : none; border-radius: 5px; border-right: 3px solid rgba(35, 37, 40, 200); border-bottom: 3px solid rgba(35, 37, 40, 200);}
					 		*>QTableWidget:hover { border : none; border-radius: 5px; border-right: 3px solid rgba(35, 37, 40, 100); border-bottom: 3px solid rgba(35, 37, 40, 100);}
					 	""")

		self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.table.horizontalHeader().hide()
		self.table.verticalHeader().hide()

		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.layout = QGridLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.layout.addWidget(self.table, 0, 0, 2, 2)

		self.add_col_button = QPushButton(self)
		self.add_col_button.setText("+")
		self.add_col_button.setMaximumSize(15, 16777215)
		self.add_col_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.add_col_button.clicked.connect(lambda: self.table.setColumnCount(self.table.columnCount() + 1))
		self.rem_col_button = QPushButton(self)
		self.rem_col_button.setText("-")
		self.rem_col_button.setMaximumSize(15, 16777215)
		self.rem_col_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.rem_col_button.clicked.connect(lambda: self.table.setColumnCount(self.table.columnCount() - 1))

		self.add_row_button = QPushButton(self)
		self.add_row_button.setText("+")
		self.add_row_button.setMaximumSize(16777215, 15)
		self.add_row_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.add_row_button.clicked.connect(lambda: self.table.setRowCount(self.table.rowCount() + 1))
		self.rem_row_button = QPushButton(self)
		self.rem_row_button.setText("-")
		self.rem_row_button.setMaximumSize(16777215, 15)
		self.rem_row_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.rem_row_button.clicked.connect(lambda: self.table.setRowCount(self.table.rowCount() - 1))

		self.layout.addWidget(self.add_col_button, 0, 2)
		self.layout.addWidget(self.rem_col_button, 1, 2)
		self.layout.addWidget(self.rem_row_button, 2, 0)
		self.layout.addWidget(self.add_row_button, 2, 1)

		self.add_col_button.hide()
		self.rem_col_button.hide()
		self.add_row_button.hide()
		self.rem_row_button.hide()

		self._type = WidgetEnum.Widgets.TABLE

	def resizeEvent(self, event):
		font = self.table.font()
		font.setPixelSize(self.height() // 20)
		self.table.setFont(font)

	def eventFilter(self, source, event):
		if event.type() == QEvent.MouseButtonPress:
			if not self.geometry().contains(event.globalPos()):
				self.clearSelection()

		if event.type() == QEvent.MouseMove:
			pos = event.pos()
			if pos.x() > self.width() * 0.9:
				self.add_col_button.show()
				self.rem_col_button.show()
			else:
				self.add_col_button.hide()
				self.rem_col_button.hide()
			
			if pos.y() > self.height() * 0.90:
				self.add_row_button.show()
				self.rem_row_button.show()
			else:
				self.add_row_button.hide()
				self.rem_row_button.hide()
	
		return super(MTableWidget, self).eventFilter(source, event)
	
	def set_data(self, data:tuple) ->None:
		self.table.setRowCount(data[0])
		self.table.setColumnCount(data[1])
		data = data[2:]
		for i in range(self.table.rowCount()):
			for j in range(self.table.columnCount()):
				if data[i * self.table.columnCount() + j] is not None:
					self.table.setItem(i, j, QTableWidgetItem(data[i * self.table.columnCount() + j]))
	
	def get_data(self) -> tuple:
		data = [self.table.rowCount(), self.table.columnCount()]
		for i in range(self.table.rowCount()):
			for j in range(self.table.columnCount()):
				if self.table.item(i, j) is not None:
					data.append(self.table.item(i, j).text())
					continue
				data.append(None)
		
		return tuple(data)
	
	def setup_widget(self, *args, **kwargs):
		cell = kwargs.pop('cell', None)
		if cell:
			self.set_cell(cell)
		data = kwargs.pop('data', None)
		if data:
			self.set_data(data)

class MCalendarWidget(QCalendarWidget, MCellWidget):
	def __init__(self, *args, **kwargs):
		super(MCalendarWidget, self).__init__(*args, **kwargs)
		self.setObjectName("MCalendarWidget")

	def set_cell(self, cell:tuple):
		self._cell = cell
	
	def get_cell(self):
		return self._cell
	
	def set_data(self, data:str):
		self.setSelectedDate(QDate.fromString(data, "yyyy-MM-dd"))

	def get_data(self):
		return self.selectedDate().toString("yyyy-MM-dd")
	
	def setup_widget(self, *args, **kwargs):
		pass

class MCheckListWidget(QWidget, MCellWidget):
	def __init__(self, *args, **kwargs):
		super(MCheckListWidget, self).__init__(*args, **kwargs)
		self.setObjectName("MCheckListWidget")
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.outer_layout = QVBoxLayout()
		self.outer_layout.setContentsMargins(0, 0, 0, 0)
		self.outer_layout.setSpacing(0)
		self.setLayout(self.outer_layout)

		self.row = 0
		
		self.outer_layout.addLayout(self.layout)

		self.add_button = QPushButton("+")
		self.add_button.setMaximumSize(16777215, 15)
		self.add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.add_button.clicked.connect(self.new_item)

		self.sub_button = QPushButton("-")
		self.sub_button.setMaximumSize(16777215, 15)
		self.sub_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.sub_button.clicked.connect(self.remove_item)

		self.action_layout = QHBoxLayout()
		self.action_layout.setContentsMargins(0, 0, 0, 0)
		self.action_layout.setSpacing(0)

		self.action_layout.addWidget(self.sub_button)
		self.action_layout.addWidget(self.add_button)

		self.outer_layout.addLayout(self.action_layout)

		self.item = []
		self.layouts= []

	def new_item(self, ischecked:bool=None, text:str=None):
		layout = QHBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

		check_box = QCheckBox(self)
		check_box.setFixedWidth(20)
		check_box.setFixedHeight(20)
		check_box.setChecked(ischecked)

		line_edit = QLineEdit(self)
		line_edit.setFixedHeight(20)
		line_edit.setText(text)

		layout.addWidget(check_box)
		layout.addWidget(line_edit)

		self.layout.addLayout(layout)
		self.layouts.append(layout)
		index = self.row
		self.item.append((check_box, line_edit))
		self.row += 1
		self.check_state_changed(index)
		check_box.stateChanged.connect(lambda: self.check_state_changed(index))

	def check_state_changed(self, index:int):
		font = self.item[index][1].font()
		font.setStrikeOut(self.item[index][0].isChecked())
		self.item[index][1].setFont(font)

	def remove_item(self):
		self.layout.removeLayout(self.layouts[-1])
		self.layouts.pop()
		self.item.pop()

	def set_data(self, data:str):
		data = json.loads(data)
		for item in data:
			if item:
				self.new_item(ischecked = item[0], text = item[1])

	def get_data(self) -> tuple:
		data = []
		for i in self.item:
			data.append((i[0].isChecked(), i[1].text()))
		data = json.dumps(data)
		return data

	def setup_widget(self, *args, **kwargs):
		cell = kwargs.pop('cell', None)
		if cell:
			self.set_cell(cell)
		data = kwargs.pop('data', None)
		if data:
			self.set_data(data)

class WidgetEnum(QObject):
	class Widgets:
		TEXT, TABLE, DELETE, CHECKLIST= range(4)

	_widgets = (MPlainTextEdit, MTableWidget, None, MCheckListWidget)

	@classmethod
	def get_widget(cls, widget):
		return cls._widgets[widget]
	

if __name__ == "__main__":
	import sys
	from PyQt5.QtWidgets import QApplication
	app = QApplication(sys.argv)
	window = MCalendarWidget()
	window.show()
	sys.exit(app.exec_())
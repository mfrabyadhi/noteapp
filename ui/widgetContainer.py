from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np

from ui.custom_widget_enum import WidgetEnum

class WidgetContainerFrame(QtWidgets.QWidget):
	size_changed = QtCore.pyqtSignal(int, int)
	def __init__(self, *args, **kwargs):
		super(WidgetContainerFrame, self).__init__(*args, **kwargs)
		self.setObjectName("WidgetContainerFrame")
		self.setMouseTracking(True)
		self.layout = QtWidgets.QGridLayout(self)
		self.layout.setContentsMargins(10, 10, 10, 10)
		self.layout.setSpacing(10)
		self.setLayout(self.layout)

		self.add_row_button = QtWidgets.QPushButton(self)
		self.add_row_button.setObjectName("add_row_button")
		self.add_row_button.setText("+")
		self.add_row_button.setMinimumSize(0, 40)
		self.add_row_button.setMaximumSize(16777215, 40)
		self.add_row_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.add_row_button.clicked.connect(lambda: self._size_changed(1, 0))
		self.layout.addWidget(self.add_row_button, 2, 1, 1, 1)

		self.rem_row_button = QtWidgets.QPushButton(self)
		self.rem_row_button.setObjectName("rem_row_button")
		self.rem_row_button.setText("-")
		self.rem_row_button.setMinimumSize(0, 40)
		self.rem_row_button.setMaximumSize(16777215, 40)
		self.rem_row_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.rem_row_button.clicked.connect(lambda: self._size_changed(-1, 0))
		self.layout.addWidget(self.rem_row_button, 2, 0, 1, 1)

		self.add_col_button = QtWidgets.QPushButton(self)
		self.add_col_button.setObjectName("add_col_button")
		self.add_col_button.setText("+")
		self.add_col_button.setMinimumSize(40, 0)
		self.add_col_button.setMaximumSize(40, 16777215)
		self.add_col_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.add_col_button.clicked.connect(lambda: self._size_changed(0, 1))
		self.layout.addWidget(self.add_col_button, 0, 2, 1, 1)

		self.rem_col_button = QtWidgets.QPushButton(self)
		self.rem_col_button.setObjectName("rem_col_button")
		self.rem_col_button.setText("-")
		self.rem_col_button.setMinimumSize(40, 0)
		self.rem_col_button.setMaximumSize(40, 16777215)
		self.rem_col_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.rem_col_button.clicked.connect(lambda: self._size_changed(0, -1))
		self.layout.addWidget(self.rem_col_button, 1, 2, 1, 1)

	def _size_changed(self, row, col):
		self.size_changed.emit(row, col)

class WidgetContainer(QtWidgets.QTableWidget):
	# untuk menyimpan widget
	_widget:np.ndarray = np.empty((3,2), dtype=object)

	# sinyal buat menambah dan mengurangi widget
	widget_added = QtCore.pyqtSignal(int, int)
	widget_deleted = QtCore.pyqtSignal(int, int)

	def __init__(self, *args, **kwargs):
		super(WidgetContainer, self).__init__(*args, **kwargs)
		self.setObjectName("WidgetContainer")
		self.setRowCount(3)
		self.setColumnCount(2)
		self.horizontalHeader().hide()
		self.verticalHeader().hide()
		self.setShowGrid(False)
		self.setMouseTracking(True)
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		
		self.cell_style = """
				{ border : none; border-radius: 5px; border-right: 3px solid rgba(35, 37, 40, 0); border-bottom: 3px solid rgba(35, 37, 40, 0);
				background-color: #ff00ff;};
				:focus { border : none; border-radius: 5px; border-right: 3px solid rgba(35, 37, 40, 200); border-bottom: 3px solid rgba(35, 37, 40, 200);};
				:hover { border : none; border-radius: 5px; border-right: 3px solid rgba(35, 37, 40, 100); border-bottom: 3px solid rgba(35, 37, 40, 100);};
				"""
		self.resizeColumnsToContents()

		self.setStyleSheet("::item:selected {color: rgba(0,0,0,200); background-color: rgba(0,0,0,50); }")
		
		self.installEventFilter(self)
		self.setAcceptDrops(True)

		button = QtWidgets.QPushButton("test", self)
		button.setFixedSize(int(self.width() * 0.95), self.height())
		button.move(self.width() - button.width(), 0)

		self.add_column_button = button
		self.add_column_button.hide()

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.MouseButtonPress:
			if not self.geometry().contains(event.globalPos()):
				self.clearSelection()
		return super(WidgetContainer, self).eventFilter(source, event)

	def dragEnterEvent(self, event):
		if event.mimeData().hasFormat("type/widget"):
			print("dragged")
			event.accept()

	def dragMoveEvent(self, event):
		pos = event.pos()
		row, col = self.rowAt(pos.y()), self.columnAt(pos.x())
		cell = self.cellWidget(row, col)


	def dropEvent(self, event):
		if event.mimeData().hasFormat("type/widget"):
			data = event.mimeData().data("type/widget")
			_object = WidgetEnum.get_widget(int(data))
			
			pos = event.pos()
			row, col = self.rowAt(pos.y()), self.columnAt(pos.x())

			if self.cellWidget(row, col) is not None:
				if not 	_object:
					self._widget[row, col].deleteLater()
					self._widget[row, col] = None
					self.setCellWidget(row, col, None)
					self.widget_deleted.emit(row, col)
					return
				event.ignore()
				return
			else:
				if not _object:
					if not self.cellWidget(row, col - 1):
						event.ignore()
						return
					self._widget[row, col - 1].deleteLater()
					self._widget[row, col - 1] = None
					self.setSpan(row, col - 1, 1, 1)
					self.setCellWidget(row, col - 1, None)
					self.widget_deleted.emit(row, col - 1)
					return

			if isinstance(self.cellWidget(row, col - 1), _object):	
				self.setSpan(row, col - 1, 1, 2)
				self.update()
				self._widget[row, col - 1].update()
				self._widget[row, col - 1].set_span(1, 2)
				self.widget_added.emit(row, col - 1)
				return
			
			self.add_widget(_object, (row, col))
			self.widget_added.emit(row, col)
		event.accept()

	def clear_page(self) -> None:
		for row in range(self.rowCount()):
			for column in range(self.columnCount()):
				item = self.cellWidget(row, column)
				if item:
					item.deleteLater()
					self.setCellWidget(row, column, None)

	def new_page(self, row = 3, col = 2) -> None:
		self.clear_page()
		self._widget = np.empty((row, col),  dtype = object)
		self.setRowCount(row)
		self.setColumnCount(col)
		self.update()

	def add_widget(self, _object, cell, span = (1, 1), name = None, data = None):
		row, col = cell
		if self.cellWidget(row, col) is not None:
			return
		self._widget[row, col] = _object(self)
		self._widget[row, col].setup_widget(parent = self, cell = (row, col))
		self.setCellWidget(row, col, self._widget[row, col])
		self.setSpan(row, col, span[0], span[1])
		self.update()
		self._widget[row, col].update()
		self._widget[row, col].set_span(span[0], span[1])
		if name:
			self._widget[row, col].setObjectName(name)
		if data:
			self._widget[row, col].set_data(data)

	def get_widget(self, cell:tuple) -> QtWidgets.QWidget:
		return self.cellWidget(cell[0], cell[1])

if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	# widget with hboxlayout
	main_window = WidgetContainer()
	main_window.setObjectName("MainWindow")
	main_window.show()
	sys.exit(app.exec_())
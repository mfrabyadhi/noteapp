from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np

class WidgetContainer(QtWidgets.QTableWidget):
	# array of qobjects
	_widget:np.ndarray = np.empty((2,2), dtype=object)

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

		self.setAcceptDrops(True)

		button = QtWidgets.QPushButton("test", self)
		button.setFixedSize(int(self.width() * 0.95), self.height())
		button.move(self.width() - button.width(), 0)

		self.add_column_button = button
		self.add_column_button.hide()

	# def mouseMoveEvent(self, event):
	# 	if event.buttons() == QtCore.Qt.NoButton:
	# 		pos = event.pos()
	# 		if pos.x() > self.width() * 0.95:
	# 			self.add_column_button.show()
	# 		if pos.y() > self.height() * 0.95:
	# 			print("mouse is on the bottom side")

	# 	return super(WidgetContainer, self).mouseMoveEvent(event)

	def dragEnterEvent(self, event):
		if event.mimeData().hasFormat("type/widget"):
			print("dragged")
			event.accept()

	def dragMoveEvent(self, event):
		pos = event.pos()
		row, col = self.rowAt(pos.x()), self.columnAt(pos.y())
		print(col, row)
		# cell = self.itemAt(pos_x, pos_y)
		# self.setCurrentItem(cell)

	def dropEvent(self, event):
		print("dropped")
		if event.mimeData().hasFormat("type/widget"):
			event.accept()
			pos = event.pos()
			row, col = self.rowAt(pos.x()), self.columnAt(pos.y())
			print(row, col)

			if self._widget[row, col] is None:
				self._widget[row, col] = QtWidgets.QLabel("test")
				self.setCellWidget(row, col, self._widget[row, col])

	

	# def mouseMoveEvent(self, event):
	# 	pos = event.pos()
	# 	row = self.rowAt(pos.y())
	# 	col = self.columnAt(pos.x())
	# 	self.setCurrentCell(row, col)

class DragButton(QtWidgets.QPushButton):

    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            drag.setMimeData(mime)
            drag.setHotSpot(e.pos() - self.rect().topLeft())

            pixmap = QtGui.QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(QtCore.Qt.MoveAction)



# mainwindow
class temp(QtWidgets.QMainWindow):
	main_window_resized_signal = QtCore.pyqtSignal(QtCore.QEvent)
	main_window_moved_signal = QtCore.pyqtSignal(QtCore.QEvent)

	def __init__ (self, *args, **kwargs):
		super(temp, self).__init__(*args, **kwargs)
		self.setObjectName("MainWindow")
		self.resize(640, 480)
		self.layout = QtWidgets.QHBoxLayout()
		self.widget_sidebar = SidebarContainer(self)
		self.widget_container = WidgetContainer(self)
		self.layout.addWidget(self.widget_container)
		self.setLayout(self.layout)

		self.main_window_resized_signal.connect(self.widget_sidebar.main_window_resized)
		self.main_window_moved_signal.connect(self.widget_sidebar.main_window_moved)
		pos = self.pos()
		self.widget_sidebar.resize(int(self.width() / 10), self.height())
		self.widget_sidebar.move(self.width() - self.widget_sidebar.width(), 0)
		self.widget_sidebar.show()

	def resizeEvent(self, event):
		super(temp, self).resizeEvent(event)
		self.main_window_resized_signal.emit(event)

	def moveEvent(self, event):
		super(temp, self).moveEvent(event)
		self.main_window_moved_signal.emit(event)

if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	# widget with hboxlayout
	main_window = WidgetContainer()
	main_window.setObjectName("MainWindow")
	main_window.show()
	sys.exit(app.exec_())
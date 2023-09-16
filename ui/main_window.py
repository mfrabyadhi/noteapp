from PyQt5 import QtCore, QtGui, QtWidgets
from widgetContainer import WidgetContainer
from sidebarContainer import SidebarContainer
from menu_bar import MenuBar
import numpy as np

class MMainWindow(QtWidgets.QMainWindow):
	_main_window_resized_signal = QtCore.pyqtSignal()
	_main_window_moved_signal = QtCore.pyqtSignal()
	def __init__(self, *args, **kwargs):
		super(MMainWindow, self).__init__(*args, **kwargs)
		self.setObjectName("MainWindow")
		self.resize(800, 600)
		self.setMinimumSize(800, 600)


		self._central_widget = CentralWidget(self)
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.layout.addWidget(self._central_widget)


class CentralWidget(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super(CentralWidget, self).__init__(*args, **kwargs)

		self.setObjectName("CentralWidget")
		self._layout = QtWidgets.QHBoxLayout(self)
		self._layout.setContentsMargins(0, 0, 0, 0)
		self._layout.setSpacing(0)

		self._widget_menubar = MenuBar(self)
		self._widget_sidebar = SidebarContainer(self)
		self._widget_container = WidgetContainer(self)
		
		self._layout.addWidget(self._widget_menubar)
		self._layout.addWidget(self._widget_sidebar)
		self._layout.addWidget(self._widget_container)


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	main = CentralWidget()
	main.show()
	sys.exit(app.exec_())


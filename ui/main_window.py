from PyQt5 import QtCore, QtGui, QtWidgets
from ui.widgetContainer import WidgetContainer
from ui.sidebarContainer import SidebarContainer
from ui.menu_bar import MenuBar
from ui.login_page import LoginPage
import numpy as np

class Noted(QtWidgets.QMainWindow):
	_main_window_resized_signal = QtCore.pyqtSignal()
	_main_window_moved_signal = QtCore.pyqtSignal()
	def __init__(self, *args, **kwargs):
		super(Noted, self).__init__(*args, **kwargs)
		self.setObjectName("MainWindow")
		self.resize(1000, 600)
		self.setMinimumSize(1000, 600)

		self.setAutoFillBackground(True)

		self._central_widget = CentralWidget(self)
		self.setCentralWidget(self._central_widget)

class CentralWidget(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super(CentralWidget, self).__init__(*args, **kwargs)

		self.setObjectName("CentralWidget")
		self._layout = QtWidgets.QHBoxLayout(self)
		self._layout.setContentsMargins(0, 0, 0, 0)
		self._layout.setSpacing(0)

		# self.setAutoFillBackground(True)
		self.setStyleSheet("background-color: #f4f6fe;")

		self._widget_menubar = MenuBar(self)
		self._widget_sidebar = SidebarContainer(self)
		self._widget_container = WidgetContainer(self)

		self._widget_menubar.wid_button.clicked.connect(self._widget_sidebar.extend)
		
		self._layout.addWidget(self._widget_menubar,5)
		self._layout.addWidget(self._widget_sidebar,5)
		self._layout.addWidget(self._widget_container,5)
		
		self.login_page = LoginPage()
		self.login_page.show()
		self.login_page.activateWindow()

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	main = CentralWidget()
	main.show()
	sys.exit(app.exec_())


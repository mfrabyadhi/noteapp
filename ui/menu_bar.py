from PyQt5 import QtCore, QtGui, QtWidgets
# from menu_bar_setup import MenuBarSetup
from collapsible_box import CollapsibleBox

class MenuBar(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super(MenuBar, self).__init__(*args, **kwargs)

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		
		self.head_layout = QtWidgets.QHBoxLayout()
		self.head_layout.setContentsMargins(0,0,0,0)
		self.head_layout.setSpacing(0)
		self.head_layout.setAlignment(QtCore.Qt.AlignCenter)

		self.layout.addLayout(self.head_layout)

		button = QtWidgets.QPushButton("account")
		button.setMinimumSize(50, 50)
		button.setMaximumSize(50, 50)

		self.head_layout.addStretch(1)
		self.head_layout.addWidget(button)
		self.head_layout.addStretch(1)
		
		button = QtWidgets.QPushButton("widget")
		button.setMinimumSize(50, 50)
		button.setMaximumSize(50, 50)

		self.head_layout.addWidget(button)
		self.head_layout.addStretch(1)
		self.test = CollapsibleBox("test")
		layout = QtWidgets.QVBoxLayout()
		for i in range(5):
			layout.addWidget(QtWidgets.QPushButton("test"))
		self.test.setContentLayout(layout)
		self.layout.addWidget(self.test)
		self.setMaximumSize(200, 16777215)
		self.setMinimumSize(200, 0)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	main = MenuBar()
	main.show()
	sys.exit(app.exec_())
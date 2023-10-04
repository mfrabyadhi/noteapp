from PyQt5 import QtCore, QtGui, QtWidgets
# from menu_bar_setup import MenuBarSetup
from ui.collapsible_box import NoteList

class MenuBar(QtWidgets.QWidget):
	page_changed = QtCore.pyqtSignal(str, str)
	def __init__(self, *args, **kwargs):
		super(MenuBar, self).__init__(*args, **kwargs)
		self.setObjectName("MenuBar")
		self.setAutoFillBackground(True)
		style = """
		QWidget:not(QPushButton):not(QScrollArea) {
			background: rgba(123, 235, 255, 255);
		}

		QScrollArea {
			background: rgba(255, 255, 255, 255);
			border: none;
			border-radius: 5px;
		}

		#menuBar QWidget:not(QPushButton):not(QScrollArea) {
			background: rgba(255, 255, 255, 175);
		}

		QPushButton {
			background: rgba(163, 188, 249, 50);
			border: none;
			border-radius: 5px;
			border-right: 1px solid rgba(35, 37, 40, 255);
			border-bottom: 1px solid rgba(35, 37, 40, 255);
		}

		QPushButton::hover {
			background: rgba(163, 188, 249, 150);
		}
		QPushButton::pressed {
			background: rgba(163, 188, 249, 255);
		}
		"""

		self.setStyleSheet(style)

		self.resize(100, 600)
		self.setMaximumWidth(200)

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0,10,0,10)
		self.layout.setSpacing(0)
		
		self.head_layout = QtWidgets.QHBoxLayout()
		self.head_layout.setContentsMargins(0,0,0,0)
		self.head_layout.setSpacing(1)
		self.head_layout.setAlignment(QtCore.Qt.AlignCenter)

		self.head_menu_layout = QtWidgets.QVBoxLayout()
		self.head_menu_layout.setContentsMargins(0,0,0,0)
		self.head_menu_layout.setSpacing(0)
		self.head_menu_layout.setAlignment(QtCore.Qt.AlignCenter)

		self.head_action_layout = QtWidgets.QHBoxLayout()
		self.head_action_layout.setContentsMargins(0,0,0,0)
		self.head_action_layout.setSpacing(0)
		self.head_action_layout.setAlignment(QtCore.Qt.AlignCenter)

		self.acc_button = QtWidgets.QPushButton("account")
		self.acc_button.setIcon(QtGui.QIcon("ui/images/note.png"))
		self.acc_button.setMinimumSize(0, 0)
		self.acc_button.setMaximumSize(16777215, 16777215)
		self.acc_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.head_menu_layout.addWidget(self.acc_button, 14)

		self.head_menu_layout.addLayout(self.head_action_layout, 9)
		self.head_layout.addLayout(self.head_menu_layout)
		self.layout.addLayout(self.head_layout, 1)
		
		self.add_note_button = QtWidgets.QPushButton()
		self.add_note_button.setIcon(QtGui.QIcon("ui/images/plus.png"))
		self.add_note_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.head_action_layout.addWidget(self.add_note_button, 1)

		self.save_button = QtWidgets.QPushButton()
		self.save_button.setIcon(QtGui.QIcon("ui/images/save.png"))
		self.save_button.setMinimumSize(0, 0)
		self.save_button.setMaximumSize(16777215, 16777215)
		self.save_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.head_action_layout.addWidget(self.save_button, 1)

		self.wid_button = QtWidgets.QPushButton()
		self.wid_button.setIcon(QtGui.QIcon("ui/images/arrow.png"))
		self.wid_button.setMinimumSize(0, 100)
		self.wid_button.setMaximumSize(30, 16777215)
		self.wid_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.head_layout.addWidget(self.wid_button, 1)

		self.scroll_area = QtWidgets.QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
		self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scroll_area.setContentsMargins(0, 0, 0, 0)
		self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

		self.layout.addWidget(self.scroll_area, 9)

		self.widget = QtWidgets.QWidget()
		self.widget_layout = QtWidgets.QVBoxLayout(self.widget)
		self.widget_layout.setContentsMargins(0, 10, 0, 0)
		self.widget_layout.setSpacing(5)
		self.widget_layout.setAlignment(QtCore.Qt.AlignTop)
		
		self.scroll_area.setWidget(self.widget)

		self.add_note_button.clicked.connect(self.add_new_note)

		self.note = []

		# self.test = CollapsibleBox("test")
		# layout = QtWidgets.QVBoxLayout()

		# for i in range(5):
		# 	button = QtWidgets.QPushButton("test")
		# 	layout.addWidget(button)
		# self.test.setContentLayoutOut(layout)
		# self.widget_layout.addWidget(self.test)
		# self.setMaximumSize(200, 16777215)
		# self.setMinimumSize(200, 0)

	def add_new_note(self, name:str = "", pages:str = None) -> NoteList:
		if not name:
			name = "Note-" + str(len(self.note) + 1)
		self.note.append(NoteList(name))
		self.note[-1].setObjectName(name)
		self.add_new_page(self.note[-1])
		
		self.widget_layout.addWidget(self.note[-1])
		self.note[-1].page_changed.connect(self._page_changed)

		return self.note[-1]
	
	def add_note(self, note:str, pages:list = None) -> NoteList:
		self.note.append(NoteList(note, pages))
		self.note[-1].setObjectName(note)
		self.widget_layout.addWidget(self.note[-1])
		self.note[-1].page_changed.connect(self._page_changed)

		return self.note[-1]

	def get_num_notes(self):
		return len(self.note)
	
	def get_notes(self):
		return self.note

	def add_new_page(self, note, name=""):
		page = note.add_item(name)
		page.set_rowcol((3,2))
		return page

	def _page_changed(self, page_name):
		if not page_name:
			return
		note_name = self.sender().objectName()
		self.page_changed.emit(note_name, page_name)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	main = MenuBar()
	main.show()
	sys.exit(app.exec_())
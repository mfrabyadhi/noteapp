from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np

class SidebarContainer(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super(SidebarContainer, self).__init__(*args, **kwargs)
		self.setObjectName("SidebarContainer")
		# self.setStyleSheet("#SidebarContainer {border-radius: 5px; background-color: palette(base);}")

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(5)
		self.layout.setAlignment(QtCore.Qt.AlignCenter)
		self.setLayout(self.layout)

		self.setAutoFillBackground(True)
		self.setMaximumSize(75, 16777215)
		self.setMinimumSize(75, 0)

		pallete = self.palette()
		color = QtGui.QColor(30, 30, 30, 100)
		pallete.setColor(self.backgroundRole(), color)
		self.setPalette(pallete)

		self._widget:np.ndarray = np.empty(1, dtype=QtWidgets.QWidget)

		self._resizing = False

		widget = PseudoWidget(self)
		self._widget[0] = widget
		self.layout.addWidget(widget)
		widget = PseudoWidget(self)
		self._widget = np.append(self._widget, widget)
		self.layout.addWidget(widget)

	@QtCore.pyqtSlot()
	def main_window_resized(self, event):
		# self.resize(event)
		pass

	@QtCore.pyqtSlot()
	def main_window_moved(self):
		pass

	def dragEnterEvent(self, event):
		event.ignore()

		

class PseudoWidget(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super(PseudoWidget, self).__init__(*args, **kwargs)
		self.setMinimumSize(50, 50)
		self.setMaximumSize(50, 50)
		self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

		self.setAutoFillBackground(True)

		p = self.palette()
		p.setColor(self.backgroundRole(), QtCore.Qt.black)
		self.setPalette(p)

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)

		self._icon = QtWidgets.QLabel(self)
		self._text = QtWidgets.QLabel(self)
		self._text.setText("test")

	def setObjectName(self, name):
		super(PseudoWidget, self).setObjectName(name)
		self._text.setObjectName(name + "Text")

	def enterEvent(self, event):
		self._text.setStyleSheet("color: white;")
		self._icon.setStyleSheet("border: 1px solid white;")
		self.setStyleSheet("background-color: #1e1e1e;")
		super(PseudoWidget, self).enterEvent(event)

	def leaveEvent(self, event):
		self._text.setStyleSheet("color: gray;")
		self._icon.setStyleSheet("border: 1px solid gray;")
		self.setStyleSheet("background-color: black;")
		super(PseudoWidget, self).leaveEvent(event)

	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			mimeData = QtCore.QMimeData()
			mimeData.setData("type/widget", b"test")
			drag = QtGui.QDrag(self)
			drag.setMimeData(mimeData)
			drag.setHotSpot(event.pos() - self.rect().topLeft())
			drag.setPixmap(self.grab())
			drag.exec_(QtCore.Qt.MoveAction)

if (__name__ == "__main__"):
	import sys
	app = QtWidgets.QApplication(sys.argv)
	test = QtWidgets.QWidget()
	test.setObjectName("test")
	test.resize(640, 480)
	test.setStyleSheet("#test {background-color: blue;}")
	test.layout = QtWidgets.QHBoxLayout(test)
	test.layout.setContentsMargins(0, 0, 0, 0)
	test.layout.setSpacing(0)
	test.layout.setAlignment(QtCore.Qt.AlignCenter)
	widget = SidebarContainer(test)
	test.layout.addWidget(widget)
	test.show()
	sys.exit(app.exec())
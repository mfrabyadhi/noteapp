from PyQt5 import QtWidgets, QtCore, QtGui
from custom_widget_enum import WidgetEnum
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
		widget.setObjectType(WidgetEnum.Widgets.DELETE)
		widget.setText("DELETE")
		widget.setIcon("ui/images/delete.svg")
		self._widget[0] = widget
		self.layout.addWidget(widget)
		widget = PseudoWidget(self)
		widget.setObjectType(WidgetEnum.Widgets.TEXT)
		widget.setText("TEXT")
		widget.setIcon("ui/images/text.svg")
		self._widget = np.append(self._widget, widget)
		self.layout.addWidget(widget)
		widget = PseudoWidget(self)
		widget.setObjectType(WidgetEnum.Widgets.TABLE)
		widget.setText("TABLE")
		widget.setIcon("ui/images/table.svg")
		self._widget = np.append(self._widget, widget)
		self.layout.addWidget(widget)
		widget = PseudoWidget(self)
		widget.setObjectType(WidgetEnum.Widgets.CHECKLIST)
		widget.setText("CHECK")
		widget.setIcon("ui/images/checkbox.svg")
		self._widget = np.append(self._widget, widget)
		self.layout.addWidget(widget)



		self.animation = QtCore.QParallelAnimationGroup(self)

		animation = QtCore.QPropertyAnimation(self, b"maximumWidth")
		animation.setDuration(300)
		animation.setStartValue(0)
		animation.setEndValue(75)
		self.animation.addAnimation(animation)

		animation = QtCore.QPropertyAnimation(self, b"minimumWidth")
		animation.setDuration(300)
		animation.setStartValue(0)
		animation.setEndValue(75)
		self.animation.addAnimation(animation)

		self.extended = True
		self.extend()

	@QtCore.pyqtSlot()
	def extend(self):
		if not self.extended:
			self.animation.setDirection(QtCore.QAbstractAnimation.Forward)
			self.animation.start()
			self.extended = True
			self.show()
			for i in self.children():
				if isinstance(i, PseudoWidget):
					i.show()
		else:
			for i in self.children():
				if isinstance(i, PseudoWidget):
					i.hide()
			self.animation.setDirection(QtCore.QAbstractAnimation.Backward)
			self.animation.start()
			self.extended = False
		self.animation.finished.connect(self.show_self)

	def show_self(self):
		self.setVisible(self.extended)

	def dragEnterEvent(self, event):
		event.ignore()

class PseudoWidget(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		icon = kwargs.pop("icon", None)
		text = kwargs.pop("text", None)
		super(PseudoWidget, self).__init__(*args, **kwargs)
		self.setMinimumSize(50, 50)
		self.setMaximumSize(50, 50)
		self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

		self.setAutoFillBackground(True)

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)

		self._icon = QtWidgets.QLabel(self)
		self._icon.setAlignment(QtCore.Qt.AlignCenter)
		icon = QtGui.QIcon(icon)
		self._icon.setPixmap(icon.pixmap(32, 32))
		self._text = QtWidgets.QLabel(self)
		self._text.setAlignment(QtCore.Qt.AlignCenter)
		self._text.setText(text)

		self.layout.addWidget(self._icon, 4)
		self.layout.addWidget(self._text, 1)
		
		self.type = None
	
	def setIcon(self, icon):
		icon = QtGui.QIcon(icon)
		self._icon.setPixmap(icon.pixmap(32, 32))

	def setText(self, text):
		self._text.setText(text)

	def setObjectName(self, name):
		super(PseudoWidget, self).setObjectName(name)
		self._text.setObjectName(name + "Text")

	def setObjectType(self, type:WidgetEnum.Widgets):
		self.type = type

	def enterEvent(self, event):
		self._text.setStyleSheet("color: white;")
		self._icon.setStyleSheet("border: 1px solid white;")
		super(PseudoWidget, self).enterEvent(event)

	def leaveEvent(self, event):
		self._text.setStyleSheet("color: gray;")
		self._icon.setStyleSheet("border: 1px solid gray;")
		super(PseudoWidget, self).leaveEvent(event)

	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			mimeData = QtCore.QMimeData()
			mimeData.setData("type/widget", bytes(str(self.type), "utf-8"))
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
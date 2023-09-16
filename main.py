from PyQt5 import QtWidgets, QtCore, QtGui

class Noted(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	noted = Noted()
	noted.show()
	sys.exit(app.exec_())
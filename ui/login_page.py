from PyQt5 import QtCore, QtWidgets, QtGui

class LoginPage(QtWidgets.QWidget):
	login_signal = QtCore.pyqtSignal(str, str)
	signup_signal = QtCore.pyqtSignal(str, str)

	def __init__(self, *args, **kwargs):
		super(LoginPage, self).__init__(*args, **kwargs)
		self.setObjectName("LoginPage")
		self.setAutoFillBackground(True)
		style = """
		#LoginPage {
			background-color: #66A3FF;
		}

		QLineEdit {
			background-color: rgba(255, 255, 255, 255);
			border: none;
			border-radius: 5px;
			border-right: 1px solid rgba(35, 37, 40, 255);
			border-bottom: 1px solid rgba(35, 37, 40, 255);
		}

		QLineEdit::hover {
			background-color: rgba(163, 188, 249, 255);
		}

		QPushButton {
			background-color: rgba(100,100,100, 150);
			border: none;
			border-radius: 5px;
			border-right: 1px solid rgba(35, 37, 40, 255);
			border-bottom: 1px solid rgba(35, 37, 40, 255);
			font-size: 15px;
		}

		QPushButton::hover {
			background-color: rgba(163, 188, 249, 200);
		}

		QPushButton::pressed {
			background-color: rgba(163, 188, 249, 255);
		}

		QPushButton #Signup_button {
			background-color: rgba(100,100,100, 0);
		}

		"""

		self.resize(360, 480)
		self.setMaximumSize(360, 360)

		self.layout = QtWidgets.QGridLayout(self)
		self.layout.setContentsMargins(20,0,20,0)
		self.layout.setSpacing(5)
		self.layout.setAlignment(QtCore.Qt.AlignCenter)

		self.label = QtWidgets.QLabel("Welcome")
		self.label.setMinimumSize(0, 0)
		self.label.setMaximumSize(16777215, 50)
		self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName("label")
		self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
		self.layout.addWidget(self.label, 0, 1)

		self.username = QtWidgets.QLineEdit()
		self.username.setPlaceholderText("Username")
		self.username.setMinimumSize(0, 0)
		self.username.setMaximumSize(16777215, 50)
		self.username.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.layout.addWidget(self.username, 1, 1)

		self.password = QtWidgets.QLineEdit()
		self.password.setPlaceholderText("Password")
		self.password.setMinimumSize(0, 0)
		self.password.setMaximumSize(16777215, 50)
		self.password.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.layout.addWidget(self.password, 2, 1)

		self.login_button = QtWidgets.QPushButton("Login")
		self.login_button.setMinimumSize(0, 0)
		self.login_button.setMaximumSize(16777215, 50)
		self.login_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.setObjectName("login_button")
		self.layout.addWidget(self.login_button, 4, 1)

		self.signup_button = QtWidgets.QPushButton("Sign Up?")
		self.signup_button.setMinimumSize(0, 0)
		self.signup_button.setMaximumSize(16777215, 20)
		self.signup_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.setObjectName("signup_button")
		self.layout.addWidget(self.signup_button, 5, 1)
		
		self.setStyleSheet(style)

		self.login_button.clicked.connect(self.login_button_clicked)
		self.signup_button.clicked.connect(self.signup_button_clicked)

	def login_button_clicked(self):
		username = self.username.text()
		password = self.password.text()
		self.login_signal.emit(username, password)

	def signup_button_clicked(self):
		username = self.username.text()
		password = self.password.text()
		self.signup_signal.emit(username, password)

	def login_res(self, res:bool, type:bool):
		QtCore.QTimer.singleShot(2000, self.login_button_reset)

		if res:
			self.hide()
			return
		if not type:	
			self.login_button.setText("Login Failed")
			self.login_button.setStyleSheet("background-color: rgba(255, 0, 0, 155);")
			self.password.setText("")
			return
		self.login_button.setText("Username Already Exists")
		self.login_button.setStyleSheet("background-color: rgba(255, 0, 0, 155);")
		self.password.setText("")

	def login_button_reset(self):
		self.login_button.setText("Login")
		self.login_button.setStyleSheet("""QPushButton::hover {
											background-color: rgba(163, 188, 249, 255);
										}

										QPushButton #Signup_button {
											background-color: rgba(100,100,100, 0);
										}
										""")


	
	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.drawPixmap(self.rect(), QtGui.QPixmap("ui/images/background_login.png"))

if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	window = LoginPage()
	window.show()
	sys.exit(app.exec_())
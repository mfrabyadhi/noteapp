from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import os
import inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"ui")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"model")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from ui.main_window import Noted
from model.main_model import MainModel

class MainApp(QtWidgets.QApplication):	
	def __init__(self, *args, **kwargs):
		super(MainApp, self).__init__(*args, **kwargs)
		self._view = Noted()
		self._view.show()
		self._model = MainModel(view=self._view)

if __name__ == '__main__':
	app = MainApp(sys.argv)
	sys.exit(app.exec_())
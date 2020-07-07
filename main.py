import sys
from PyQt5.QtWidgets import QApplication
from GUI import *
import globalvar as gl


if __name__ == '__main__':
    gl._init()
    path = ''
    gl.set_value('path', '')
    app = QApplication(sys.argv)
    mainwindow = gui()
    mainwindow.show()
    sys.exit(app.exec_())
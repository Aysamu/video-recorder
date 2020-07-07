from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog
import child
import 录屏
from recorder import recorder
import globalvar as gl


class gui(QMainWindow, 录屏.Ui_mainWindow):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        self.about = childwindow()
        self.tool = recorder()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showtime)
        self.pushButton.clicked.connect(self.start)
        self.pushButton.clicked.connect(self.tool.run)
        self.pushButton_2.clicked.connect(self.timestop)
        self.pushButton_2.clicked.connect(self.tool.stop)
        self.toolButton.clicked.connect(self.showDialog)
        self.toolButton_2.clicked.connect(self.about.show)
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display('00:00:00')

    def start(self):
        self.curtime = 0
        self.timer.start(1000)

    def showtime(self):
        # 显示流逝的时间
        self.curtime = self.curtime + 1
        hours = self.curtime / 3600
        minutes_curtime = self.curtime % 3600
        minutes = minutes_curtime / 60
        seconds_curtime = minutes_curtime % 60
        seconds = seconds_curtime
        str_time = "%02d:%02d:%02d" % (hours, minutes, seconds)
        self.lcdNumber.display(str_time)

    def timestop(self):
        self.timer.stop()
        self.lcdNumber.display('00:00:00')

    def showDialog(self):
        path = gl.get_value('path')
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", ".")
        path = path + '/'
        gl.set_value('path', path)
        self.tool.__init__()


class childwindow(QDialog, child.Ui_Dialog):
    def __init__(self, parent=None):
        super(childwindow, self).__init__(parent)
        self.setupUi(self)
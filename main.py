import sys
import CountWidget
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
from PyQt5.QtCore import QTimer
import PyQt5.QtCore as QtCore
import time
import pyttsx3
import requests
import random


def engine(voice):
    engine = pyttsx3.init()
    engine.say(voice)
    engine.runAndWait()


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = CountWidget.Ui_Dialog()
        self.ui.setupUi(self)
        self.Labels = []
        self.CurrentLabel = -1
        self.DefaultColor = 'gray'
        self.HighLightColor = 'green'

        for i in range(10):
            for j in range(10):
                label = QLabel(str(i*10+j+1))
                label.setFixedSize(80,80)
                label.setAlignment(QtCore.Qt.AlignCenter)
                self._set_label_color(label,self.DefaultColor)
                self.Labels.append(label)
                self.ui.NumberLayout.addWidget(label, i, j)
        self.ui.RandomPickBtn.clicked.connect(self.RandomPick)
        self.ui.ClearBtn.clicked.connect(self.Clear)

        timer = QTimer()
        timer.timeout.connect(self.Scan)  # 计时器挂接到槽：update
        self.ui.ScanBtn.clicked.connect(lambda: timer.start(500))
        self.ui.RandomPickBtn.clicked.connect(lambda: timer.stop())
        self.ui.ClearBtn.clicked.connect(lambda: timer.stop())


    def _get_color_style(self,name):
        return "QLabel{{ font-size:25px;font-weight:bold;font-family:Roman times;background-color:{} }}".format(name)

    def _set_label_color(self, label, color):
        label.setStyleSheet(self._get_color_style(color))


    def ChangeLabel(self, num):
        if self.CurrentLabel != num:
            self._set_label_color(self.Labels[self.CurrentLabel], self.DefaultColor)
            self.CurrentLabel = num
            self._set_label_color(self.Labels[self.CurrentLabel], self.HighLightColor)
            self.repaint()
        engine(self.CurrentLabel+1)

    def Scan(self):
        if self.CurrentLabel >=-1 and self.CurrentLabel < 100:
            self.ChangeLabel(self.CurrentLabel + 1)
        else:
            self.CurrentLabel = 0

    def RandomPick(self):
        num = random.randint(0, 100)
        self.ChangeLabel(num)


    def Clear(self):
        print("Clear")

if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
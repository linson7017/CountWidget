import CountWidget
import PyQt5.QtCore as QtCore
import pyttsx3
import random
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
from number_to_word import num2word


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
                label = QLabel(str(i * 10 + j + 1))
                label.setFixedSize(80, 80)
                label.setAlignment(QtCore.Qt.AlignCenter)
                self._set_label_color(label, self.DefaultColor)
                self.Labels.append(label)
                self.ui.NumberLayout.addWidget(label, i, j)
        self.ui.RandomPickBtn.clicked.connect(self.RandomPick)
        self.ui.ResetBtn.clicked.connect(self.Reset)

        self.timer = QTimer()
        self.timer.timeout.connect(self.Refresh)  # 计时器挂接到槽：update
        self.ui.ScanBtn.clicked.connect(self.Scan)
        self.ui.RandomPickBtn.clicked.connect(self.StopScan)
        self.ui.ResetBtn.clicked.connect(self.StopScan)
        self.ui.ScanIntervalSlider.valueChanged.connect(self.InternalChanged)

    def _get_color_style(self, name):
        return "QLabel{{ font-size:25px;font-weight:bold;font-family:Roman times;background-color:{} }}".format(name)

    def _set_label_color(self, label, color):
        label.setStyleSheet(self._get_color_style(color))

    def _say_number(self, number):
        if self.ui.LanguageComboBox.currentIndex() == 0:
            engine(number)
        elif self.ui.LanguageComboBox.currentIndex() == 1:
            engine(num2word(number))
        else:
            engine(number)

    def ChangeLabel(self, num):
        if self.CurrentLabel != num:
            self._set_label_color(self.Labels[self.CurrentLabel], self.DefaultColor)
            self.CurrentLabel = num
            self._set_label_color(self.Labels[self.CurrentLabel], self.HighLightColor)
            self.repaint()
        self._say_number(self.CurrentLabel + 1)

    def Refresh(self):
        if self.CurrentLabel >= -1 and self.CurrentLabel < 100:
            self.ChangeLabel(self.CurrentLabel + 1)
        else:
            self.CurrentLabel = 0

    def Scan(self, checked):
        if checked:
            self.timer.start(self.ui.ScanIntervalSlider.value())
            self.ui.ScanIntervalSlider.setEnabled(False)
        else:
            self.StopScan()

    def StopScan(self):
        self.timer.stop()
        self.ui.ScanIntervalSlider.setEnabled(True)
        self.ui.ScanBtn.setChecked(False)

    def RandomPick(self):
        num = random.randint(0, 100)
        self.ChangeLabel(num)

    def InternalChanged(self):
        self.ui.InternalText.setText('{} ms'.format(self.ui.ScanIntervalSlider.value()))

    def Reset(self):
        self._set_label_color(self.Labels[self.CurrentLabel], self.DefaultColor)
        self.CurrentLabel = -1


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())

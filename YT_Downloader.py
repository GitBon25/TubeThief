from PyQt5 import QtWidgets, uic, QtCore
import sys, os, time, requests, pyperclip
from pytube import YouTube
from threading import Thread


class Main_UI(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("YT_Downloader.ui", self)

        self.pushButton.clicked.connect(lambda: self.lineEdit.setText(pyperclip.paste()))
        self.pushButton_2.clicked.connect(lambda: self.Check_Def())
        self.pushButton_3.clicked.connect(lambda: self.download_Def())
        self.pushButton_4.clicked.connect(lambda: self.clear_Def())


    def clear_Def(self):
        if "None" in str(self.comboBox.currentText()):
            pass
        else:
            self.comboBox.clear()
            self.comboBox.addItem("None")
        self.label.setText("")
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_4.setText("")
        self.label_5.setText("")
        self.lineEdit.clear()

    def Check_Def(self):
        try:
            request = requests.get("https://www.google.com", timeout=2)
            if self.radioButton.isChecked():
                self.high_Def()
            if self.radioButton_2.isChecked():
                self.Normal_Def()
            if self.radioButton_3.isChecked():
                self.Good_Def()
            if self.radioButton_4.isChecked():
                self.low_Def()
            pass
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.label_3.setText("Please Check Your Internet Connection")
            self.label_3.setStyleSheet("color: #FF0000")


    def high_Def(self):
        try:
            self.comboBox.clear()
            yt = YouTube(self.lineEdit.text())
            for stream in yt.streams:
                if "vp9.2" in str(stream.codecs):
                    self.comboBox.addItem(f'{str(stream.itag)}, Res - {str(stream.resolution)} ,  FPS - {str(stream.fps)} ,  Codec-{str(" ". join(stream.codecs)[0:5])} ,  Size - {str("{:.2f}".format(float(stream.filesize / 1024 / 1024)))} MiB')
        except Exception:
            self.exception_Def()

    def Normal_Def(self):
        try:
            self.comboBox.clear()
            yt = YouTube(self.lineEdit.text())
            for stream in yt.streams:
                if "vp9" in str(stream.codecs):
                    if "vp9.2" not in str(stream.codecs):
                        self.comboBox.addItem(f'{str(stream.itag)}, Res - {str(stream.resolution)} ,  FPS - {str(stream.fps)} ,  Codec - {str(" ". join(stream.codecs)[0:5])} ,  Size - {str("{:.2f}".format(float(stream.filesize / 1024 / 1024)))}  MiB')
        except Exception:
            self.exception_Def()

    def Good_Def(self):
        try:
            self.comboBox.clear()
            yt = YouTube(self.lineEdit.text())
            for stream in yt.streams:
                if "avc" in str(stream.codecs):
                    if "mp4a" not in str(stream.codecs):
                        self.comboBox.addItem(f'{str(stream.itag)}, Res - {str(stream.resolution)} ,  FPS - {str(stream.fps)} ,  Codec-{str(" ". join(stream.codecs)[0:4])} ,  Size - {str("{:.2f}".format(float(stream.filesize / 1024 / 1024)))}  MiB')
        except Exception:
            self.exception_Def()

    def low_Def(self):
        try:
            self.comboBox.clear()
            yt = YouTube(self.lineEdit.text())
            for stream in yt.streams:
                if "av0" in str(stream.codecs):
                    if "None" not in str(stream.resolution):
                        self.comboBox.addItem(f'{str(stream.itag)}, Res - {str(stream.resolution)} ,  FPS - {str(stream.fps)} ,  Codec-{str(" ". join(stream.codecs)[0:4])} ,  Size - {str("{:.2f}".format(float(stream.filesize / 1024 / 1024)))} MiB')
        except Exception:
            self.exception_Def()

    def exception_Def(self):
        self.comboBox.addItem("None")
        self.label.setText("")
        self.label_2.setText("")
        self.label_3.setText("Invalid Youtube URL")
        self.label_3.setStyleSheet("color: #FF0000")
        self.label_4.setText("")
        self.label_5.setText("")


    def download_Def(self):
        self.pushButton_3.setEnabled(False)
        Thread(target=self.download_Def1).start()

    def download_Def1(self):
        self.label.setText("")
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_4.setText("")
        self.label_5.setText("")
        try:
            self.pushButton_2.setEnabled(False)
            self.dYT0 = YouTube(self.lineEdit.text())
            self.label.setText("Please Wait")
            self.yta = self.dYT0.streams.get_by_itag("140").download()

            self.label_2.setText("Step One Complete")

            self.ne1 = str(self.comboBox.currentText()[0:3])
            self.dYT1 = YouTube(self.lineEdit.text())
            self.label_3.setText("Please Wait for Downloading..")
            self.label_3.setStyleSheet("color: #FFFFFF")
            self.ytv = self.dYT1.streams.get_by_itag(self.ne1).download()

            self.label_4.setText("Step Two Complete")

            os.system('ffmpeg -i "'+ self.ytv +'" -i "'+ self.yta +'" -map 0:v -map 1:a -c copy -y "'+ f'{str(self.dYT1.title)}{".mp4"}' +'"')

            os.remove(str(self.ytv))
            os.remove(str(self.yta))

            self.label_5.setText("Downloading Completed")
            self.label_5.setStyleSheet("color: #00FF00")
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)

        except Exception:
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.label.setText("")
            self.label_2.setText("")
            self.label_3.setText("Something Went Wrong")
            self.label_3.setStyleSheet("color: #FF0000")
            self.label_4.setText("")
            self.label_5.setText("")
        pass


if __name__ == "__main__":
    MainApp = QtWidgets.QApplication(sys.argv)
    App = Main_UI()
    App.show()
    sys.exit(MainApp.exec_())

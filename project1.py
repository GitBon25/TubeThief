import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt6.QtCore import Qt
from pytube import YouTube
from PyQt6 import uic


class YT_Downloader(QWidget):
    def __init__(self):
        super(YT_Downloader, self).__init__()
        uic.loadUi("project1.ui", self)
  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_form = YT_Downloader()
    card_form.show()
    sys.exit(app.exec())
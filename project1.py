import sys, os, time, requests, pyperclip
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import uic, QtCore
import pytube
from threading import Thread


class Window1(QMainWindow):
    def __init__(self):
        super(Window1, self).__init__()
        uic.loadUi("project1.ui", self)

        self.url_set.clicked.connect(lambda: self.url_edit.setText(pyperclip.paste()))
        self.down1.clicked.connect(self.show_new_window)

    def show_new_window(self, checked):
        self.w2 = Window2()
        self.w2.show()


class Window2(QMainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        uic.loadUi("project2.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_form = Window1()
    card_form.show()
    sys.exit(app.exec())

import sys, os, time, requests, pyperclip
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt6 import uic, QtCore
import pytube
from threading import Thread
import csv

links_file = "links.csv"
ytlink = ""


class Window1(QMainWindow):
    def __init__(self):
        super(Window1, self).__init__()
        uic.loadUi("project1.ui", self)  

        self.url_edit.setText(pyperclip.paste())  
        self.w2 = Window2()

        self.url_set.clicked.connect(lambda: self.url_edit.setText(pyperclip.paste()))
        self.down1.clicked.connect(self.show_new_window)

    def show_new_window(self):
        global ytlink
        ytlink = self.url_edit.text()  

        try:
            pytube.YouTube(ytlink)  
        except pytube.exceptions.RegexMatchError:
            msg = QMessageBox()
            msg.setWindowTitle("Invalid Link")
            msg.setText("Please enter a valid YouTube URL.")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return

        self.w2.show()
        self.close()


class Window2(QMainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        uic.loadUi("project2.ui", self)

        self.directory.setEnabled(False)
        self.download_button.clicked.connect(self.download)
        self.browse.clicked.connect(self.getDirectory)

    def download(self):
        try:
            youtubelink = pytube.YouTube(ytlink)
            video = youtubelink.streams.get_highest_resolution()
            video.download(output_path=self.directory.text())
            self.save_to_csv(ytlink)
        except pytube.exceptions.PytubeError as e:
            msg = QMessageBox()
            msg.setWindowTitle("Download error")
            msg.setText(f"Error downloading video: {e}")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()


    def getDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.directory.clear()
        self.directory.setText(directory)

    def save_to_csv(self, link):
        with open(links_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([link])

        msg = QMessageBox()
        msg.setWindowTitle("Download Complete")
        msg.setText(f"Video downloaded and link saved to '{links_file}'.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_form = Window1()
    card_form.show()
    sys.exit(app.exec())

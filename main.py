import sys, pyperclip, subprocess, pytube, csv, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtGui import QIcon
import yt_dlp as youtube_dl
from PIL import Image

ytlink = ""
directory = ""
video_audio = 0


class Window1(QMainWindow):
    def __init__(self):
        super(Window1, self).__init__()
        uic.loadUi("project1.ui", self)

        self.url_edit.setText(pyperclip.paste())
        self.w2 = Window2()

        self.url_set.clicked.connect(
            lambda: self.url_edit.setText(pyperclip.paste()))
        self.down1.clicked.connect(self.show_new_window)

        download_icon = QIcon("download.png")
        paste_icon = QIcon("paste.png")
        self.down1.setIcon(download_icon)
        self.url_set.setIcon(paste_icon)

    def show_new_window(self):
        global ytlink
        ytlink = str(self.url_edit.text())

        try:
            pytube.YouTube(ytlink)
        except pytube.exceptions.RegexMatchError:
            msg = QMessageBox()
            msg.setWindowTitle("Invalid Link")
            msg.setText("Please enter a valid YouTube URL.")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(ytlink, download=False)
            video_title = info_dict.get('title', None)
            uploader = info_dict.get("uploader", None)

        command = f"yt-dlp --write-thumbnail --skip-download -o \"thumbnail\" {
            ytlink}"
        subprocess.call(command, shell=True)
        output_size = (442, 224)
        output_image = "resized_thumbnail.webp"
        with Image.open("thumbnail.webp") as img:
            img = img.resize(output_size)
            img.save(output_image)
        self.w2.thumbnail.setStyleSheet(
            f"QFrame {{ background-image: url(resized_thumbnail.webp); background-repeat: no-repeat; background-position: center; }}")
        self.w2.title.setText(video_title)
        self.w2.uploader_title.setText(uploader)
        self.w2.show()
        self.close()


class Window2(QMainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        uic.loadUi("project2.ui", self)

        self.directory.setEnabled(False)
        self.download_button.clicked.connect(self.download)
        self.browse.clicked.connect(self.getDirectory)
        self.video.clicked.connect(self.video_butt)
        self.audio.clicked.connect(self.audio_butt)

        download_icon = QIcon("download.png")
        directory_icon = QIcon("directory.png")
        self.download_button.setIcon(download_icon)
        self.browse.setIcon(directory_icon)

        self.w3 = Window3

    def download(self):
        global video_audio
        if video_audio == 1:
            self.download_video()
        elif video_audio == 2:
            self.download_mp3()

    def download_video(self):
        try:
            global ytlink
            ydl_opts = {'format': 'bestvideo[height<=?4K]+bestaudio/best',
                        'outtmpl': f'{self.directory.text()}/%(title)s.%(ext)s'
                        }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.cache.remove()
                    ydl.download(ytlink)
                except youtube_dl.DownloadError as error:
                    pass
            self.save_to_csv(ytlink)
            self.w3 = Window3()
            self.w3.show()
            self.close()
        except pytube.exceptions.PytubeError as e:
            msg = QMessageBox()
            msg.setWindowTitle("Download error")
            msg.setText(f"Error downloading video: {e}")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def download_mp3(self):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{self.directory.text()}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.cache.remove()
                    ydl.download(ytlink)
                except youtube_dl.DownloadError as error:
                    pass
            self.save_to_csv(ytlink)
            self.w3 = Window3()
            self.w3.show()
            self.close()
        except pytube.exceptions.PytubeError as e:
            msg = QMessageBox()
            msg.setWindowTitle("Download error")
            msg.setText(f"Error downloading MP3: {e}")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def audio_butt(self):
        global video_audio
        video_audio = 2

    def video_butt(self):
        global video_audio
        video_audio = 1

    def getDirectory(self):
        global directory
        directory = QFileDialog.getExistingDirectory(
            self, "Выбрать папку", ".")
        self.directory.clear()
        self.directory.setText(directory)

    def save_to_csv(self, link):
        with open("links.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([link])


class Window3(QMainWindow):
    def __init__(self):
        super(Window3, self).__init__()
        uic.loadUi("project3.ui", self)
        self.view.clicked.connect(self.view_file)
        self.close_button.clicked.connect(self.close)

    def view_file(self):
        global directory
        if os.path.exists(directory):
            os.startfile(os.path.dirname(directory))
        else:
            print("Файл не найден.")

    def close(self):
        app = QApplication.instance()
        os.remove("thumbnail.webp")
        os.remove("resized_thumbnail.webp")
        app.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_form = Window1()
    card_form.show()
    sys.exit(app.exec())

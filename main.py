import sys, pyperclip, subprocess, pytube, csv, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtGui import QIcon
import yt_dlp as youtube_dl
from PIL import Image

ytlink = ""
directory = ""
video_audio = 0
test = 0
video_title = ""


class Window1(QMainWindow):
    def __init__(self):
        super(Window1, self).__init__()
        uic.loadUi("GUI/project1.ui", self)
        self.w2 = Window2()
        self.wI = WindowI()

        self.url_set.clicked.connect(
            lambda: self.url_edit.setText(pyperclip.paste()))
        self.down1.clicked.connect(self.show_new_window)
        self.geo_check.stateChanged.connect(self.check_geo_state)
        self.info.clicked.connect(self.show_info)
        self.down1.setToolTip("Переход к загрузке видео")
        self.url_set.setToolTip("Вставка ссылки")
        self.geo_check.setToolTip("Обход блокировок")

        download_icon = QIcon("ICONS/download.png")
        paste_icon = QIcon("ICONS/paste.png")
        info_icon = QIcon("ICONS/info.png")
        self.down1.setIcon(download_icon)
        self.url_set.setIcon(paste_icon)
        self.info.setIcon(info_icon)

    def show_info(self):
        self.wI.show()

    def check_geo_state(self):
        global test
        if self.geo_check.isChecked():
            test = 1
        else:
            test = 0

    def show_new_window(self):
        global ytlink
        global test
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

        if test == 1:
            ydl_opts = {'geo_bypass': True}
            command = f"yt-dlp --geo-bypass --write-thumbnail --skip-download -o \"thumbnail\" {
            ytlink}"
        else:
            ydl_opts = {}
            command = f"yt-dlp --write-thumbnail --skip-download -o \"thumbnail\" {
            ytlink}"
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            global video_title
            info_dict = ydl.extract_info(ytlink, download=False)
            video_title = info_dict.get('title', None)
            uploader = info_dict.get("uploader", None)

        subprocess.call(command, shell=True)
        available_resolutions = []
        for format in info_dict.get('formats', []):
            if format.get('vcodec') is not None and format.get('height') is not None:
                height = int(format.get('height'))
                if height not in available_resolutions and height > 180:
                    available_resolutions.append(str(height) + 'p')

        output_size = (442, 224)
        output_image = "resized_thumbnail.webp"
        with Image.open("thumbnail.webp") as img:
            img = img.resize(output_size)
            img.save(output_image)
        self.w2.thumbnail.setStyleSheet(
            f"QFrame {{ background-image: url(resized_thumbnail.webp); background-repeat: no-repeat; background-position: center; }}")
        self.w2.title.setText(video_title)
        self.w2.uploader_title.setText(uploader)
        self.w2.resolution.clear()
        self.w2.resolution.addItems(available_resolutions)
        self.w2.show()
        self.close()


class Window2(QMainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        uic.loadUi("GUI/project2.ui", self)

        self.directory.setEnabled(False)
        self.download_button.clicked.connect(self.download)
        self.browse.clicked.connect(self.getDirectory)
        self.video.clicked.connect(self.video_butt)
        self.audio.clicked.connect(self.audio_butt)
        self.download_button.setToolTip("Загрузка видео/аудио")
        self.browse.setToolTip("Выбор директории")
        self.video.setToolTip("Видео формат")
        self.audio.setToolTip("Аудио формат")

        download_icon = QIcon("ICONS/download.png")
        directory_icon = QIcon("ICONS/directory.png")
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
            global test
            global ytlink
            current_resolution = str(self.resolution.currentText())
            if test == 1:
                ydl_opts = {'format': f'bestvideo[height={current_resolution}]+bestaudio/best',
                            'geo_bypass': True,
                            'outtmpl': f'{self.directory.text()}/%(title)s.%(ext)s'
                            }
            else:
                ydl_opts = {'format': f'bestvideo[height={current_resolution}]+bestaudio/best',
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
        except pytube.exceptions.PytubeError as e:
            msg = QMessageBox()
            msg.setWindowTitle("Download error")
            msg.setText(f"Error downloading video: {e}")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def download_mp3(self):
        global test
        global ytlink
        try:
            if test == 1:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'geo_bypass': True,
                    'outtmpl': f'{self.directory.text()}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]}
            else:
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
        global video_title
        with open("links.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([link, video_title])


class Window3(QMainWindow):
    def __init__(self):
        super(Window3, self).__init__()
        uic.loadUi("GUI/project3.ui", self)
        self.view.clicked.connect(self.view_file)
        self.close_button.clicked.connect(self.close)

    def view_file(self):
        global directory
        if os.path.exists(directory):
            os.startfile(os.path.dirname(directory))
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Directory error")
            msg.setText(f"Directory not found")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def close(self):
        app = QApplication.instance()
        os.remove("thumbnail.webp")
        os.remove("resized_thumbnail.webp")
        app.quit()


class WindowI(QMainWindow):
    def __init__(self):
        super(WindowI, self).__init__()
        uic.loadUi("GUI/project4.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QToolTip { color: white}")
    card_form = Window1()
    card_form.show()
    sys.exit(app.exec())

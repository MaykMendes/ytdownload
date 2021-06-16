import sys
import os
from pytube import YouTube, Playlist
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QPushButton,
                             QLabel,
                             QLineEdit,
                             QRadioButton,
                             QComboBox,
                             QFileDialog)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 320)
        self.setWindowIcon(QIcon("image/yt.ico"))
        self.setWindowTitle("Ytdownload")

        with open("css/interface.css") as interface:
            self.setStyleSheet(interface.read())

        label = QLabel(self)
        label.setText("Put your link here:")
        label.move(30, 20)
        label.setObjectName("text")
        label.resize(200, 20)

        self.putlink = QLineEdit(self)
        self.putlink.move(30, 50)
        self.putlink.resize(450, 30)

        self.button = QPushButton("DOWNLOAD", self)
        self.button.move(210, 270)
        self.button.resize(80, 30)
        self.button.setObjectName("button")
        self.button.clicked.connect(self.download)

        self.buttondiretory = QPushButton("Choice a directory", self)
        self.buttondiretory.move(200, 230)
        self.buttondiretory.resize(100, 30)
        self.buttondiretory.clicked.connect(self.salvedownlaod)

        self.directory = QLabel('Directory:', self)
        self.directory.move(37, 200)

        label = QLabel(self)
        label.setText("Selection a format: ")
        label.move(30, 90)
        label.setObjectName("text")
        label.resize(200, 20)

        self.buttonMP4 = QRadioButton("MP4", self)
        self.buttonMP4.move(35, 120)
        self.buttonMP4.resize(40, 20)

        self.buttonMP3 = QRadioButton("MP3", self)
        self.buttonMP3.move(35, 140)
        self.buttonMP3.resize(40, 20)

        self.buttonMP4play = QRadioButton("MP4 PLAYLIST", self)
        self.buttonMP4play.move(35, 160)
        self.buttonMP4play.resize(90, 20)

        self.buttonMP3play = QRadioButton("MP3 PLAYLIST", self)
        self.buttonMP3play.move(35, 180)
        self.buttonMP3play.resize(90, 20)

        label = QLabel(self)
        label.setText("Selection a quality: ")
        label.move(380, 90)
        label.setObjectName("text")
        label.resize(200, 20)

        self.quality = QComboBox(self)
        self.quality.addItems(["High", "Medium", "Low"])
        self.quality.move(380, 120)
        self.quality.resize(90, 20)

    def salvedownlaod(self):
        self.file_ = QFileDialog.getExistingDirectory()

    def download(self):

        if self.buttonMP4.isChecked():
            downloadMP4 = self.putlink.text()
            yt = YouTube(downloadMP4)
            yt.streams.get_highest_resolution().download(self.file_)
            print(yt.title + " has been successfully downloaded.")

        elif self.buttonMP3.isChecked():
            download = self.putlink.text()
            yt = YouTube(download)
            video = yt.streams.filter(only_audio=True).first()
            print(f"Downloading {yt.title}")
            out_file = video.download(self.file_)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

        elif self.buttonMP4play.isChecked():
            download = self.putlink.text()
            PLAYLIST_URL = download
            playlist = Playlist(PLAYLIST_URL)
            print(f'downloading playlist: {playlist.title}...')
            for download in playlist.video_urls:
                video = YouTube(download)
                print(f'downloading {video.title}...')
                stream = video.streams.get_highest_resolution()
                stream.download(self.file_)

        elif self.buttonMP3play.isChecked():
            download = self.putlink.text()
            PLAYLIST_URL = download
            pl = Playlist(PLAYLIST_URL)
            print(f"Downloading Audios of {pl.title}")
            for download in pl.video_urls:
                yt = YouTube(download)
                stream = yt.streams.filter(only_audio=True).first()
                print(f"Downloading {yt.title}...")
                out_file = stream.download(self.file_)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)

            print("Your playlist audios has been succesful downloaded")

        else:
            print('Select a option!')


aplication = QApplication(sys.argv)
main = Window()
main.show()

sys.exit(aplication.exec_())

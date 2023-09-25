import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QRadioButton, QProgressBar, \
    QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer



class Downloader(QThread):
    progress = pyqtSignal(str)

    def __init__(self, url, quality, download_dir):
        super().__init__()
        self.url = url
        self.quality = quality
        self.download_dir = download_dir

    def run(self):
        self.download_video()

    def download_video(self):
        command = []

        if self.quality == "MP3 Only":
            command = ["yt-dlp", "-f", "bestaudio[ext=m4a]/bestaudio", "-x", "--audio-format", "mp3", "-o",
                       os.path.join(self.download_dir, "%(title)s.%(ext)s"), self.url]
        elif self.quality == "720p":
            command = ["yt-dlp", "-f", "best[height<=720][ext=mp4]", "-o",
                       os.path.join(self.download_dir, "%(title)s.%(ext)s"), self.url]
        elif self.quality == "1080p":
            command = ["yt-dlp", "-f",
                       "bestvideo[height<=?1080][vbr<=?10000][fps<=?120][ext=mp4]+bestaudio[abr<=?192]/best[ext=mp4]/best",
                       "-o", os.path.join(self.download_dir, "%(title)s.%(ext)s"), self.url]
        elif self.quality == "Highest Available":
            command = ["yt-dlp", "-f", "bestvideo+bestaudio[fps<=?120]", "-o",
                       os.path.join(self.download_dir, "%(title)s.%(ext)s"), self.url]

        # For now, simply notify the GUI that we are downloading and then complete.
        # Ideally, you would capture yt-dlp's output and update the progress bar more granularly.
        self.progress.emit("Downloading...")
        subprocess.run(command, capture_output=True)
        self.progress.emit("Complete!")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter YouTube URL")

        self.mp3_btn = QRadioButton("MP3 Only", self)
        self._720p_btn = QRadioButton("720p", self)
        self._1080p_btn = QRadioButton("1080p", self)
        self.highest_btn = QRadioButton("Highest Available", self)
        self.mp3_btn.setChecked(True)

        self.download_btn = QPushButton('Download', self)
        self.download_btn.clicked.connect(self.download_video)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_label = QLabel("", self)
        self.progress_bar.hide()
        self.progress_label.hide()

        layout.addWidget(self.url_input)
        layout.addWidget(self.mp3_btn)
        layout.addWidget(self._720p_btn)
        layout.addWidget(self._1080p_btn)
        layout.addWidget(self.highest_btn)
        layout.addWidget(self.download_btn)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setWindowTitle('YouTube Video Downloader')
        self.resize(400, 200)
        self.show()

    def download_video(self):
        url = self.url_input.text()
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        if self.mp3_btn.isChecked():
            quality = "MP3 Only"
        elif self._720p_btn.isChecked():
            quality = "720p"
        elif self._1080p_btn.isChecked():
            quality = "1080p"
        else:
            quality = "Highest Available"

        self.downloader = Downloader(url, quality, download_dir)
        self.downloader.progress.connect(self.update_progress)
        self.downloader.start()

    def update_progress(self, status):
        if status == "Downloading...":
            self.progress_label.setText("Downloading...")
            self.progress_label.show()
            self.progress_bar.setValue(50)
            self.progress_bar.show()
        elif status == "Complete!":
            self.progress_label.setText("Download Complete!")
            self.progress_bar.setValue(100)
            QTimer.singleShot(10000, self.progress_label.hide)  # hide status bar after 10 seconds
            QTimer.singleShot(10000, self.progress_bar.hide)


app = QApplication(sys.argv)
app.setStyleSheet("""
    QWidget {
        background-color: #333;
    }
    QLabel, QRadioButton {
        color: #fff;
    }
    QPushButton {
        background-color: #555;
        color: #fff;
        padding: 5px 15px;
        border: none;
    }
    QPushButton:hover {
        background-color: #666;
    }
    QLineEdit {
        background-color: #555;
        color: #fff;
        padding: 5px;
        border: none;
    }
""")
window = App()
sys.exit(app.exec_())
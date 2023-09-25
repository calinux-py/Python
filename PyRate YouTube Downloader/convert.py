import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QComboBox, QLabel, \
    QMessageBox
from PyQt5.QtGui import QIcon
from moviepy.editor import VideoFileClip
import os

class VideoConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.filePathLineEdit = QLineEdit(self)
        browseButton = QPushButton('Browse', self)
        browseButton.clicked.connect(self.browse_file)

        self.formatLabel = QLabel('Select output format:', self)
        self.formatComboBox = QComboBox(self)
        self.formatComboBox.addItems(['.mp4', '.avi', '.mkv', '.flv', '.mov'])

        convertButton = QPushButton('Convert', self)
        convertButton.clicked.connect(self.convert_video)

        self.conversionStatusLabel = QLabel('', self)

        layout.addWidget(self.filePathLineEdit)
        layout.addWidget(browseButton)
        layout.addWidget(self.formatLabel)
        layout.addWidget(self.formatComboBox)
        layout.addWidget(convertButton)
        layout.addWidget(self.conversionStatusLabel)

        self.setLayout(layout)

        self.setStyleSheet("""
        QWidget {
            background-color: #333;
        }
        QLabel, QPushButton, QComboBox, QLineEdit {
            color: #fff;
        }
        QPushButton {
            background-color: #555;
            border: 2px solid #888;
        }
        QPushButton:hover {
            background-color: #666;
        }
        """)

        self.setWindowTitle('PyRate Converter')
        self.setGeometry(100, 100, 400, 200)

    def browse_file(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Video File", "",
                                                  "Video Files (*.webm *.mp4 *.avi *.mkv *.flv *.mov);;All Files (*)",
                                                  options=options)
        if filePath:
            self.filePathLineEdit.setText(filePath)

    def convert_video(self):
        input_path = self.filePathLineEdit.text()
        output_format = self.formatComboBox.currentText()

        if not input_path:
            QMessageBox.warning(self, 'Warning', 'Please select a video file.')
            return

        self.conversionStatusLabel.setText("Converting... this may take awhile...")

        QApplication.processEvents()

        clip = VideoFileClip(input_path)
        output_path = input_path.rsplit('.', 1)[0] + output_format

        try:
            clip.write_videofile(output_path, codec='libx264' if output_format == '.mp4' else 'mpeg4')
            os.remove(input_path)
            self.conversionStatusLabel.setText("")
            QMessageBox.information(self, 'Success', 'Conversion has completed!')
        except Exception as e:
            self.conversionStatusLabel.setText("")
            QMessageBox.critical(self, 'Error', f"Error occurred: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoConverterApp()
    ex.show()
    sys.exit(app.exec_())
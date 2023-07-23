import pyaudio
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        self.fig = Figure(facecolor='black')
        self.ax = self.fig.add_subplot(111, facecolor='black')
        self.ax.set_axis_off()
        self.line, = self.ax.plot([], [], '-', lw=3, color='grey')
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.setCentralWidget(central_widget)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visualizer)
        self.timer.start(1)
        self.dragging = False
        self.offset = QPoint(0, 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def update_visualizer(self):
        data = stream.read(CHUNK)
        samples = np.frombuffer(data, dtype=np.int16)
        self.line.set_data(np.arange(0, CHUNK), samples)
        self.ax.set_xlim(0, CHUNK)
        self.ax.set_ylim(-32768, 32768)
        self.fig.tight_layout(rect=(0, 0, 1, 1))
        self.canvas.draw()

app = QApplication(sys.argv)
app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
palette.setColor(QPalette.Text, QColor(255, 255, 255))
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
app.setPalette(palette)

main_window = MainWindow()
main_window.show()

screen_geometry = app.desktop().screenGeometry()
window_size = screen_geometry.width() * 0.20, screen_geometry.height() * 0.20
main_window.setGeometry(0, screen_geometry.height() - int(window_size[1]), int(window_size[0]), int(window_size[1]))

sys.exit(app.exec_())

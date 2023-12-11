import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class ClipboardWatcher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.previous_clipboard_content = self.clipboard.text()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label = QtWidgets.QLabel("Copied!", self)
        self.label.setStyleSheet("""
            QLabel {
                color : white;
                border: 1px solid white;
                border-radius: 15px;
                padding: 5px;
            }
        """)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setGeometry(20, 10, 80, 30)

        effect = QtWidgets.QGraphicsDropShadowEffect(self.label)
        effect.setBlurRadius(0)
        effect.setColor(QtGui.QColor("black"))
        effect.setOffset(1, 1)
        self.label.setGraphicsEffect(effect)

    def on_clipboard_change(self):
        current_clipboard_content = self.clipboard.text()
        if current_clipboard_content != self.previous_clipboard_content:
            self.previous_clipboard_content = current_clipboard_content
            self.show_bubble()

    def show_bubble(self):
        cursor_pos = QtGui.QCursor.pos()
        self.move(cursor_pos.x(), cursor_pos.y())
        self.setWindowOpacity(0.75)
        self.show()

        # Delay before starting fade out
        QtCore.QTimer.singleShot(500, self.start_fade_animation)

    def start_fade_animation(self):
        # Animation for fading out or whatever
        self.fade_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(1000)  # Duration of fade
        self.fade_animation.setStartValue(0.75)
        self.fade_animation.setEndValue(0)
        self.fade_animation.finished.connect(self.hide_bubble)
        self.fade_animation.start()

    def hide_bubble(self):
        self.hide()

def main():
    app = QtWidgets.QApplication(sys.argv)
    watcher = ClipboardWatcher()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

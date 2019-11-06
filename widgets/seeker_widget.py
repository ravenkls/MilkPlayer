from PyQt5 import QtWidgets, QtCore, QtGui

class SeekerWidget(QtWidgets.QProgressBar):

    timestamp_updated = QtCore.pyqtSignal(str)

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.player.positionChanged.connect(self.update_position)
        self.setTextVisible(False)
        self.setRange(0, 1000)
        self.setFixedHeight(25)
        self.dragging = False

        self.setStyleSheet(
            """
            QProgressBar {
                margin-top: 10px;
                margin-bottom: 10px;
                height: 5px;
                border: 0px solid #555;
                border-radius: 2px;
                background-color: #666;
            }

            QProgressBar::chunk {
                background-color: white;
                border-radius: 2px;
                width: 1px;
            }
            """
        )

    def update_position(self, milliseconds: int):
        if self.player.duration():
            self.setValue((milliseconds/self.player.duration())*self.maximum())
            duration = int(milliseconds / 1000)
            seconds = str(duration % 60)
            minutes = str(duration // 60)
            self.timestamp_updated.emit(minutes.zfill(2) + ':' + seconds.zfill(2))

    def mousePressEvent(self, event):
        self.dragging = True
        value = (event.x() / self.width()) * self.maximum()
        self.player.setPosition((event.x() / self.width()) * self.player.duration())
        self.setValue(value)

    def mouseMoveEvent(self, event):
        if self.dragging:
            value = (event.x() / self.width()) * self.maximum()
            self.player.setPosition((event.x() / self.width()) * self.player.duration())
            self.setValue(value)

    def mouseReleaseEvent(self, event):
        self.dragging = False

    # def paintEvent(self, event):
    #     """Painting the circle onto the seeker"""
    #     super().paintEvent(event)
    #     painter = QtGui.QPainter(self)
    #     painter.setPen(QtGui.QColor("#c9c9c9"))
    #     painter.setBrush(QtGui.QColor("#c9c9c9"))
    #     seeker_x_offset = self.value() / self.maximum() * (self.width() - 10)
    #     painter.drawEllipse(seeker_x_offset, 7, 10, 10)
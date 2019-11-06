import os
import re

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
import numpy as np

from .fft_analyser import FFTAnalyser


class NowPlayingWidget(QtWidgets.QGraphicsView):

    def __init__(self, media_player):
        super().__init__()
        self._media_player = media_player
        self._media_player.currentMediaChanged.connect(self.change_title)

        self.setScene(QtWidgets.QGraphicsScene(self))
        self.init_ui()

    def set_opacity(self, value):
        self._opacity = value
        self.overlay.setOpacity(value)

    def init_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(200)

        self.now_playing_visual = NowPlayingVisual(self._media_player, self)
        self.main_layout.addWidget(self.now_playing_visual)

        self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.black))

        self.video_item = QGraphicsVideoItem()
        self.video_item.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect())
        self.video_item.setAspectRatioMode(QtCore.Qt.KeepAspectRatioByExpanding)
        self._media_player.setVideoOutput(self.video_item)
        self.scene().addItem(self.video_item)

        self.overlay = QtWidgets.QGraphicsRectItem(0, 0, 0, 0, self.video_item)
        self.overlay.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.set_opacity(0.8)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setStyleSheet('border: 0px;')

        self.setLayout(self.main_layout)

    def change_title(self, media):
        data = self._media_player.nowplaying()
        if data:
            self.now_playing_visual.set_title(data)

    def resizeEvent(self, event):
        self.video_item.setSize(QtCore.QSizeF(self.size()))
        rect = QtCore.QRectF(0, 0, self.video_item.size().width(),
                             self.video_item.size().height())
        self.overlay.setRect(rect)


class NowPlayingVisual(QtWidgets.QWidget):

    def __init__(self, media_player, parent):
        super().__init__(parent)
        self.media_player = media_player
        self.fft_analyser = FFTAnalyser(self.media_player)
        self.fft_analyser.calculated_visual.connect(self.set_amplitudes)
        self.fft_analyser.start()
        self.amps = np.array([])
        self.colour = QtGui.QColor(255, 255, 255, 255)
        self.init_ui()
    
    def init_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.song_title = QtWidgets.QLabel()
        self.song_title.setFont(QtGui.QFont('Montserrat', 36))
        self.song_title.setAlignment(QtCore.Qt.AlignCenter)
        self.now_playing = QtWidgets.QLabel('<html><img src="images/play.png" height="14"> NOW PLAYING</html>')
        self.now_playing.setAlignment(QtCore.Qt.AlignCenter)
        self.now_playing.setFont(QtGui.QFont('Karla', 14))

        self.main_layout.addWidget(self.song_title)
        self.main_layout.addWidget(self.now_playing)

        self.setStyleSheet('color: white;')

        self.setLayout(self.main_layout)

    def set_amplitudes(self, amps):
        self.amps = np.array(amps)
        self.repaint()

    def draw_polygon(self):
        poly = QtGui.QPolygonF()
        poly.append(QtCore.QPointF(0, self.height()))
        for n, amp in zip(np.linspace(0, self.width(), self.amps.size), self.amps):
            poly.append(QtCore.QPointF(n, self.height()-amp*self.height()))
        poly.append(QtCore.QPointF(self.width(), self.height()))
        return poly

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        poly = self.draw_polygon()
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.colour)
        painter.drawPolygon(poly)
        painter.drawRect(0, self.height()-5, self.width(), 5)
    
    def set_title(self, data):
        name = data['snippet']['title'].upper()
        #name = re.sub(r'\(.*?\)', '', name).strip().upper()
        if len(name) > 35:
            name = name[:35].strip() + '...'
        self.song_title.setText(name)
        w = self.song_title.fontMetrics().boundingRect(name).width()
        self.parent().setMinimumWidth(w+200)
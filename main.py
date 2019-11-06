import sys
import os
import re
import ctypes

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pydub import AudioSegment
from youtube_dl import YoutubeDL
import numpy as np

from audio import NowPlayingWidget, YTMediaPlayer
from widgets.queue_widget import QueueWidget
from widgets.media_controls import MediaControls


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.main_widget = QtWidgets.QWidget()

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(15)

        with open('token.txt') as token_file:
            key = token_file.read()
        self.media_player = YTMediaPlayer(key)
    
        self.view = NowPlayingWidget(self.media_player)
        self.main_layout.addWidget(self.view)

        self.container = QtWidgets.QVBoxLayout()
        self.container.setContentsMargins(200, 0, 200, 0)
        self.main_layout.addLayout(self.container)

        self.queue_widget = QueueWidget(self.media_player)
        self.container.addWidget(self.queue_widget)

        self.main_layout.addStretch()

        self.controls = MediaControls(self.media_player)
        self.main_layout.addWidget(self.controls)
        
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))
        self.setWindowTitle('Milk Player')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_P:
            self.media_player.query('eminem lucky you')
            self.media_player.query('Lucky Luke FEEL Bass Boosted')
            

        

if __name__ == '__main__':
    app_id = u'me.ravenkls.milkplayer.one'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

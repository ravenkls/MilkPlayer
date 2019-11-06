from PyQt5 import QtWidgets, QtCore, QtGui
import os


class MediaPlayerButtons(QtWidgets.QWidget):
    def __init__(self, media_player):
        super().__init__()
        self._media_player = media_player
        self._media_player.stateChanged.connect(self._change_button_icon)
        self.init_ui()
    
    @property
    def media_player(self):
        return self._media_player

    def init_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.previous_icon = QtGui.QIcon('images/previous.png')
        self.next_icon = QtGui.QIcon('images/next.png')
        self.play_icon = QtGui.QIcon('images/play.png')
        self.pause_icon = QtGui.QIcon('images/pause.png')

        self.previous_song_button = QtWidgets.QPushButton(self.previous_icon, '')
        self.previous_song_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.next_song_button = QtWidgets.QPushButton(self.next_icon, '')
        self.next_song_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.play_pause_button = QtWidgets.QPushButton(self.play_icon, '')
        self.play_pause_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.play_pause_button.clicked.connect(self.toggle_play)

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.previous_song_button)
        self.main_layout.addWidget(self.play_pause_button)
        self.main_layout.addWidget(self.next_song_button)
        self.main_layout.addStretch()

        self.setStyleSheet('QPushButton{ '
                           '    background: transparent;'
                           '}')

        self.setLayout(self.main_layout)
    
    def toggle_play(self):
        if self.media_player.state() == self.media_player.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def _change_button_icon(self, state):
        if state == self.media_player.PlayingState:
            self.play_pause_button.setIcon(self.pause_icon)
        else:
            self.play_pause_button.setIcon(self.play_icon)

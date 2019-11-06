from PyQt5 import QtWidgets, QtGui, QtCore
from widgets.nowplaying_widget import NowPlayingWidget
from widgets.seeker_widget import SeekerWidget
from widgets.volume_widget import VolumeWidget
from widgets.media_player_buttons import MediaPlayerButtons

class MediaControls(QtWidgets.QFrame):

    def __init__(self, media_player):
       super().__init__()
       self._media_player = media_player
       self._media_player.durationChanged.connect(self.change_song)
       self.init_ui()

    @property
    def media_player(self):
        return self._media_player

    def init_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setSpacing(50)

        self.nowplaying_widget = NowPlayingWidget(self.media_player)
        self.main_layout.addWidget(self.nowplaying_widget)

        self.controls_layout = QtWidgets.QVBoxLayout()
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_layout.setSpacing(0)

        self.media_player_buttons = MediaPlayerButtons(self.media_player)
        self.controls_layout.addWidget(self.media_player_buttons)

        self.seeker_widget = SeekerWidget(self.media_player)
        self.controls_layout.addWidget(self.seeker_widget)
        
        self.duration_layout = QtWidgets.QHBoxLayout()
        self.duration_layout.setContentsMargins(0, 0, 0, 0)
        self.duration_layout.setSpacing(0)
        self.duration_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.current_position = QtWidgets.QLabel()
        self.current_position.setAlignment(QtCore.Qt.AlignTop)
        self.current_position.setFont(QtGui.QFont('Karla', 8))
        self.current_position.setStyleSheet('color: white;')
        self.seeker_widget.timestamp_updated.connect(self.current_position.setText)
        self.duration_layout.addWidget(self.current_position)
        self.duration_layout.addStretch()
        self.end_position = QtWidgets.QLabel()
        self.end_position.setFont(QtGui.QFont('Karla', 8))
        self.end_position.setStyleSheet('color: white;')
        self.duration_layout.addWidget(self.end_position)
        self.controls_layout.addLayout(self.duration_layout)

        self.main_layout.addLayout(self.controls_layout)

        self.volume_area = QtWidgets.QHBoxLayout()
        self.volume_area.setContentsMargins(0, 0, 0, 0)
        self.volume_area.setSpacing(0)
        self.volume_icon = QtWidgets.QLabel()
        self.volume_icon.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.volume_icon.setPixmap(QtGui.QPixmap('images/volume.png').scaledToHeight(15))
        self.volume_area.addWidget(self.volume_icon)
        self.volume_widget = VolumeWidget(self.media_player)
        self.volume_area.addWidget(self.volume_widget)
        self.main_layout.addLayout(self.volume_area)

        self.setLayout(self.main_layout)
        self.setStyleSheet('QFrame { background: #242424; }')
        self.setFixedHeight(80)

    def change_song(self):
        duration = int(self.media_player.duration() / 1000)
        seconds = str(duration % 60)
        minutes = str(duration // 60)
        self.end_position.setText(minutes.zfill(2) + ':' + seconds.zfill(2))

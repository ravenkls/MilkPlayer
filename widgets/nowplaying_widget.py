from PyQt5 import QtWidgets, QtCore, QtGui
from widgets.marquee_label import MarqueeLabel
import requests


class Downloader(QtCore.QThread):

    downloaded = QtCore.pyqtSignal(bytes)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        data = requests.get(self.url).content
        self.downloaded.emit(data)


class NowPlayingWidget(QtWidgets.QWidget):

    def __init__(self, media_player):
        super().__init__()
        self._media_player = media_player
        self._media_player.currentMediaChanged.connect(self.change_song)
        self.init_ui()
    
    @property
    def media_player(self):
        return self._media_player

    def init_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(16)
        self.main_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.album_art = QtWidgets.QLabel()
        self.album_art.setStyleSheet('border-radius: 5px')
        self.album_art.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.album_art)

        self.song_info_layout = QtWidgets.QVBoxLayout()
        self.song_info_layout.setContentsMargins(0, 0, 0, 0)
        self.song_info_layout.setSpacing(4)
        self.song_info_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.song_title = MarqueeLabel()
        self.song_title.setFont(QtGui.QFont('Montserrat', 10))
        self.song_title.setColour(QtCore.Qt.white)
        self.song_info_layout.addWidget(self.song_title)
        self.song_artist = QtWidgets.QLabel()
        self.song_artist.setFont(QtGui.QFont('Karla', 8))
        self.song_artist.setStyleSheet('color: white;')
        self.song_info_layout.addWidget(self.song_artist)

        self.main_layout.addLayout(self.song_info_layout)
        self.setLayout(self.main_layout)
        self.setFixedWidth(200)
    
    def change_song(self):
        song = self._media_player.nowplaying()
        if song:
            self.song_title.setText(song['snippet']['title'])
            self.song_artist.setText(song['snippet']['channelTitle'])
            
            thumb_url = song['channel_data']['snippet']['thumbnails']['default']['url']
            self.downloader_thread = Downloader(thumb_url)
            self.downloader_thread.downloaded.connect(self.set_thumbnail)
            self.downloader_thread.start()
    
    def set_thumbnail(self, thumb):
        thumb_pixmap = QtGui.QPixmap()
        thumb_pixmap.loadFromData(thumb)
        self.album_art.setPixmap(thumb_pixmap.scaledToHeight(65))

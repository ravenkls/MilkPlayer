from PyQt5 import QtWidgets, QtGui, QtCore
from .queue_item import QueueItem
from functools import partial
import requests


class Downloader(QtCore.QThread):

    downloaded = QtCore.pyqtSignal(bytes)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        data = requests.get(self.url).content
        self.downloaded.emit(data)


class QueueWidget(QtWidgets.QWidget):

    def __init__(self, media_player):
        super().__init__()
        self._media_player = media_player
        self._media_player.playlist().mediaInserted.connect(self.media_added)
        self.queue_items = {}
        self.downloaders = []
        self.init_ui()
    
    @property
    def media_player(self):
        return self._media_player

    def init_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSpacing(6)
        
        self.up_next_label = QtWidgets.QLabel('UP NEXT')
        self.up_next_label.setFont(QtGui.QFont('Karla', 18))
        self.main_layout.addWidget(self.up_next_label)
        spacer = QtWidgets.QSpacerItem(0, 6)
        self.main_layout.addItem(spacer)

        self.up_next_layout = QtWidgets.QVBoxLayout()
        self.up_next_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.up_next_layout)

        spacer = QtWidgets.QSpacerItem(0, 20)
        self.main_layout.addItem(spacer)

        self.queue_label = QtWidgets.QLabel('SONG QUEUE')
        self.queue_label.setFont(QtGui.QFont('Karla', 18))
        self.main_layout.addWidget(self.queue_label)
        spacer = QtWidgets.QSpacerItem(0, 6)
        self.main_layout.addItem(spacer)

        self.song_queue_layout = QtWidgets.QVBoxLayout()
        self.song_queue_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.song_queue_layout)

        self.setLayout(self.main_layout)

    def media_added(self, start, end):
        for index in range(start, end+1):
            media = self.media_player.playlist().media(start)
            video_id = media.canonicalUrl().fileName().split('.')[0]
            data = self.media_player.load_metadata(video_id)
            self.add_media(data)

    def add_media(self, data):
        downloader = Downloader(data['channel_data']['snippet']['thumbnails']['default']['url'])
        downloader.downloaded.connect(partial(self.add_queue_item, data))
        downloader.start()
        self.downloaders.append(downloader)
    
    def add_queue_item(self, video_data, thumb_data):
        q_item = QueueItem(thumb_data, video_data['snippet']['title'].upper())
        if len(self.queue_items) == 0:
            q_item.set_dark(True)
            self.up_next_layout.addWidget(q_item)
            self.queue_items[video_data['id']['videoId']] = q_item
        else:
            self.song_queue_layout.insertWidget(0, q_item)
            self.queue_items[video_data['id']['videoId']] = q_item

import re
import os
import json

from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5 import QtCore
from pathlib import Path
from youtube_dl import YoutubeDL
import requests

from .youtube_downloader import YouTubeDownloader


class YTMediaPlayer(QMediaPlayer):

    def __init__(self, api_key):
        super().__init__(flags=QMediaPlayer.VideoSurface)
        self._playlist = QMediaPlaylist()
        self._api_key = api_key
        self._download_threads = []
        self._cache_path = Path(os.getenv('appdata')) / 'MilkPlayer'
        self._metadata_file = self._cache_path / 'metadata.json'
        self.setPlaylist(self._playlist)
        self.currentMediaChanged.connect(self._set_nowplaying)
    
    @property
    def api_key(self):
        return self._api_key

    @property
    def cache_path(self):
        return self._cache_path

    @property
    def metadata_file(self):
        return self._metadata_file

    def _set_nowplaying(self, new):
        self._now_playing_media = new

    def query(self, query):
        video_data = self.load_metadata(query)
        if not video_data:
            dl_thread = YouTubeDownloader(query, self)
            dl_thread.downloaded.connect(self.add_video)
            dl_thread.start()
            self._download_threads.append(dl_thread)
        else:
            video_id = video_data['id']['videoId']
            filename = self._cache_path / 'cache' / f'{video_id}.mp4'
            self.add_video((filename, video_data))
        
    def add_video(self, data):
        file_path, video_data = data
        video_id = video_data['id']['videoId']

        if not self.load_metadata(video_id):
            self.save_metadata(video_id, video_data)

        content = QMediaContent(QtCore.QUrl.fromLocalFile(str(file_path)))
        self._playlist.addMedia(content)

    def save_metadata(self, video_id, data):
        if not self._metadata_file.exists():
            cache = {}
        else:
            with open(self._metadata_file) as cache_file:
                cache = json.load(cache_file)
        
        cache[video_id] = data
        with open(self._metadata_file, 'w') as cache_file:
            json.dump(cache, cache_file, indent=2)

    def load_metadata(self, video_id):
        with open(self._metadata_file) as cache_file:
            cache = json.load(cache_file)
            return cache.get(video_id)
    
    def nowplaying(self):
        fn = self._now_playing_media.canonicalUrl().fileName()
        video_id = '.'.join(fn.split('.')[:-1])
        return self.load_metadata(video_id)
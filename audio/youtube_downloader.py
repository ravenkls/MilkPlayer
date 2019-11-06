from PyQt5 import QtCore
from pathlib import Path
from youtube_dl import YoutubeDL
import requests
import time
import json


class YouTubeDownloader(QtCore.QThread):

    downloaded = QtCore.pyqtSignal(tuple)

    def __init__(self, query, media_player):
        super().__init__()
        self.media_player = media_player
        self.api_key = self.media_player.api_key
        self.query = query
        self.media_cache = media_player.cache_path / 'cache'
        self.ydl = YoutubeDL({'format': 'mp4',
                              'outtmpl': str(self.media_cache / '%(id)s.%(ext)s')})

    def enqueue(self, video):
        self._video_urls.append(video)

    def run(self):
        api_params = {'part': 'snippet', 'q': self.query, 'type': 'video', 'videoDuration': 'short', 'key': self.api_key}

        if len(self.query) == 11 and ' ' not in self.query:
            video_data = self.load_metadata(self.query)
            if not video_data:
                response = requests.get('https://www.googleapis.com/youtube/v3/search',
                                        params=api_params)
                video_data = response.json()['items'][0]
        else:
            response = requests.get('https://www.googleapis.com/youtube/v3/search',
                                    params=api_params)
            video_data = response.json()['items'][0]
        
        video_id = video_data['id']['videoId']

        with open(self.media_player.metadata_file) as cache_file:
            cache = json.load(cache_file)
            current_cache = cache.get(video_id)

        if not current_cache:
            response = requests.get('https://www.googleapis.com/youtube/v3/channels',
                                params={'part': 'snippet', 'id': video_data['snippet']['channelId'], 'key': self.api_key})
            channel_data = response.json()['items'][0]
            video_data['channel_data'] = channel_data

        self.ydl.download([video_id])
        filename = str(self.media_cache / f'{video_id}.mp4')

        self.downloaded.emit((filename, video_data))
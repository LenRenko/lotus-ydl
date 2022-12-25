from __future__ import unicode_literals
from threading import Thread, Event
from enum import Enum

import os
import yt_dlp as yt
import json


DOWNLOAD_LIST = [] # urls in waiting list for download
COMPLETED_LIST = [] # urls of already downloaded songs
YOUTUBE_BASE = "https://www.youtube.com/watch?v="
COMPLETED = "Completed"
DOWNLOADING = "Downloading"
output_format = "MP3"
output_dir = os.path.expanduser("~/YTDownloader/YTDownloadOutput/")


class Format(Enum):
    MP3 = "MP3"
    WAV = "WAV"
    M4A = "M4A"
    OGG = "OGG"
    FLAC = "FLAC"
    MP4 = "MP4"
    AVI = "AVI"
    MKV = "MKV"

class URLError(Exception):
    """Raised when bad url is entered for download"""
    pass


def check_config():
    config_file = os.path.exists("config.json")
    data = {
                "output_dir": output_dir, 
                "output_format": output_format, 
                "light_mode": "Light"
            }
    if not config_file:
        with open(os.path.abspath('config.json'), 'w') as f:
            json.dump(data, f, indent=4)

check_config()

# Opening settings file
with open(os.path.abspath('config.json'), 'r') as f:
    settings = json.load(f)

# =================================================================
def set_options(hook, dir: str, format: str, skip_dl: bool ) -> dict:
    """
        Set options for youtube download
    """
    
    opts = {
        "writethumbnail": True,
        "ignoreerrors": True,
        "outtmpl": os.path.join(dir, "%(title)s.%(ext)s"),
        "progress_hooks": [hook],
        "ffmpeg_location": os.path.abspath("ffmpeg/bin"),
        "skip_download": skip_dl,
        "quiet": True,
    }
    
    if format in [Format.MP4.value, Format.AVI.value, Format.MKV.value]:
        opts["format"] = Format[format].value
    elif format in [Format.MP3.value]:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": Format[format].value,
                "preferredquality": "1000",
            },
            {
                'key': 'EmbedThumbnail',
            },
            {
                'key': 'FFmpegMetadata',
            },
        ]
    else:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": Format[format].value,
                "preferredquality": "1000",
            },
            {
                'key': 'FFmpegMetadata',
            },
        ]
    return opts


def is_playlist(url: str):
    if "list" in url:
        return True
    return False

def is_youtube_url(url: str):
    if "youtube.com/watch" in url:
        return True
    else:
        return False

# =================================================================
class AsyncExtractPlaylist(Thread):
    """
        Asyncrhonously get playlist songs informations and return it to UI
    """
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.playlist_titles = []
    
    def run(self):
        with open(os.path.abspath('config.json'), 'r') as f:
            settings = json.load(f)
        yt_opt = set_options(None, settings['output_dir'], settings['output_format'], skip_dl=True, )
        try:
            with yt.YoutubeDL(yt_opt) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.playlist_count = info['playlist_count']
                
                for songs in info['entries']:
                    song_url = YOUTUBE_BASE+str(songs['id'])
                    DOWNLOAD_LIST.append(song_url)
                    self.playlist_titles.append(songs['title'])
                return self.playlist_titles
        except yt.utils.DownloadError:
            raise URLError

class AsyncExtractSongInfo(Thread):
    """
        Get song informations
    """
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.title = ""
    
    def run(self):
        with open(os.path.abspath('config.json'), 'r') as f:
            settings = json.load(f)
        yt_opt = set_options(None, settings['output_dir'], settings['output_format'], skip_dl=True)
        DOWNLOAD_LIST.append(self.url)
        try:
            with yt.YoutubeDL(yt_opt) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.title = info['title']
                
                return self.title
        except yt.utils.DownloadError:
            raise URLError

# ============================== DOWNLOAD ============================ #

class AsyncDownload(Thread):
    """
        Thread for downloading songs
    """
    def __init__(self):
        super().__init__()

        self.status = COMPLETED
        self.download_list = DOWNLOAD_LIST
        self.downloaded = []
        self.current_title = ""
        self.complete_titles = []
        self.count = 0
        
        self._stop_event = Event()
            
    def run(self):
        with open(os.path.abspath('config.json'), 'r') as f:
            settings = json.load(f)
        yt_opt = set_options(self.download_hook, settings['output_dir'], settings['output_format'], skip_dl=False)
        for song in self.download_list:
            self.status = DOWNLOADING
            if self._stop_event.is_set():
                self.status = COMPLETED
                break 
            self.download(song, yt_opt)
            COMPLETED_LIST.append(song)
    
    def download(self, url, yt_opt):
        try:
            with yt.YoutubeDL(yt_opt) as ydl:
                info = ydl.extract_info(url, download=False)
                ydl.download([url])
                self.current_title = info['title']
                self.complete_titles.append(info['title'])
                self.count += 1
        except yt.utils.DownloadError:
            raise URLError


    def download_hook(self, d):
        if d["status"] == "downloading":
            pass
        if d["status"] == "finished":
            self.status = COMPLETED
    
    def stop(self):
        self._stop_event.set()
        

def delete_download_list():
    for i in COMPLETED_LIST:
        DOWNLOAD_LIST.remove(i)
    
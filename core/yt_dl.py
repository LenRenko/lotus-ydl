from threading import Thread

import os
import yt_dlp as yt
import json


DOWNLOAD_LIST = [] # urls in waiting list for download
YOUTUBE_BASE = "https://www.youtube.com/watch?v="
COMPLETED = "Completed"
DOWNLOADING = "Downloading"

class URLError(Exception):
    """Raised when bad url is entered for download"""
    pass

class ThreadWithResult(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)



def check_config():
    config_file = os.path.exists("config.json")
    data = {
                "output_dir": os.path.expanduser("~/YTDownloadOutput/"), 
                "output_format": "MP3", 
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
    yt_opts = ""
    if format == "MP3":
        yt_opts = {
            "ignoreerrors": True,
            "format": "bestaudio/best",
            "ffmpeg_location": os.path.abspath("ffmpeg/bin"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "1000",
                }
            ],
            "outtmpl": os.path.join(dir, "%(title)s.%(ext)s"),
            "progress_hooks": [hook],
            "skip_download": skip_dl,
            "quiet": True,
        }
    elif format == "MP4":
        yt_opts = {
            "ignoreerrors": True,
            "format": "mp4",
            "outtmpl": os.path.join(dir, "%(title)s.%(ext)s"),
            "progress_hooks": [hook],
            "skip_download": skip_dl,
        }

    return yt_opts


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
        yt_opt = set_options(None, settings['output_dir'], settings['output_format'], skip_dl=True)
        DOWNLOAD_LIST.append(self.url)
        try:
            with yt.YoutubeDL(yt_opt) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.title = info['title']
                print(info['title'])
                
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

        self.status = DOWNLOADING
        self.download_list = DOWNLOAD_LIST
        self.downloaded = []
        self.current_title = ""
        self.complete_titles = []
        self.count = 0
            
    def run(self):
        yt_opt = set_options(self.download_hook, settings['output_dir'], settings['output_format'], skip_dl=False)
        for song in self.download_list:
            self.status = DOWNLOADING
            self.download(song, yt_opt)
            self.downloaded.append(song)
    
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
            print(
                "\n"
                + str(
                    round(float(d["downloaded_bytes"]) / float(d["total_bytes"]) * 100, 1)
                )
            )
        if d["status"] == "finished":
            self.status = COMPLETED

def delete_download_list():
    DOWNLOAD_LIST.clear()
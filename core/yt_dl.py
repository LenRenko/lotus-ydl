from __future__ import unicode_literals
from errors import URLError
from threading import Thread

import os
import yt_dlp as yt
import json


class ThreadWithResult(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)

# =================================================================

DOWNLOAD_LIST = [] # urls in waiting list for download
YOUTUBE_BASE = "https://www.youtube.com/watch?v="

# Opening settings file
with open('../config.json', 'r') as f:
    settings = json.load(f)

def set_options(dir: str, format: str, skip_dl: bool) -> dict:
    """
        Set the default options 
    """
    yt_opts = ""
    if format == "MP3":
        yt_opts = {
            "ignoreerrors": True,
            "format": "bestaudio/best",
            "ffmpeg_location": "../ffmpeg/bin",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "1000",
                }
            ],
            "outtmpl": os.path.join(dir, "%(title)s.%(ext)s"),
            "progress_hooks": [download_hook],
            "skip_download": skip_dl,
        }
    elif format == "MP4":
        yt_opts = {
            "ignoreerrors": True,
            "format": "mp4",
            "outtmpl": os.path.join(dir, "%(title)s.%(ext)s"),
            "progress_hooks": [download_hook],
            "skip_download": skip_dl,
        }

    return yt_opts


def is_playlist(url: str):
    if "list" in url:
        return True
    return False


# =================================================================
def get_playlist_titles(url: str):
    yt_opt = set_options(settings['output_dir'], settings['output_format'], skip_dl=True)
    playlist_ttitles = []
    try:
        with yt.YoutubeDL(yt_opt) as ydl:
            info = ydl.extract_info(url, download=False)
            print(info.keys())
            print(info['playlist_count'])
            
            for songs in info['entries']:
                song_url = YOUTUBE_BASE+str(songs['id'])
                DOWNLOAD_LIST.append(song_url)
                playlist_ttitles.append(songs['title'])
            
            return playlist_ttitles
    except yt.utils.DownloadError:
        raise URLError

def get_yt_info(url: str):
    yt_opt = set_options(settings['output_dir'], settings['output_format'], skip_dl=True)
    DOWNLOAD_LIST.append(url)
    try:
        with yt.YoutubeDL(yt_opt) as ydl:
            info = ydl.extract_info(url, download=False)
            #print(info.keys())
            print(info['title'])
    except yt.utils.DownloadError:
        raise URLError
    
    return info['title']

# ============================== DOWNLOAD ============================ #

# Downloading hook to retrieve progress data
def download_hook(d):
    print("ICI")
    if d["status"] == "downloading":
        print(
            "\n"
            + str(
                round(float(d["downloaded_bytes"]) / float(d["total_bytes"]) * 100, 1)
            )
        )
        print(d["eta"])


def start_download(url: str):
    download_thread = Thread(target=download, args=[url])
    download_thread.start()

def download(url: str):
    yt_opt = set_options(settings['output_dir'], settings['output_format'], skip_dl=False)

    try:
        with yt.YoutubeDL(yt_opt) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])
            print(info.keys())
            print(info['title'])
    except yt.utils.DownloadError:
        raise URLError

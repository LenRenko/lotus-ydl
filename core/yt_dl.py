from __future__ import unicode_literals
from errors import URLError
from threading import Thread

import os
import yt_dlp as yt
import json

# =================================================================
with open('../config.json', 'r') as f:
    settings = json.load(f)

def set_options(dir: str, format: str) -> dict:
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
        }
    elif format == "MP4":
        yt_opts = {
            "ignoreerrors": True,
            "format": "mp4",
            "outtmpl": os.path.join(dir, "%(title)s.%(ext)s"),
            "progress_hooks": [download_hook],
        }

    return yt_opts

# =================================================================

def get_yt_info(url: str):
    yt_opt = set_options(settings['output_dir'], settings['output_format'])
    try:
        with yt.YoutubeDL(yt_opt) as ydl:
            info = ydl.extract_info(url, download=False)
            #print(info.keys())
            print(info['title'])
    except yt.utils.DownloadError:
        raise URLError
    
    return info['title']

# Downloading hook to retrieve progress data
def download_hook(d):
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
    yt_opt = set_options("B:\Dev\Projetcs\lotus-ydl\output", 'MP4')

    try:
        with yt.YoutubeDL(yt_opt) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])
            print(info.keys())
            print(info['title'])
    except yt.utils.DownloadError:
        raise URLError

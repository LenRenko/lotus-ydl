from __future__ import unicode_literals

import os

import yt_dlp as yt

from errors import URLError


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


# setting the options
# using FFMpeg to postprocess youtube data
def set_options(dir: str) -> dict:
    yt_opts = {
        "format": "bestaudio/best",
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

    return yt_opts


def downloader(url: str):
    yt_opt = set_options("~/Documents/Dev/projects/lotus-ydl/")

    try:
        with yt.YoutubeDL(yt_opt) as ydl:
            info = ydl.extract_info(url, download=False)
            # ydl.download([url])
            print(info.keys())
    except yt.utils.DownloadError:
        raise URLError

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./static/img/lunar_lotus_logo.ico">
    <img src="./static/img/lunar_lotus_logo.ico" width="100" heigth="100">
  </picture>
  
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./static/img/logo_ydl.png">
    <img src="./static/img/logo_ydl.png">
  </picture>
</p>


<div align="center">
  <h3> Yet another simple Youtube Downloader</h3>
</div>

---

This is a simple Youtube Downloader GUI application build in python with tkinter and TomSchimansky [customtkinter](https://github.com/TomSchimansky/CustomTkinter). I built it because I didn't found what I wanted, so made it as simple as possible. _Special thanks to my GF for testing it and giving improvements ideas_ 

<div align="center">
  <p align="left">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./static/doc_images/yt_dl_dark.PNG">
      <img src="./static/doc_images/yt_dl_dark.PNG" width="400" height="400">
    </picture>
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./static/doc_images/yt_dl_light.PNG">
      <img src="./static/doc_images/yt_dl_light.PNG" width="400" height="400">
    </picture>
  </p>
  
  <p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./static/doc_images/yt_dl_st.PNG">
      <img src="./static/doc_images/yt_dl_st.PNG">
    </picture>
  </p>
</div>

## Get the installer
### Simply go to the website [LL Youtube Downloader](https://yt-dl.lunar-lotus.com/) and click on "Download"

---
#### Where to get the .exe file ? 
- You can get the exe file [here](https://github.com/LenRenko/lotus-ydl/releases) or click on release on the right
- Extract the archive (with [winrar](https://www.win-rar.com/start.html?L=10) or [7zip](https://www.7-zip.org/download.html)) where you want on your computer
- Go to the folder LLYTDownloader and look for the `LLYTDownloader.exe`

#### How to use it ?
- Go to youtube and copy the url of your favorite song or video
- Launch with `LLYTDownloader.exe`
- Follow the instructions on your screen :-> Paste your url on the entry, press ENTER or click add to add your url to download list
- Do step 1 to 3 again if you want. 
- When you have all your desired urls to download :-> Click DOWNLOAD button and wait for it to download. 

###### Open settings
- To open settings window, click on the gear button on the bottom right and chose desired options

---
#### How to use with Python ?
- Download ffmpeg binaries from [Btbn](https://github.com/BtbN/FFmpeg-Builds/releases) for your OS
- Extract the folder and rename it `ffmpeg`
- Clone this repo to your computer or download [source code](https://github.com/LenRenko/lotus-ydl/archive/refs/tags/V1.0.0.zip) and extract it where you want
- Install requirements with `pip install -r requirements.txt`
- Put the `ffmpeg` folder in the root of this project
- Launch `python main.py`

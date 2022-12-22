import customtkinter as ctk
import tkinter as tk
import os
import json
from . import yt_dl

from tkinter import filedialog
from pathlib import Path
from PIL import Image

class OutputTopLevel(ctk.CTkToplevel):
    """
        Create a TopLevel window for settings
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Settings")
        self.geometry("300x250+820+300")
        self.resizable(0,0)
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )
        self.iconphoto(False, tk.PhotoImage(os.path.abspath('static/img/lunar_lotus_logo.ico')))
        
        # ============ Main frame =========== #
        self.setting_frame = ctk.CTkFrame(
            master=self,
            border_width=1,
            corner_radius=0)
        self.setting_frame.grid(row=0, column=0, pady=(1, 10))
        
        # ============ Output ============ #
        
        # info label
        output_dis_label = ctk.CTkLabel(
            master=self.setting_frame,
            text="Output Folder",
            font=('Helvetica', 14, 'bold'))
        output_dis_label.grid(row=0, padx=20, pady=5, sticky="we")
        
        # directory display label
        self.output_dis_label = ctk.CTkLabel(
            master=self.setting_frame,
            text=self.master.output_dir)
        self.output_dis_label.grid(row=1, padx=20, pady=5, sticky="we")
        
         # Choose button
        self.output_button = ctk.CTkButton(
            master=self.setting_frame,
            text="Select Folder",
            cursor="hand2",
            border_width=0,
            corner_radius=0,
            command=self.set_output_dir)
        self.output_button.grid(row=2, sticky="we", padx=80, pady=5)

        # ============ Format ============ #
        
        # info label
        format_dis_label = ctk.CTkLabel(
            master=self.setting_frame,
            text="Format",
            font=('Helvetica', 14, 'bold'))
        format_dis_label.grid(row=4, column=0, padx=20, pady=5, sticky="we")

        self.format_menu = ctk.CTkOptionMenu(
            master=self.setting_frame, 
            values=["MP3", "MP4"],
            corner_radius=0,
            width=150,
            command=self.set_format_choice)
        self.format_menu.grid(row=5, column=0, padx=20, pady=(10,10), sticky="")
        
        # ============ DARK MODE ============ #
        self.dark_mode = ctk.CTkSwitch(
            master=self.setting_frame,
            text="Dark Mode",
            onvalue="Dark",
            offvalue="Light",
            corner_radius=2)
        self.dark_mode.configure(command=self.switch_event)
        self.dark_mode.grid(row=6, column=0, padx=20, pady=(10,10))
        
    
    def switch_event(self):
        """
            Define apparence mode dark or light and save it on config file
        """
        if self.dark_mode.get() == "Dark":
            ctk.set_appearance_mode("Dark")
            self.master.light_mode = "Dark"
            self.dark_mode.select()
        else:
            ctk.set_appearance_mode("Light")
            self.master.light_mode = "Light"
            self.dark_mode.deselect()
            
        self.master.set_setting("light_mode", self.dark_mode.get())
       
    def set_output_dir(self):
        output_dir = filedialog.askdirectory(initialdir = "/",title = "Open file")
        if output_dir :
            self.master.output_dir = output_dir
            self.output_dis_label.configure(text=self.master.output_dir)
            self.master.set_setting("output_dir", output_dir)
    
    def set_format_choice(self, choice):
        self.master.output_format = choice
        self.master.set_setting("output_format", choice)
        
    def on_closing(self):
        self.withdraw()
        self.master.grab_set()

# =========== Confirm Top Level ============= #
class ConfirmTopLevel(ctk.CTkToplevel):
    
    playlist_url = ""
    song_url = ""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Confirm")
        self.geometry("340x250+820+300")
        self.resizable(0,0)
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )
        self.iconphoto(False, tk.PhotoImage(os.path.abspath("static/img/lunar_lotus_logo.png")))
    
        # confirm text
        self.txt_label = ctk.CTkLabel(master=self, text="This file is part of a playlist. \n Do you want to add all the playlist to download ? \n \n This can take a moment depending on playlist length", font=('Helvetica', 12, 'bold'))
        self.txt_label.pack(pady=(20, 0))
        
        self.txt_warning = ctk.CTkLabel(master=self, font=('Helvetica', 13, 'bold'), text="Make sure the playlist is not private ! \n Change your private playlist to 'not listed' or 'public'")
        self.txt_warning.configure(text_color="#e36414")
        self.txt_warning.pack()
        
        # buttons
        self.yes_button = ctk.CTkButton(
            master=self,
            text="Yes",
            cursor="hand2",
            border_width=0,
            corner_radius=0,
            font=('Helvetica', 13, 'bold'),
            width=50,
            command=self.yes_command)
        self.yes_button.pack(side=tk.LEFT, padx=(50,0))
        
        self.no_button = ctk.CTkButton(
            master=self,
            text="No",
            cursor="hand2",
            border_width=0,
            corner_radius=0,
            font=('Helvetica', 13, 'bold'),
            width=50,
            command=self.on_closing)
        self.no_button.pack(side=tk.RIGHT, padx=(0, 50))
        
        self.only_song = ctk.CTkButton(
            master=self,
            text="This song only",
            cursor="hand2",
            border_width=0,
            corner_radius=0,
            font=('Helvetica', 13, 'bold'),
            command=self.song_only)
        self.only_song.pack(side=tk.RIGHT, padx=(10, 10))
        
    def yes_command(self):
        self.master.url_frame.url_entry.delete(0, tk.END)
        playlist_thread = yt_dl.AsyncExtractPlaylist(self.playlist_url)
        playlist_thread.start()
        
        self.master.dl_frame.current_dl.yt_title.configure(text="Fetching songs from playlist, please wait ...")
        self.master.dl_frame.current_dl.yt_title.configure(text_color="#708d81")
        self.monitor(playlist_thread, 'PL')
        self.master.dl_frame.current_dl.progress_bar.start()
        self.on_closing()
            
    def song_only(self):
        self.master.url_frame.url_entry.delete(0, tk.END)
        self.song_url = self.playlist_url.split('&')[0]
        song_thread = yt_dl.AsyncExtractSongInfo(self.song_url)
        song_thread.start()
        
        self.monitor(song_thread, 'S')
        self.on_closing()
    
    def monitor(self, thread, type):
        if thread.is_alive():
            self.after(100, lambda: self.monitor(thread, type))
        else:
            if type == "PL":
                self.master.dl_frame.update_list_with_playlist(thread.playlist_titles)
                self.master.dl_frame.current_dl.progress_bar.stop()
                self.master.dl_frame.current_dl.progress_bar.configure(mode="determinate")
                self.master.dl_frame.current_dl.progress_bar.set(0)
            elif type == "S":
                self.master.dl_frame.update_list(self.song_url, thread.title)
            
            self.master.dl_frame.current_dl.yt_title.configure(text="")
            self.master.dl_frame.current_dl.progress_count.configure(text=f"0 / {len(self.master.dl_frame.download_list)}")
                
    def on_closing(self):
        self.withdraw()
        self.master.grab_set()
        
        
# ================================================================= #

class LogoFrame(ctk.CTkFrame):
    """
        Top frame for logo title display
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.logo_image = ctk.CTkImage(Image.open(os.path.abspath("static/img/logo_ydl.png")), 
            size=(300,120)
        )
        
        self.image_label = ctk.CTkLabel(master=self, image=self.logo_image, text="")
        self.image_label.grid(row=0, column=0, sticky="nswe", ipadx=150)
        
class URLEntryFrame(ctk.CTkFrame):
    """
    Define the top frame where the URL entry is with one button to add url to list of URLs
    """
    
    url = ""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.url_entry = ctk.CTkEntry(
            master=self, 
            placeholder_text="Paste url here, press ENTER or click Add and click Download to download all list", 
            width=500, 
            corner_radius=0)
        self.url_entry.pack(padx=(50,50), pady=5)
        
        self.add = ctk.CTkButton(
            master=self,
            text="Add",
            cursor="hand2",
            border_width=0,
            corner_radius=0,
            font=('Helvetica', 13, 'bold'))
        self.add.pack(padx=10, pady=(2,10))
        
        # Bind ENTER key to the url entry to automatically do something when ENTER is pressed
        self.url_entry.bind("<Return>", self.get_url_info)
        self.add.configure(command=self.get_url_info)
        
    def get_url_info(self, event=0):
        self.url = self.url_entry.get()
        
        if self.url:
            if yt_dl.is_youtube_url(self.url):
                self.master.dl_frame.current_dl.yt_title.configure(text="")
                if yt_dl.is_playlist(self.url):
                    self.master.confirm_window.playlist_url = self.url
                    self.master.confirm_window.deiconify()
                    self.master.confirm_window.grab_set()
                else:
                    if self.url not in self.master.dl_frame.download_urls:
                        song_thread = yt_dl.AsyncExtractSongInfo(self.url)
                        song_thread.start()
                        
                        self.monitor(song_thread)

            else:
                self.master.dl_frame.current_dl.yt_title.configure(text="Invalid youtube URL")
    
    def monitor(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.monitor(thread))
        else:
            self.master.dl_frame.update_list(self.url, thread.title)
            self.url_entry.delete(0, 'end')
            self.master.dl_frame.current_dl.progress_count.configure(text=f"0 / {len(self.master.dl_frame.download_list)}")
    
class DownloadItemFrame(ctk.CTkFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_width=1)
        
        # Title label
        self.yt_title = ctk.CTkLabel(
            master=self,
            text=f"",
            font=('Helvetica', 14, 'bold'))
        self.yt_title.grid(row=0, column=0, sticky="w", padx=(10,0), pady=(2, 0))
        
        # progress bar
        self.progress_bar = ctk.CTkProgressBar(master=self, height=10, width=460, corner_radius=0, mode="indeterminate")
        self.progress_bar.grid(row=1, column=0, padx=(10,0))
        self.progress_bar.set(0)
        
        # percent label
        self.progress_count = ctk.CTkLabel(master=self, text=f"")
        self.progress_count.grid(row=1, column=1, sticky="we", padx=(20,20), pady=(2,2))

class ListItem(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_width=1, border_color="gray20")
        self.configure(corner_radius=0)
        self.configure(fg_color="gray70")
        
        self.number_box = ctk.CTkLabel(master=self, text="", font=('Helvetica', 13, "bold"), width=10)
        self.number_box.grid(row=0, column=0, sticky="NW")
        
        self.title_box = ctk.CTkLabel(master=self, text="", font=('Helvetica', 13, 'bold'), width=450)
        self.title_box.grid(sticky="W", row=0, column=1)
        
        self.state = ctk.CTkLabel(master=self, text="", font=('Helvetica', 11, 'bold'), width=80)
        self.state.grid(sticky="E", row=0, column=2)

class DownloadListFrame(ctk.CTkFrame):
    
    download_list = []
    download_urls = []
    downloaded_list = []
    download_items = []
    completed = 0
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ============ Current download
        self.current_dl = DownloadItemFrame(master=self, corner_radius=0)
        self.current_dl.grid(row=0, column=0, sticky="we", padx=10, pady=5)
        
        # ============ Waiting list
        self.title_label = ctk.CTkLabel(master=self, text="Download List", font=('Helvetica', 14, 'bold'))
        self.title_label.grid(row=1, column=0)
        
        # Download list display
        
        self.download_list_canvas = ctk.CTkCanvas(master=self, height=160)
        self.download_list_canvas.grid(row=2, column=0, sticky="nsew", padx=(5, 5), )
        
        self.scrollbar = ctk.CTkScrollbar(
            master=self,
            orientation=tk.VERTICAL,
            command=self.download_list_canvas.yview,
            corner_radius=0)
        self.scrollbar.grid(row=2, column=1, sticky=tk.E, padx=(0, 5))
        
        self.download_list_canvas.configure(yscrollcommand=self.scrollbar.set, border=False, borderwidth=0)
        self.download_list_canvas.bind("<Configure>", lambda e: self.download_list_canvas.configure(scrollregion=self.download_list_canvas.bbox("all")))
        
        self.download_list_frame = ctk.CTkFrame(master=self.download_list_canvas, border_width=0, corner_radius=0, width=600)
        self.download_list_canvas.create_window((2,2), window=self.download_list_frame, anchor="n")
        
        
        self.download_btn = ctk.CTkButton(
            master=self,
            text="Download",
            cursor="hand2",
            border_width=0,
            corner_radius=0,
            width=150,
            font=('Helvetica', 16, 'bold'),
            command=self.start_download,)
        self.download_btn.grid(row=3, columnspan=2, pady=(5,5))
        
        self.columnconfigure(1, weight=1)

    def update_list_with_playlist(self, playlist: list):
        if playlist:
            for title in playlist:
                if title not in self.download_list:
                    self.download_list.append(title)
                    idx = self.download_list.index(title)
                    title = self.check_title_lenght(title)
                    
                    # Write in the dl_list the song
                    title_item = ListItem(master=self.download_list_frame)
                    title_item.number_box.configure(text=str(idx+1))
                    title_item.title_box.configure(text=title)
                    title_item.pack(padx=4, pady=2, expand=True)
                    self.download_items.append(title_item)
                    

    def update_list(self, url: str, title: str):
        if url not in self.download_urls:
            self.download_urls.append(url)
            
            if title not in self.download_list:
                self.download_list.append(title)
                idx = self.download_list.index(title)
                title = self.check_title_lenght(title)
                
                title_item = ListItem(master=self.download_list_frame)
                title_item.number_box.configure(text=str(idx+1))
                title_item.title_box.configure(text=title)
                title_item.pack(padx=4, pady=2, fill=tk.X, expand=True, anchor=tk.W)
                self.download_items.append(title_item)
                        
        self.master.url_frame.url_entry.delete(0, 'end')
    
    def start_download(self):
        self.download_btn.configure(state="disabled")
        self.current_dl.progress_bar.configure(mode="determinate")
        self.current_dl.yt_title.configure(text="Starting download...")
        
        download = yt_dl.AsyncDownload()
        download.start()
        
        self.monitor_download(download)
    
    def monitor_download(self, thread):
        if thread.is_alive():
            self.update_current_dl(thread.current_title, thread.count)
            self.after(10, lambda: self.monitor_download(thread))
        else:
            self.download_btn.configure(state="normal")
            self.update_ended()

    
    def update_current_dl(self, current_title:str, complete_items: int):
        if current_title:
            current_text = self.current_dl.yt_title
            current_progress_text = self.current_dl.progress_count
            total_items = len(self.download_list)
            
            # Update text and count
            current_text.configure(text=f"{self.check_title_lenght(current_title)}")
            current_progress_text.configure(text=f"{complete_items} / {total_items}")
            
            # Update progress bar
            value = (complete_items/total_items)
            self.completed += complete_items
            self.current_dl.progress_bar.set(value)
    
    def update_ended(self):
        for items in self.download_items:
            items.state.configure(text="DOWNLOADED")
        self.current_dl.yt_title.configure(text="Download completed !")
        self.current_dl.progress_bar.set(0)
        self.download_list.clear()
        yt_dl.delete_download_list()
    
    def check_title_lenght(self, title: str):
        if len(title) > 50:
            return title[:50] + "..."
        return title
        

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 
        self.org_label = ctk.CTkLabel(master=self, text="Powered by Lunar Lotus")
        self.org_label.pack(side=tk.LEFT, padx=10)
        
        # settings button
        image = Image.open(os.path.abspath("static/img/settings_icon.png"))
        setting_icon = ctk.CTkImage(image)
        
        self.setting_button = ctk.CTkButton(
            master=self, 
            text="", 
            cursor="hand2", 
            border_width=0, 
            corner_radius=0,
            image=setting_icon,
            compound=tk.LEFT,
            width=20
        )
        self.setting_button.configure(command=self.master.on_open_settings)
        self.setting_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(1,4))

class App(ctk.CTk):
    """
    Main application interface
    """
    WIDTH = 600
    HEIGHT = 570
    
    output_format = "mp3"
    output_dir = str(Path.home())+"\download\\"
    light_mode = "Light"
    
    def __init__(self):
        super().__init__()
        self.init_settings()
        
        # ============ INIT APP =========== #
        self.title("Youtube Downloader by Lunar Lotus")
        self.resizable(0,0)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}+700+200")
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )
        self.iconphoto(False, tk.PhotoImage(os.path.abspath("static/img/lunar_lotus_logo.png")))
                
        # init options windows
        self.output_window = OutputTopLevel(self)
        self.output_window.withdraw()
        
        # init confirm top level
        self.confirm_window = ConfirmTopLevel(self)
        self.confirm_window.withdraw()
        
        # ============ LOGO FRAME ========== #
        self.logo_frame = LogoFrame(master=self)
        self.logo_frame.grid(row=0, column=0, sticky="we")
        
        # ============ TOP FRAME =========== #
        self.url_frame = URLEntryFrame(master=self, corner_radius=0)
        self.url_frame.grid(row=1, column=0, sticky="we")
        
        # ============ URLs display FRAME =========== #
        self.dl_frame = DownloadListFrame(master=self, corner_radius=0)
        self.dl_frame.grid(row=2, column=0, sticky="we")
        
        # ============ BOTTOM FRAME =========== #
        self.bot_frame = SettingsFrame(master=self, corner_radius=0)
        self.bot_frame.grid(row=3, column=0, pady=2, sticky="we")

    
    def on_open_settings(self):
        if self.output_window.state() == "withdrawn":
            self.output_window.deiconify()
            self.output_window.grab_set()
            if self.light_mode == "Light":
                self.output_window.dark_mode.deselect()
            else:
                self.output_window.dark_mode.select()

    def init_settings(self):
        with open(os.path.abspath('config.json')) as f:
            data = json.load(f)
            
            self.output_format = data["output_format"]

            if data["light_mode"]:
                ctk.set_appearance_mode(data["light_mode"])
                self.light_mode = data["light_mode"]
            if data['output_dir']:
                self.output_dir = data["output_dir"]
            theme_path = os.path.abspath("static/theme.json")
            ctk.set_default_color_theme(theme_path)
    
    def set_setting(self, setting: str, value: str):
        with open(os.path.abspath('config.json')) as f:
            data = json.load(f)
        data[setting] = value
        with open(os.path.abspath('config.json'), "w") as f:
            json.dump(data, f)
    
    def on_closing(self, event=0):
        self.destroy()
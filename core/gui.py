from time import sleep
import customtkinter as ctk
import tkinter as tk
import os
import json
import yt_dl

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
        self.iconbitmap("B:\Dev\Projetcs\lotus-ydl\static\img\lunar_lotus_logo.ico")
        
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Confirm")
        self.geometry("260x140+820+300")
        self.resizable(0,0)
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )
        self.iconbitmap("B:\Dev\Projetcs\lotus-ydl\static\img\lunar_lotus_logo.ico")
    
        # confirm text
        self.txt_label = ctk.CTkLabel(master=self, text="This file is part of a playlist. \n Do you want to download all the playlist ?", font=('Helvetica', 12, 'bold'))
        self.txt_label.pack(pady=(20, 0))
        
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
            width=50)
        self.no_button.pack(side=tk.RIGHT, padx=(0, 50))
        
    
    def yes_command(self):
        self.master.url_frame.url_entry.delete(0, tk.END)
        self.yes_button.configure(state="disabled")
        self.no_button.configure(state="disabled")
        self.txt_label.configure(text="Getting playlist songs...")
        sleep(1)
        self.get_playlist_titles()
    
    def no_command(self):
        ""
     
    def on_closing(self):
        self.withdraw()
        self.master.grab_set()
    
    def get_playlist_titles(self):
        playlist_songs = yt_dl.get_playlist_titles(self.playlist_url)
        self.on_closing()
        self.master.dl_frame.update_list_with_playlist(playlist_songs)
        
# ================================================================= #

class LogoFrame(ctk.CTkFrame):
    """
        Top frame for logo title display
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.logo_image = ctk.CTkImage(Image.open("..\static\img\logo_ydl.png"), 
            size=(300,120)
        )
        
        self.image_label = ctk.CTkLabel(master=self, image=self.logo_image, text="")
        self.image_label.grid(row=0, column=0, sticky="nswe", ipadx=150)
        
class URLEntryFrame(ctk.CTkFrame):
    """
    Define the top frame where the URL entry is with one button to add url to list of URLs
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.url_entry = ctk.CTkEntry(
            master=self, 
            placeholder_text="Paste your url here and press ENTER to add to download list", 
            width=500, 
            corner_radius=0)
        self.url_entry.grid(row=0, columnspan=2, sticky="we", padx=(50,50), pady=5)
        
        self.dl_button = ctk.CTkButton(
            master=self,
            text="Download",
            cursor="hand2",
            border_width=0,
            corner_radius=0,
            font=('Helvetica', 13, 'bold'))
        self.dl_button.grid(row=1, column=1, sticky="w", padx=10, pady=(2,10))
        
        # Bind ENTER key to the url entry to automatically do something when ENTER is pressed
        self.url_entry.bind("<Return>", self.get_url_info)
        #self.dl_button.configure(command=self.get_url_info)
        
    def get_url_info(self, event=0):
        url = self.url_entry.get()
        if url:
            if yt_dl.is_playlist(url):
                print("This is a playlist")
                self.master.confirm_window.playlist_url = url
                self.master.confirm_window.deiconify()
                self.master.confirm_window.grab_set()
                
            else:
                if url not in self.master.dl_frame.download_urls:
                    url_title = yt_dl.get_yt_info(url)
                    self.master.dl_frame.update_list(url, url_title)
                    self.url_entry.delete(0, 'end')
            
class DownloadItemFrame(ctk.CTkFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_width=1)
        
        # Title label
        self.yt_title = ctk.CTkLabel(
            master=self,
            text=f"",
            font=('Helvetica', 14, 'bold')) # ! Insert music title here
        self.yt_title.grid(row=0, column=0, sticky="w", padx=(10,0), pady=(2, 0))
        
        # progress bar
        self.progress_bar = ctk.CTkProgressBar(master=self, height=10, width=420, corner_radius=0)
        self.progress_bar.grid(row=1, column=0, padx=(10,0))
        self.progress_bar.set(0)
        
        # percent label
        self.progress_percent = ctk.CTkLabel(master=self, text=f"") # ! Insert progress percentage here
        self.progress_percent.grid(row=1, column=1, sticky="we", padx=(20,20), pady=(2,2))

class DownloadListFrame(ctk.CTkFrame):
    
    download_list = []
    download_urls = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ============ Current download
        self.current_dl = DownloadItemFrame(master=self, corner_radius=0)
        self.current_dl.pack(fill=tk.X, padx=10, pady=5)
        
        # ============ Waiting list
        self.title_label = ctk.CTkLabel(master=self, text="Download List", font=('Helvetica', 14, 'bold'))
        self.title_label.pack()
        
        self.dl_list = ctk.CTkTextbox(
            master=self,
            corner_radius=0,
            state="disabled",
            fg_color="gray80",
            height=200)
        self.dl_list.pack(fill=tk.BOTH, padx=10, pady=5)

    def update_list_with_playlist(self, playlist: list):
        if playlist:
            for title in playlist:
                if title not in self.download_list:
                    self.download_list.append(title)
                    idx = self.download_list.index(title)
                    title_text = str(idx+1)+ " - " + title +"\n"
                    
                    # Write in the dl_list the song
                    self.dl_list.configure(state="normal")
                    self.dl_list.insert(f"{idx+1}.0", title_text)
                    self.dl_list.update()
                    self.dl_list.configure(state="disabled")

    def update_list(self, url: str, title: str):
        if url not in self.download_urls:
            self.download_urls.append(url)
        if title not in self.download_list:
            self.download_list.append(title)
            idx = self.download_list.index(title)
            title_text = str(idx+1)+ " - " + title +"\n"
            
            # Write in the dl_list the song
            self.dl_list.configure(state="normal")
            self.dl_list.insert(f"{idx+1}.0", title_text)
            self.dl_list.update()
            self.dl_list.configure(state="disabled")
        
        self.master.url_frame.url_entry.delete(0, 'end')

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 
        self.org_label = ctk.CTkLabel(master=self, text="Powered by Lunar Lotus")
        self.org_label.pack(side=tk.LEFT, padx=10)
        
        # settings button
        image = Image.open("../static/img/settings_icon.png")
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
        self.setting_button.pack(side=tk.RIGHT, padx=(0, 10))

class App(ctk.CTk):
    """
    Main application interface
    """
    WIDTH = 600
    HEIGHT = 540
    
    download_list = []
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
        self.iconbitmap("B:\Dev\Projetcs\lotus-ydl\static\img\lunar_lotus_logo.ico")
                
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
    
    def on_closing(self, event=0):
        self.destroy()

    def init_settings(self):
        with open('../config.json') as f:
            data = json.load(f)
            
            self.output_format = data["output_format"]

            if data["light_mode"]:
                ctk.set_appearance_mode(data["light_mode"])
                self.light_mode = data["light_mode"]
            if data['output_dir']:
                self.output_dir = data["output_dir"]
            ctk.set_default_color_theme(os.path.abspath("../static/theme.json"))
    
    def set_setting(self, setting: str, value: str):
        with open('../config.json') as f:
            data = json.load(f)
        data[setting] = value
        with open('../config.json', "w") as f:
            json.dump(data, f)
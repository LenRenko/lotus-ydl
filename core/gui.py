import customtkinter as ctk
import tkinter as tk

from tkinter import filedialog
from pathlib import Path
from PIL import Image

# ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
# ctk.set_default_color_theme(os.path.abspath("../static/theme.json"))

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
            values=[".mp3", ".mp4"],
            corner_radius=0,
            width=150,
            command=self.set_format_choice)
        self.format_menu.grid(row=5, column=0, padx=20, pady=(10,10), sticky="")
        
        # ============ DARK MODE ============ #
        self.dark_mode = ctk.CTkSwitch(
            master=self.setting_frame,
            text="Dark Mode",
            onvalue="dark",
            offvalue="light",
            corner_radius=2)
        self.dark_mode.configure(command=self.switch_event)
        self.dark_mode.select()
        self.dark_mode.grid(row=6, column=0, padx=20, pady=(10,10))
        
    
    def switch_event(self):
        """
            Define apparence mode dark or light
        """
        print(f"switch mode : {self.dark_mode.get()}")
        if self.dark_mode.get() == "dark":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
       
    def set_output_dir(self):
        output_dir = filedialog.askdirectory(initialdir = "/",title = "Open file")
        if output_dir :
            self.master.output_dir = output_dir
            self.output_dis_label.configure(text=self.master.output_dir)
    
    def set_format_choice(self, choice):
        print(f"Format Choose : {choice}")
        self.master.output_format = choice
        
    def on_closing(self):
        self.withdraw()
        self.master.grab_set()

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
            placeholder_text="Paste your url here", 
            width=500, 
            corner_radius=0)
        self.url_entry.grid(row=0, columnspan=2, sticky="we", padx=(50,50), pady=5)
        
        # Add button
        self.add_button = ctk.CTkButton(
            master=self, 
            text="Add", 
            cursor="hand2", 
            border_width=0, 
            corner_radius=0,
            font=('Helvetica', 13, 'bold'))
        self.add_button.grid(row=1, column=0, sticky="e", padx=10, pady=(2,10))
        
        self.dl_button = ctk.CTkButton(
            master=self,
            text="Download",
            cursor="hand2",
            border_width=0,
            corner_radius=0,
            font=('Helvetica', 13, 'bold'))
        self.dl_button.grid(row=1, column=1, sticky="w", padx=10, pady=(2,10))
        
    def get_entry_value(self):
        """
        Get the value of the URL entry
        """
        return ""


class DownloadItemFrame(ctk.CTkFrame):
    """
    Define the download list with all current downloading files history.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_width=1)
                
        # Title label
        self.yt_title = ctk.CTkLabel(master=self, text=f"[Insert file title here]")
        self.yt_title.grid(row=0, column=0, sticky="w", padx=(10,0), pady=(2, 0))
        
        # progress bar
        self.progress_bar = ctk.CTkProgressBar(master=self, height=10, width=420, corner_radius=0)
        self.progress_bar.grid(row=1, column=0, padx=(10,0))
        
        # percent label
        self.progress_percent = ctk.CTkLabel(master=self, text="[percentage here]")
        self.progress_percent.grid(row=1, column=1, sticky="we", padx=(20,20), pady=(2,2))

class DownloadListFrame(ctk.CTkFrame):
    
    download_list = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ============ Current download
        self.current_dl = DownloadItemFrame(master=self, corner_radius=0)
        self.current_dl.pack(fill=tk.X, padx=10, pady=5)
        
        # ============ Waiting list
        self.title_label = ctk.CTkLabel(master=self, text="Download List", font=('Helvetica', 14, 'bold'))
        self.title_label.pack()
        
        self.dl_list = ctk.CTkTextbox(master=self, corner_radius=0, state="disabled", fg_color="gray70", height=180)
        self.dl_list.pack(fill=tk.BOTH, padx=10, pady=5)
        
    
    def get_download_list(self):
        return self.download_list


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
        self.setting_button.configure(command=self.master.on_open)
        self.setting_button.pack(side=tk.RIGHT)

class App(ctk.CTk):
    """
    Main application interface
    """
    WIDTH = 600
    HEIGHT = 520
    
    download_list = []
    output_format = "mp3"
    output_dir = str(Path.home())+"\download\\"
    
    def __init__(self):
        super().__init__()
        
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

    
    def on_open(self):
        if self.output_window.state() == "withdrawn":
            self.output_window.deiconify()
            self.output_window.grab_set()
    
    def on_closing(self, event=0):
        self.destroy()

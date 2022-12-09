import os
import time
from tktooltip import ToolTip
import customtkinter as ctk
import tkinter as tk
from errors import URLError

import yt_dl

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme(os.path.abspath("../static/theme.json"))


class SettingFrame(ctk.CTkFrame):
    """
    Display settings frame
    """

    def __init__(self, master, name):
        super().__init__()
        self.master = master
        self.name = name


class LeftFrame(ctk.CTkFrame):
    """
    Left frame control panel
    """

    def __init__(self, master, name):
        super().__init__()
        self.master = master
        self.name = name

        self.grid(row=0, column=0, sticky="nswe")

        self.grid_rowconfigure(0, minsize=10)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(8, minsize=20)
        self.grid_rowconfigure(11, minsize=10)

        self.label_1 = ctk.CTkLabel(
            master=self, text="Logo Here", text_font=("Roboto Medium", -16)
        )  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        # Setting button
        self.setting_button = ctk.CTkButton(
            master=self, text="Settings", border_width=2, command=self.show_settings
        )
        self.setting_button.grid(
            row=9, column=0, columnspan=1, pady=0, padx=0, sticky="we"
        )

        # Quit button
        self.quit_button = ctk.CTkButton(
            master=self,
            text="Quit",
            border_width=2,
            fg_color="#633131",
            command=self.close,
        )
        self.quit_button.grid(
            row=10, column=0, columnspan=1, pady=0, padx=0, sticky="we"
        )

    # =========== Callbacks ============ #
    def show_settings(self):
        for child in self.master.winfo_children():
            if child.winfo_name() == "!middleframe":
                child.place_forget()

    def close(self):
        time.sleep(0.5)
        self.master.destroy()


class MiddleFrame(ctk.CTkFrame):
    """
    Middle Frame panel class
    """

    def __init__(self, master, name):
        super().__init__()
        self.master = master
        self.name = name

        self.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # configure grid layout (3x7)
        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.rowconfigure(2, weight=10)
        self.columnconfigure((0, 1), weight=1)
        self.columnconfigure(2, weight=0)

        # ============================= Url Entry ============================== #
        # global setting
        self.frame_url = ctk.CTkFrame(master=self)
        self.frame_url.grid(
            row=0, column=0, columnspan=4, rowspan=1, pady=0, padx=0, sticky="nsew"
        )
        self.frame_url.rowconfigure((0, 1), weight=1)
        self.frame_url.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Url entry
        self.entry = ctk.CTkEntry(
            master=self.frame_url,
            width=120,
            placeholder_text="Enter your url here",
            text_color="white",
        )
        self.entry.grid(
            row=0, column=0, columnspan=4, pady=10, padx=10, sticky="nsew"
        )

        # Add button
        plus_image = tk.PhotoImage(file=os.path.abspath("../static/img/plus.png"))
        self.add_button = ctk.CTkButton(
            master=self.frame_url,
            text="",
            border_width=2,
            height=40,
            width=40,
            image=plus_image,
            command=self.add_button_event,
        )
        self.add_button.grid(
            row=1, column=0, columnspan=1, pady=0, padx=(10, 2), sticky="we"
        )
        ToolTip(self.add_button, msg="Add url to download list", delay=1.0)

        # Download button
        self.add_button = ctk.CTkButton(
            master=self.frame_url,
            text="Download",
            border_width=2,
            height=40,
            width=40,
            # image=plus_image,
            command=self.download_button_event,
        )
        self.add_button.grid(row=1, column=1, columnspan=2, pady=0, padx=0, sticky="we")

    # =========================== Download List =========================== #
    
    # global setting
        self.frame_url = ctk.CTkFrame(master=self)
        self.frame_url.grid(
            row=1, column=0, columnspan=4, rowspan=1, pady=10, padx=0, sticky="nsew"
        )
        self.frame_url.rowconfigure((0, 1), weight=1)
        self.frame_url.columnconfigure((0, 1, 2, 3), weight=1)
    
    # list box
    

    # ============================= Callbacks ============================= #
    def add_button_event(self):
        print("Add pressed")

    def download_button_event(self):
        print("Download pressed")
        if self.entry.get() == "":
            pass
        else:
            try:
                yt_dl.downloader(self.entry.get())
            except URLError:
                pass


class App(ctk.CTk):
    """
    Main app
    """

    MIN_WIDTH = 1000
    MIN_HEIGHT = 800

    def __init__(self):
        super().__init__()

        self.title("Lotus YT Downloader")
        self.geometry(f"{self.MIN_WIDTH}x{self.MIN_HEIGHT}")
        self.minsize(800, 600)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ============ creating two frame ============ #

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left frame for options and menu frame
        self.frame_left = LeftFrame(master=self, name="optionframe")
        # Middle frame
        self.frame_middle = MiddleFrame(master=self, name="middleframe")

    # =============== Callbacks ================== #
    def on_closing(self, event=0):
        """
        Destroy app on closing
        """
        time.sleep(0.5)
        self.destroy()

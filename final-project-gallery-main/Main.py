from customtkinter import *
from PIL import Image
from login import LoginWindow
from database import get_photos
from tkinter import filedialog
import os
from PIL import Image
from database import add_photo
from AlbumPage import AlbumPage
from TimelinePage import TimelinePage
from FavoritePage import FavoritePage
from TrashPage import TrashPage
from SwitchUser import SwitchUserDialog

class MainWindow():
    def __init__(self, user_id):

        self.user_id = user_id
        self.App = CTk()
        self.App.title("wiileen's gallery")
        self.App.after(0, lambda: self.App.state("zoomed"))
        
        # Images for buttons------------------------------------------------------------------------------
        self.img0 = CTkImage(Image.open("/Users/rose-saryrebong/Downloads/final-project-gallery-main/icons/menu.jpeg"), size=(20,20))
        self.img1 = CTkImage(Image.open("/Users/rose-saryrebong/Downloads/final-project-gallery-main/icons/timeline.jpeg"), size=(20,20))
        self.img2 = CTkImage(Image.open("/Users/rose-saryrebong/Downloads/final-project-gallery-main/icons/album.jpeg"), size=(20,20))
        self.img3 = CTkImage(Image.open("/Users/rose-saryrebong/Downloads/final-project-gallery-main/icons/heart.jpeg"), size=(20,20))
        self.img4 = CTkImage(Image.open("/Users/rose-saryrebong/Downloads/final-project-gallery-main/icons/trash.jpeg"), size=(20,20))
        self.img5 = CTkImage(Image.open("/Users/rose-saryrebong/Downloads/final-project-gallery-main/icons/close.jpeg"), size=(20,20))
        self.img6 = CTkImage(Image.open("/Users/rose-saryrebong/Downloads/final-project-gallery-main/icons/user.jpeg"), size=(20,20))
        
        self.is_menu_maximized = True
        self.all_images = []
        self.current_view = "timeline"
        
        # Main frame----------------------------------------------------------------------------------------
        self.Main_frame = CTkFrame(self.App, width=850, height=450, fg_color= "#ffd6dc", corner_radius=0)
        self.Main_frame.pack(fill="both", expand=True)

        # Side Bar--------------------------------------------------------------------------------------------
        self.Sidebar = CTkFrame(self.Main_frame, width=65, height=450, fg_color="#ffd6dc", corner_radius=0)
        self.Sidebar.pack(side="left", fill="y", padx=(2,0))
        self.is_menu_maximized = True

        # Side Bar Buttons-------------------------------------------------------------------------------------
        start_y = 50
        gap = 35

        self.btn_menu = CTkButton(
            self.Sidebar, width=40, height=30, image=self.img0, fg_color="#ffb7ce", corner_radius=25, hover_color="#ffe7eb",
            text = "", text_color="#ffffff", font=("Arial", 14, "bold"), 
            command=self.resize_Sidebar
        )
        self.btn_menu.place(x=10, y=start_y)

        self.btn_timeline = CTkButton(
            self.Sidebar, width=40, height=30, image=self.img1, fg_color="#ffb7ce", corner_radius=25, hover_color="#ffe7eb",
            text = "", text_color="#ffffff", font=("Arial", 14, "bold")
        )
        self.btn_timeline.place(x=10, y=start_y + gap)

        self.btn_albums = CTkButton(
            self.Sidebar, width=40, height=30, image=self.img2, fg_color="#ffb7ce", corner_radius=25, hover_color="#ffe7eb",
            text = "", text_color="#ffffff", font=("Arial", 14, "bold")
        )
        self.btn_albums.place(x=10, y=start_y + gap * 2)

        self.btn_favorites = CTkButton(
            self.Sidebar, width=40, height=30, image=self.img3, fg_color="#ffb7ce", corner_radius=25, hover_color="#ffe7eb",
            text = "", text_color="#ffffff", font=("Arial", 14, "bold")
        )
        self.btn_favorites.place(x=10, y=start_y + gap * 3)

        self.btn_trash = CTkButton(
            self.Sidebar, width=40, height=30, image=self.img4, fg_color="#ffb7ce", corner_radius=25, hover_color="#ffe7eb",
            text = "", text_color="#ffffff", font=("Arial", 14, "bold")
        )
        self.btn_trash.place(x=10, y=start_y + gap * 4)

        self.btn_switch = CTkButton(
            self.Sidebar, width=40, height=30, image=self.img6, fg_color="#ffb7ce", corner_radius=25, hover_color="#ffe7eb",
            text = "", text_color="#ffffff", font=("Arial", 14, "bold"),
            command=self.switch_user
        )
        self.btn_switch.place(x=10, y=start_y + gap * 5)

        self.btn_close = CTkButton(
            self.Sidebar, width=40, height=30, image=self.img5,fg_color="#ffb7ce", corner_radius=25, hover_color="#ffe7eb",
            text = "", text_color="#ffffff", font=("Arial", 14, "bold"),
            command=self.close
        )
        self.btn_close.pack(side="bottom", pady=10, padx=(10,0))

        # Content----------------------------------------------------------------------------------------
        self.Content_frame = CTkFrame(self.Main_frame, fg_color="#ffd6dc")
        self.Content_frame.pack(fill="both", expand=True)
        self.Album = AlbumPage(self.Content_frame, self.toggle_album, user_id=user_id)
        self.Timeline = TimelinePage(self.Content_frame, self.toggle_timeline, user_id=user_id)
        self.Favorites = FavoritePage(self.Content_frame, self.toggle_favorites, user_id=user_id)
        self.Trash = TrashPage(self.Content_frame, self.toggle_trash, user_id=user_id)

        # Scrollable grid----------------------------------------------------------------------------------
        #self.Main_bar = CTkScrollableFrame(
        #    self.Content_frame, height=450, fg_color="#ffffff", corner_radius=25
        #)
        #self.Main_bar.pack(side="top", fill="both", expand=True, padx=10, pady=(5,10))

        
        # WIRE UP BUTTONS----------------------------------------------------------------------------------------
        self.btn_albums.configure(command=lambda: self.switch_page("albums"))
        self.btn_timeline.configure(command=lambda: self.switch_page("timeline"))
        self.btn_favorites.configure(command=lambda: self.switch_page("favorites"))
        self.btn_trash.configure(command=lambda: self.switch_page("trash"))

        self.switch_page("timeline")
        self.App.mainloop()

    # Sidebar toggle----------------------------------------------------------------------------------------
    def resize_Sidebar(self):
        if self.is_menu_maximized:
            self.Sidebar.configure(width=1700)
            self.btn_menu.configure(text="Menu", width=120, image=None)
            self.btn_albums.configure(text="Albums", width=120, image=None)
            self.btn_favorites.configure(text="Favorites", width=120, image=None)
            self.btn_close.configure(text="Close", width=120, image=None)
            self.btn_timeline.configure(text="Timeline", width=120, image=None)
            self.btn_trash.configure(text="Trash", width=120, image=None)
            self.btn_switch.configure(text="Switch User", width=120, image=None)
            self.is_menu_maximized = False
        else:
            self.Sidebar.configure(width=65)
            self.btn_menu.configure(text="", width=40, image=self.img0)
            self.btn_albums.configure(text="", width=40, image=self.img2)
            self.btn_favorites.configure(text="", width=40, image=self.img3)
            self.btn_close.configure(text="", width=40, image=self.img5)
            self.btn_timeline.configure(text="", width=40, image=self.img1)
            self.btn_trash.configure(text="", width=40, image=self.img4)
            self.btn_switch.configure(text="", width=40, image=self.img6)
            self.is_menu_maximized = True

    def close(self):
        self.App.destroy()

    def switch_page(self, page):
        self.Album.hide()
        self.Timeline.hide()
        self.Favorites.hide()
        self.Trash.hide()

        if page == "albums":
            self.Album.show()
        elif page == "timeline":
            self.Timeline.show()
        elif page == "favorites":
            self.Favorites.show()
        elif page == "trash":
            self.Trash.show()

    def switch_user(self):
        SwitchUserDialog(self.App, self.user_id, self.on_user_switched)

    def on_user_switched(self, new_user_id):
        self.App.destroy()
        MainWindow(new_user_id)

    def toggle_album(self, showing): pass
    def toggle_timeline(self, showing): pass
    def toggle_favorites(self, showing): pass
    def toggle_trash(self, showing): pass

login = LoginWindow()
if login.success:
    app = MainWindow(login.user_id)
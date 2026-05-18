from customtkinter import *
from PIL import Image
from tkinter import filedialog
import shutil
import os

from database import (
    add_photo,
    get_photos_by_album,
    delete_photo,
    toggle_favorite
)

class PhotoViewer:

    def __init__(self, parent, album_id, album_name, user_id):

        self.parent = parent
        self.album_id = album_id
        self.album_name = album_name
        self.user_id = user_id

        self.images = []

        # WINDOW----------------------------------------------
        self.window = CTkToplevel(parent)

        self.window.title(album_name)
        self.window.geometry("900x600")

        self.window.configure(
            fg_color="#ffd6dc"
        )

        # HEADER--------------------------------------------
        top = CTkFrame(
            self.window,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        CTkLabel(
            top,
            text=album_name,
            font=("Arial", 22, "bold"),
            text_color="#c75b7a"
        ).pack(side="left")

        CTkButton(
            top,
            text="+ Add Photos",
            width=130,
            fg_color="#ffb7ce",
            hover_color="#ffe7eb",
            text_color="#ffffff",
            command=self.import_photos
        ).pack(side="right")

        # PHOTO GRID----------------------------------------
        
        self.grid_frame = CTkScrollableFrame(
            self.window,
            fg_color="#ffffff",
            corner_radius=20
        )

        self.grid_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.load_photos()

        
    # LOAD PHOTOS----------------------------------------

    def load_photos(self):

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        photos = get_photos_by_album(
            self.album_id
        )

        self.images.clear()

        if not photos:

            CTkLabel(
                self.grid_frame,
                text="No photos yet 🌸",
                text_color="gray",
                font=("Arial", 16)
            ).pack(pady=50)

            return

        row = 0
        col = 0
        COLS = 8
        THUMB = 150

        for photo_id, filename, filepath, title, fav in photos:

            try:
                
                print("Loading:", filepath)
                
                # CHECK IF FILE EXISTS--------------------------------
                if not os.path.exists(filepath):
                    print("File not found:", filepath)
                    continue
                
                # OPEN AND RESIZE IMAGE--------------------------------
                img = Image.open(filepath).convert("RGB")
                img.thumbnail((170, 170), Image.LANCZOS)

                # CTK IMAGE--------------------------------------------
                ctk_img = CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(170, 170)
                )

                self.images.append(ctk_img)

                # CARD--------------------------------------------
                card = CTkFrame(
                    self.grid_frame,
                    width=THUMB + 20,
                    height=THUMB + 60,
                    fg_color="#ffe7eb",
                    corner_radius=16
                )
                card.grid(row=row, column=col, padx=10, pady=10)
                card.grid_propagate(False)

                # IMAGE LABEL--------------------------------------------
                img_label = CTkButton(
                    card,
                    image=ctk_img,
                    text="",
                    width=THUMB,
                    height=THUMB,
                    border_width=0,
                    fg_color="transparent",
                    hover_color="#ffd6dc",
                )

                img_label.image = ctk_img
                img_label.pack(
                    pady=(10,5)
                )

                # CLICK IMAGE--------------------------------------------
                img_label.bind(
                    "<Button-1>",
                    lambda e, p=filepath: self.open_image(p)
                )

                # BOTTOM AREA--------------------------------------------
                bottom_frame = CTkFrame(
                    card,
                    fg_color="transparent"
                )

                bottom_frame.pack(
                    fill="x",
                    padx=10,
                    pady=(0, 5)

                )

                # FILE NAME---------------------------------------------
                CTkLabel(
                    bottom_frame,
                    text=filename[:15],
                    font=("Arial", 12, "bold"),
                    text_color="#c75b7a"
                ).pack(side="left")

                # FAVORITE BUTTON--------------------------------------------
                heart = "❤️" if fav else "🤍"

                CTkButton(
                    bottom_frame,
                    text=heart,
                    width=32, height=32,
                    corner_radius=50,
                    fg_color="transparent",
                    hover_color="#ffd6dc",
                    text_color="#ff4d6d",
                    font=("Arial", 18),
                    command=lambda pid=photo_id: self.favorite_photo(pid)
                ).pack(side="right")
                
                # DELETE BUTTON--------------------------------------------
                CTkButton(
                    card,
                    text="Delete",
                    width=90,
                    height=28,
                    fg_color="#ff8fa3",
                    hover_color="#ffccd5",
                    text_color="#ffffff",
                    command=lambda pid=photo_id: self.remove_photo(pid)
                ).pack(pady=6)

                col += 1

                if col >= COLS:
                    col = 0
                    row += 1

            except Exception as e:
                print("Error loading photo:")
                print(filepath)
                print(e)
                print(e)

            
    # IMPORT PHOTOS----------------------------------------

    def import_photos(self):
    
        self.window.grab_release()
        filepaths = filedialog.askopenfilenames(
            parent=self.window,
            title="Select Photos",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")]
        )
        self.window.grab_set()

        if not filepaths:
            return

        base_dir = os.path.dirname(os.path.abspath(__file__))
        photos_dir = os.path.join(base_dir, "photos")
        os.makedirs(photos_dir, exist_ok=True)

        for filepath in filepaths:
            filename = os.path.basename(filepath)
            name, ext = os.path.splitext(filename)
            destination = os.path.join(photos_dir, filename)

            counter = 1
            while os.path.exists(destination):
                destination = os.path.join(photos_dir, f"{name}_{counter}{ext}")
                counter += 1

            filename = os.path.basename(destination)
            shutil.copy(filepath, destination)
            print("Saved to:", destination)
            print("Album ID:", self.album_id)
            add_photo(
                filename=filename,
                filepath=destination,
                album_id=self.album_id,
                user_id=self.user_id
            )

        self.load_photos()

    # OPEN IMAGE----------------------------------------

    def open_image(self, filepath):

        viewer = CTkToplevel(self.window)

        viewer.geometry("1000x700")
        viewer.title("Photo Viewer")

        img = Image.open(filepath)

        width, height = img.size

        scale = min(
            900 / width,
            600 / height
        )

        new_size = (
            int(width * scale),
            int(height * scale)
        )

        img = img.resize(new_size)

        ctk_img = CTkImage(
            light_image=img,
            dark_image=img,
            size=new_size
        )

        label = CTkLabel(
            viewer,
            image=ctk_img,
            text=""
        )

        label.image = ctk_img
        label.pack(expand=True)

    # DELETE PHOTO----------------------------------------

    def remove_photo(self, photo_id):

        delete_photo(photo_id)

        self.load_photos()

    # FAVORITE PHOTO--------------------------------------------
    def favorite_photo(self, photo_id):
        toggle_favorite(photo_id)
        self.load_photos()
from customtkinter import *
from PIL import Image
import os
from database import get_favorite_photos, toggle_favorite

class FavoritePage:
    def __init__(self, frame, on_toggle, user_id):
        self.user_id = user_id
        self.frame = frame
        self.on_toggle = on_toggle
        self.images = []

        # HEADER------------------------------
        self.header_frame = CTkFrame(frame, fg_color="transparent")

        self.titlebar = CTkLabel(
            self.header_frame,
            text="Favorites",
            width=300,
            height=35,
            fg_color="#ffb7ce",
            corner_radius=15,
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )

        # SCROLLABLE CONTENT------------------------------
        self.scroll_frame = CTkScrollableFrame(
            frame,
            fg_color="#ffffff",
            corner_radius=25
        )

    # ── LOAD ──────────────────────────────────────────────────────
    def load_favorite(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.images.clear()

        photos = get_favorite_photos(user_id=self.user_id)

        if not photos:
            CTkLabel(
                self.scroll_frame,
                text="No favorites yet 🌸\nHeart a photo to see it here.",
                text_color="gray",
                font=("Arial", 15),
                justify="center"
            ).pack(pady=60)
            return

        # PHOTO GRID------------------------------
        col = 0
        row = 0
        COLS = 8
        THUMB = 160
        
        grid = CTkFrame(self.scroll_frame, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=10, pady=10)

        for photo in photos:
            photo_id = photo[0]
            filename = photo[1]
            filepath = photo[2]
            is_fav   = photo[5]

            if not os.path.exists(filepath):
                continue

            try:
                img = Image.open(filepath).convert("RGB")
                img.thumbnail((THUMB, THUMB), Image.LANCZOS)
                ctk_img = CTkImage(light_image=img, dark_image=img, size=(THUMB, THUMB))
                self.images.append(ctk_img)
            except Exception:
                continue

            # CARD------------------------------
            card = CTkFrame(
                grid,
                width=THUMB + 20,
                height=THUMB + 60,
                fg_color="#ffe7eb",
                corner_radius=16
            )
            card.grid(row=row, column=col, padx=10, pady=10)
            card.grid_propagate(False)

            # IMAGE BUTTON------------------------------
            img_btn = CTkButton(
                card,
                image=ctk_img,
                text="",
                width=THUMB,
                height=THUMB,
                fg_color="transparent",
                hover_color="#ffd6dc",
                corner_radius=12,
                command=lambda p=filepath: self.open_fullscreen(p)
            )
            img_btn.pack(pady=(8, 4))

            # FILENAME------------------------------
            CTkLabel(
                card,
                text=filename[:18],
                font=("Arial", 11, "bold"),
                text_color="#c75b7a"
            ).pack()

            # HEART BUTTON------------------------------
            heart_btn = CTkButton(
                card,
                text="♥ Unfavorite",
                width=120,
                height=26,
                fg_color="#ff8fa3",
                hover_color="#ffccd5",
                text_color="#ffffff",
                corner_radius=12,
                font=("Arial", 11, "bold"),
                command=lambda pid=photo_id: self.unfavorite(pid)
            )
            heart_btn.pack(pady=(4, 8))

            col += 1
            if col >= COLS:
                col = 0
                row += 1

    # ── UNFAVORITE ────────────────────────────────────────────────
    def unfavorite(self, photo_id):
        toggle_favorite(photo_id)
        self.load_favorite()

    # ── FULLSCREEN ────────────────────────────────────────────────
    def open_fullscreen(self, filepath):
        viewer = CTkToplevel(self.frame)
        viewer.geometry("1000x700")
        viewer.title("Photo Viewer")
        viewer.configure(fg_color="#1a1a1a")
        viewer.grab_set()

        try:
            img = Image.open(filepath)
            w, h = img.size
            scale = min(950 / w, 650 / h)
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.LANCZOS)
            ctk_img = CTkImage(light_image=img, dark_image=img, size=new_size)
            lbl = CTkLabel(viewer, image=ctk_img, text="")
            lbl.image = ctk_img
            lbl.pack(expand=True)
        except Exception as e:
            CTkLabel(viewer, text=f"Could not open image.\n{e}",
                     text_color="gray").pack(expand=True)

        viewer.bind("<Escape>", lambda e: viewer.destroy())

    # ── SHOW / HIDE ───────────────────────────────────────────────
    def show(self):
        self.on_toggle(True)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.titlebar.pack(side="left")
        self.scroll_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
        self.load_favorite()

    def hide(self):
        self.on_toggle(False)
        self.header_frame.pack_forget()
        self.scroll_frame.pack_forget()

from customtkinter import *
from PIL import Image
import os
from database import get_favorite_photos, toggle_favorite

class FavoritePage:
    def __init__(self, frame, on_toggle, user_id):
        self.user_id = user_id
        self.frame = frame
        self.on_toggle = on_toggle
        self.images = []

        # HEADER------------------------------
        self.header_frame = CTkFrame(frame, fg_color="transparent")

        self.titlebar = CTkLabel(
            self.header_frame,
            text="Favorites",
            width=300,
            height=35,
            fg_color="#ffb7ce",
            corner_radius=15,
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )

        # ✅ TOTAL LABEL (ADDED)
        self.total_label = CTkLabel(
            self.header_frame,
            text="Total Favorites: 0",
            font=("Arial", 13, "bold"),
            text_color="#c75b7a"
        )

        # SCROLLABLE CONTENT------------------------------
        self.scroll_frame = CTkScrollableFrame(
            frame,
            fg_color="#ffffff",
            corner_radius=25
        )

    # ── LOAD ──────────────────────────────────────────────────────
    def load_favorite(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.images.clear()

        photos = get_favorite_photos(user_id=self.user_id)

        # ✅ UPDATE COUNT (ADDED)
        total = len(photos)
        self.total_label.configure(text=f"Total Favorites: {total}")

        if not photos:
            CTkLabel(
                self.scroll_frame,
                text="No favorites yet 🌸\nHeart a photo to see it here.",
                text_color="gray",
                font=("Arial", 15),
                justify="center"
            ).pack(pady=60)
            return

        col = 0
        row = 0
        COLS = 8
        THUMB = 160

        grid = CTkFrame(self.scroll_frame, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=10, pady=10)

        for photo in photos:
            photo_id = photo[0]
            filename = photo[1]
            filepath = photo[2]

            if not os.path.exists(filepath):
                continue

            try:
                img = Image.open(filepath).convert("RGB")
                img.thumbnail((THUMB, THUMB), Image.LANCZOS)
                ctk_img = CTkImage(light_image=img, dark_image=img, size=(THUMB, THUMB))
                self.images.append(ctk_img)
            except Exception:
                continue

            card = CTkFrame(
                grid,
                width=THUMB + 20,
                height=THUMB + 60,
                fg_color="#ffe7eb",
                corner_radius=16
            )
            card.grid(row=row, column=col, padx=10, pady=10)
            card.grid_propagate(False)

            CTkButton(
                card,
                image=ctk_img,
                text="",
                width=THUMB,
                height=THUMB,
                fg_color="transparent",
                hover_color="#ffd6dc",
                corner_radius=12,
                command=lambda p=filepath: self.open_fullscreen(p)
            ).pack(pady=(8, 4))

            CTkLabel(
                card,
                text=filename[:18],
                font=("Arial", 11, "bold"),
                text_color="#c75b7a"
            ).pack()

            CTkButton(
                card,
                text="♥ Unfavorite",
                width=120,
                height=26,
                fg_color="#ff8fa3",
                hover_color="#ffccd5",
                text_color="#ffffff",
                corner_radius=12,
                font=("Arial", 11, "bold"),
                command=lambda pid=photo_id: self.unfavorite(pid)
            ).pack(pady=(4, 8))

            col += 1
            if col >= COLS:
                col = 0
                row += 1

    # ── UNFAVORITE ────────────────────────────────────────────────
    def unfavorite(self, photo_id):
        toggle_favorite(photo_id)
        self.load_favorite()

    # ── FULLSCREEN ────────────────────────────────────────────────
    def open_fullscreen(self, filepath):
        viewer = CTkToplevel(self.frame)
        viewer.geometry("1000x700")
        viewer.title("Photo Viewer")
        viewer.configure(fg_color="#1a1a1a")
        viewer.grab_set()

        try:
            img = Image.open(filepath)
            w, h = img.size
            scale = min(950 / w, 650 / h)
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.LANCZOS)

            ctk_img = CTkImage(light_image=img, dark_image=img, size=new_size)

            lbl = CTkLabel(viewer, image=ctk_img, text="")
            lbl.image = ctk_img
            lbl.pack(expand=True)

        except Exception as e:
            CTkLabel(
                viewer,
                text=f"Could not open image.\n{e}",
                text_color="gray"
            ).pack(expand=True)

        viewer.bind("<Escape>", lambda e: viewer.destroy())

    # ── SHOW / HIDE ───────────────────────────────────────────────
    def show(self):
        self.on_toggle(True)

        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.titlebar.pack(side="left")

        # ✅ ADD THIS
        self.total_label.pack(side="left", padx=15)

        self.scroll_frame.pack(
            side="top",
            fill="both",
            expand=True,
            padx=10,
            pady=(5, 10)
        )

        self.load_favorite()

    def hide(self):
        self.on_toggle(False)
        self.header_frame.pack_forget()
        self.scroll_frame.pack_forget()
# from customtkinter import *
# from PIL import Image
# import os
# from database import get_trashed_photos, restore_photo, permanent_delete, empty_trash

# class TrashPage:
#     def __init__(self, frame, on_toggle, user_id):
#         self.user_id = user_id
#         self.frame = frame
#         self.on_toggle = on_toggle
#         self.images = []

#         # HEADER------------------------------
#         self.header_frame = CTkFrame(frame, fg_color="transparent")

#         self.titlebar = CTkLabel(
#             self.header_frame,
#             text="Trash",
#             width=300,
#             height=35,
#             fg_color="#ffb7ce",
#             corner_radius=15,
#             font=("Arial", 18, "bold"),
#             text_color="#ffffff"
#         )

#         self.empty_btn = CTkButton(
#             self.header_frame,
#             text="🗑 Empty Trash",
#             width=130,
#             height=35,
#             fg_color="#ff8fa3",
#             hover_color="#ffccd5",
#             corner_radius=15,
#             font=("Arial", 12, "bold"),
#             text_color="#ffffff",
#             command=self.confirm_empty_trash
#         )

#         # SCROLLABLE CONTENT------------------------------
#         self.scroll_frame = CTkScrollableFrame(
#             frame,
#             fg_color="#ffffff",
#             corner_radius=25
#         )

#     # ── LOAD ──────────────────────────────────────────────────────
#     def load_trash(self):
#         for widget in self.scroll_frame.winfo_children():
#             widget.destroy()
#         self.images.clear()

#         photos = get_trashed_photos(user_id=self.user_id)

#         if not photos:
#             CTkLabel(
#                 self.scroll_frame,
#                 text="Trash is empty 🌸",
#                 text_color="gray",
#                 font=("Arial", 15)
#             ).pack(pady=60)
#             return

#         grid = CTkFrame(self.scroll_frame, fg_color="transparent")
#         grid.pack(fill="both", expand=True, padx=10, pady=10)

#         col = 0
#         row = 0
#         COLS = 4
#         THUMB = 160

#         for photo in photos:
#             photo_id  = photo[0]
#             filename  = photo[1]
#             filepath  = photo[2]
#             deleted_at = photo[7]

#             if not os.path.exists(filepath):
#                 col += 1
#                 if col >= COLS:
#                     col = 0
#                     row += 1
#                 continue

#             try:
#                 img = Image.open(filepath).convert("RGB")
#                 img.thumbnail((THUMB, THUMB), Image.LANCZOS)
#                 ctk_img = CTkImage(light_image=img, dark_image=img, size=(THUMB, THUMB))
#                 self.images.append(ctk_img)
#             except Exception:
#                 continue

#             # CARD------------------------------
#             card = CTkFrame(
#                 grid,
#                 width=THUMB + 20,
#                 height=THUMB + 90,
#                 fg_color="#ffe7eb",
#                 corner_radius=16
#             )
#             card.grid(row=row, column=col, padx=10, pady=10)
#             card.grid_propagate(False)

#             # IMAGE------------------------------
#             CTkLabel(
#                 card,
#                 image=ctk_img,
#                 text=""
#             ).pack(pady=(8, 4))

#             # FILENAME------------------------------
#             CTkLabel(
#                 card,
#                 text=filename[:18],
#                 font=("Arial", 11, "bold"),
#                 text_color="#c75b7a"
#             ).pack()

#             # DELETED DATE------------------------------
#             if deleted_at:
#                 CTkLabel(
#                     card,
#                     text=f"Deleted: {deleted_at[:10]}",
#                     font=("Arial", 9),
#                     text_color="gray"
#                 ).pack()

#             # BUTTONS------------------------------
#             btn_frame = CTkFrame(card, fg_color="#ffe7eb", corner_radius=0)
#             btn_frame.pack(pady=(4, 8))

#             CTkButton(
#                 btn_frame,
#                 text="Restore",
#                 width=80,
#                 height=26,
#                 fg_color="#ffb7ce",
#                 hover_color="#ffe7eb",
#                 text_color="#ffffff",
#                 corner_radius=12,
#                 font=("Arial", 10, "bold"),
#                 command=lambda pid=photo_id: self.restore(pid)
#             ).pack(side="left", padx=3)

#             CTkButton(
#                 btn_frame,
#                 text="Delete",
#                 width=80,
#                 height=26,
#                 fg_color="#ff8fa3",
#                 hover_color="#ffccd5",
#                 text_color="#ffffff",
#                 corner_radius=12,
#                 font=("Arial", 10, "bold"),
#                 command=lambda pid=photo_id: self.confirm_permanent_delete(pid)
#             ).pack(side="left", padx=3)

#             col += 1
#             if col >= COLS:
#                 col = 0
#                 row += 1

#     # ── RESTORE ───────────────────────────────────────────────────
#     def restore(self, photo_id):
#         restore_photo(photo_id)
#         self.load_trash()

#     # ── PERMANENT DELETE ──────────────────────────────────────────
#     def confirm_permanent_delete(self, photo_id):
#         dialog = CTkToplevel(self.frame)
#         dialog.title("Permanently Delete")
#         dialog.geometry("300x160")
#         dialog.resizable(False, False)
#         dialog.grab_set()
#         dialog.configure(fg_color="#ffd6dc")

#         CTkLabel(
#             dialog,
#             text="Permanently delete this photo?",
#             font=("Arial", 14, "bold"),
#             text_color="#c75b7a",
#             wraplength=260
#         ).pack(pady=(20, 6))

#         CTkLabel(
#             dialog,
#             text="This cannot be undone.",
#             font=("Arial", 11),
#             text_color="gray"
#         ).pack()

#         btn_frame = CTkFrame(dialog, fg_color="transparent")
#         btn_frame.pack(pady=16)

#         CTkButton(
#             btn_frame,
#             text="Cancel",
#             width=90,
#             fg_color="#ffffff",
#             hover_color="#ffe7eb",
#             text_color="#c75b7a",
#             command=dialog.destroy
#         ).pack(side="left", padx=5)

#         def delete_now():
#             permanent_delete(photo_id)
#             self.load_trash()
#             dialog.destroy()

#         CTkButton(
#             btn_frame,
#             text="Delete",
#             width=90,
#             fg_color="#ff8fa3",
#             hover_color="#ffccd5",
#             text_color="#ffffff",
#             command=delete_now
#         ).pack(side="left", padx=5)

#     # ── EMPTY TRASH ───────────────────────────────────────────────
#     def confirm_empty_trash(self):
#         dialog = CTkToplevel(self.frame)
#         dialog.title("Empty Trash")
#         dialog.geometry("300x160")
#         dialog.resizable(False, False)
#         dialog.grab_set()
#         dialog.configure(fg_color="#ffd6dc")

#         CTkLabel(
#             dialog,
#             text="Empty all trash?",
#             font=("Arial", 14, "bold"),
#             text_color="#c75b7a"
#         ).pack(pady=(20, 6))

#         CTkLabel(
#             dialog,
#             text="All photos will be permanently deleted.",
#             font=("Arial", 11),
#             text_color="gray",
#             wraplength=260
#         ).pack()

#         btn_frame = CTkFrame(dialog, fg_color="transparent")
#         btn_frame.pack(pady=16)

#         CTkButton(
#             btn_frame,
#             text="Cancel",
#             width=90,
#             fg_color="#ffffff",
#             hover_color="#ffe7eb",
#             text_color="#c75b7a",
#             command=dialog.destroy
#         ).pack(side="left", padx=5)

#         def empty_now():
#             empty_trash()
#             self.load_trash()
#             dialog.destroy()

#         CTkButton(
#             btn_frame,
#             text="Empty",
#             width=90,
#             fg_color="#ff8fa3",
#             hover_color="#ffccd5",
#             text_color="#ffffff",
#             command=empty_now
#         ).pack(side="left", padx=5)

#     # ── SHOW / HIDE ───────────────────────────────────────────────
#     def show(self):
#         self.on_toggle(True)
#         self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
#         self.titlebar.pack(side="left")
#         self.empty_btn.pack(side="right")
#         self.scroll_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
#         self.load_trash()

#     def hide(self):
#         self.on_toggle(False)
#         self.header_frame.pack_forget()
#         self.empty_btn.pack_forget()
#         self.scroll_frame.pack_forget()

from customtkinter import *
from PIL import Image
import os
from database import get_trashed_photos, restore_photo, permanent_delete, empty_trash

class TrashPage:
    def __init__(self, frame, on_toggle, user_id):
        self.user_id = user_id
        self.frame = frame
        self.on_toggle = on_toggle
        self.images = []

        # HEADER------------------------------
        self.header_frame = CTkFrame(frame, fg_color="transparent")

        self.titlebar = CTkLabel(
            self.header_frame,
            text="Trash",
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
            text="Total Deleted: 0",
            font=("Arial", 13, "bold"),
            text_color="#c75b7a"
        )

        self.empty_btn = CTkButton(
            self.header_frame,
            text="🗑 Empty Trash",
            width=130,
            height=35,
            fg_color="#ff8fa3",
            hover_color="#ffccd5",
            corner_radius=15,
            font=("Arial", 12, "bold"),
            text_color="#ffffff",
            command=self.confirm_empty_trash
        )

        # SCROLLABLE CONTENT------------------------------
        self.scroll_frame = CTkScrollableFrame(
            frame,
            fg_color="#ffffff",
            corner_radius=25
        )

    # ── LOAD ──────────────────────────────────────────────────────
    def load_trash(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.images.clear()

        photos = get_trashed_photos(user_id=self.user_id)

        # ✅ UPDATE COUNT (ADDED)
        total = len(photos)
        self.total_label.configure(text=f"Total Deleted: {total}")

        if not photos:
            CTkLabel(
                self.scroll_frame,
                text="Trash is empty 🌸",
                text_color="gray",
                font=("Arial", 15)
            ).pack(pady=60)
            return

        grid = CTkFrame(self.scroll_frame, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=10, pady=10)

        col = 0
        row = 0
        COLS = 4
        THUMB = 160

        for photo in photos:
            photo_id  = photo[0]
            filename  = photo[1]
            filepath  = photo[2]
            deleted_at = photo[7]

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
                height=THUMB + 90,
                fg_color="#ffe7eb",
                corner_radius=16
            )
            card.grid(row=row, column=col, padx=10, pady=10)
            card.grid_propagate(False)

            CTkLabel(
                card,
                image=ctk_img,
                text=""
            ).pack(pady=(8, 4))

            CTkLabel(
                card,
                text=filename[:18],
                font=("Arial", 11, "bold"),
                text_color="#c75b7a"
            ).pack()

            if deleted_at:
                CTkLabel(
                    card,
                    text=f"Deleted: {deleted_at[:10]}",
                    font=("Arial", 9),
                    text_color="gray"
                ).pack()

            btn_frame = CTkFrame(card, fg_color="#ffe7eb", corner_radius=0)
            btn_frame.pack(pady=(4, 8))

            CTkButton(
                btn_frame,
                text="Restore",
                width=80,
                height=26,
                fg_color="#ffb7ce",
                hover_color="#ffe7eb",
                text_color="#ffffff",
                corner_radius=12,
                font=("Arial", 10, "bold"),
                command=lambda pid=photo_id: self.restore(pid)
            ).pack(side="left", padx=3)

            CTkButton(
                btn_frame,
                text="Delete",
                width=80,
                height=26,
                fg_color="#ff8fa3",
                hover_color="#ffccd5",
                text_color="#ffffff",
                corner_radius=12,
                font=("Arial", 10, "bold"),
                command=lambda pid=photo_id: self.confirm_permanent_delete(pid)
            ).pack(side="left", padx=3)

            col += 1
            if col >= COLS:
                col = 0
                row += 1

    # ── RESTORE ───────────────────────────────────────────────────
    def restore(self, photo_id):
        restore_photo(photo_id)
        self.load_trash()

    # ── PERMANENT DELETE ──────────────────────────────────────────
    def confirm_permanent_delete(self, photo_id):
        dialog = CTkToplevel(self.frame)
        dialog.title("Permanently Delete")
        dialog.geometry("300x160")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(fg_color="#ffd6dc")

        CTkLabel(
            dialog,
            text="Permanently delete this photo?",
            font=("Arial", 14, "bold"),
            text_color="#c75b7a"
        ).pack(pady=(20, 6))

        CTkLabel(
            dialog,
            text="This cannot be undone.",
            font=("Arial", 11),
            text_color="gray"
        ).pack()

        btn_frame = CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=16)

        CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=5)

        def delete_now():
            permanent_delete(photo_id)
            self.load_trash()
            dialog.destroy()

        CTkButton(
            btn_frame,
            text="Delete",
            fg_color="#ff8fa3",
            command=delete_now
        ).pack(side="left", padx=5)

    # ── EMPTY TRASH ───────────────────────────────────────────────
    def confirm_empty_trash(self):
        dialog = CTkToplevel(self.frame)
        dialog.title("Empty Trash")
        dialog.geometry("300x160")
        dialog.grab_set()
        dialog.configure(fg_color="#ffd6dc")

        CTkLabel(
            dialog,
            text="Empty all trash?",
            font=("Arial", 14, "bold"),
            text_color="#c75b7a"
        ).pack(pady=(20, 6))

        CTkLabel(
            dialog,
            text="All photos will be permanently deleted.",
            text_color="gray"
        ).pack()

        btn_frame = CTkFrame(dialog)
        btn_frame.pack(pady=16)

        CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=5)

        def empty_now():
            empty_trash()
            self.load_trash()
            dialog.destroy()

        CTkButton(
            btn_frame,
            text="Empty",
            fg_color="#ff8fa3",
            command=empty_now
        ).pack(side="left", padx=5)

    # ── SHOW / HIDE ───────────────────────────────────────────────
    def show(self):
        self.on_toggle(True)

        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.titlebar.pack(side="left")

        # ✅ IMPORTANT ORDER
        self.total_label.pack(side="left", padx=15)

        self.empty_btn.pack(side="right")

        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        self.load_trash()

    def hide(self):
        self.on_toggle(False)
        self.header_frame.pack_forget()
        self.empty_btn.pack_forget()
        self.scroll_frame.pack_forget()
# from customtkinter import *
# from database import (
#     get_albums,
#     add_album,
#     delete_album,
#     rename_album,
#     get_album_photo_count
# )
# from PhotoViewer import PhotoViewer

# class AlbumPage:
#     def __init__(self, Frame, on_toggle, on_open_album=None, user_id=None):
#         self.frame = Frame
#         self.on_toggle = on_toggle
#         self.on_open_album = on_open_album
#         self.user_id = user_id
#         # HEADER---------------------------------
#         self.header_frame = CTkFrame(
#             Frame,
#             fg_color="transparent"
#         )

#         self.titlebar = CTkLabel(
#             self.header_frame,
#             text="Albums",
#             width=300,
#             height=35,
#             fg_color="#ffb7ce",
#             corner_radius=15,
#             font=("Arial", 18, "bold"),
#             text_color="#ffffff"
#         )

#         self.add_btn = CTkButton(
#             self.header_frame,
#             text="+ New Album",
#             width=130,
#             height=35,
#             fg_color="#ffb7ce",
#             hover_color="#ffe7eb",
#             corner_radius=15,
#             font=("Arial", 12, "bold"),
#             text_color="#ffffff",
#             command=self.open_add_dialog
#         )

#         # SEARCH BAR------------------------------
#         self.search_entry = CTkEntry(
#             Frame,
#             placeholder_text="Search albums...",
#             height=35,
#             corner_radius=15,
#             fg_color="#ffe7eb",
#             border_width=0,
#             text_color="#000000",
#             placeholder_text_color="gray",
#             font=("Arial", 12)
#         )

#         self.search_entry.bind("<KeyRelease>", lambda e: self.load_albums())

#         # ALBUM GRID------------------------------
#         self.folders_frame = CTkScrollableFrame(
#             Frame,
#             fg_color="transparent"
#         )

#     # LOAD ALBUMS----------------------------------
#     def load_albums(self):

#         for widget in self.folders_frame.winfo_children():
#             widget.destroy()

#         search_text = self.search_entry.get().lower().strip()

#         albums = get_albums(user_id=self.user_id)

#         filtered = []

#         for album in albums:
#             album_id, name = album

#             if search_text in name.lower():
#                 filtered.append(album)

#         if not filtered:

#             empty_label = CTkLabel(
#                 self.folders_frame,
#                 text="No albums found 🌸",
#                 text_color="gray",
#                 font=("Arial", 15)
#             )

#             empty_label.pack(pady=50)
#             return

#         row = 0
#         col = 0

#         for album_id, name in filtered:

#             card = CTkFrame(
#                 self.folders_frame,
#                 width=500,
#                 height=500,
#                 fg_color="#ffffff",
#                 corner_radius=20,
#                 border_width=2,
#                 border_color="#ffe7eb"
#             )

#             card.grid(row=row, column=col, padx=8, pady=8, sticky="n")
#             card.grid_propagate(True)

#             # ALBUM COVER------------------------------
#             cover = CTkFrame(
#                 card,
#                 width=155,
#                 height=80,
#                 fg_color="#ffd6dc",
#                 corner_radius=12
#             )

#             cover.pack(pady=(10, 0))
#             cover.pack_propagate(False)

#             CTkLabel(
#                 cover,
#                 text="📁",
#                 font=("Arial", 30)
#             ).pack(expand=True)

#             # ALBUM NAME------------------------------
#             CTkLabel(
#                 card,
#                 text=name,
#                 font=("Arial", 13, "bold"),
#                 text_color="#c75b7a"
#             ).pack(pady=(0, 0), ipady=0)

#             # PHOTO COUNT------------------------------
#             count = get_album_photo_count(album_id)
#             CTkLabel(
#                 card,
#                 text=f"{count} photos",
#                 font=("Arial", 10),
#                 text_color="gray"
#             ).pack(pady=(0, 2), ipady=0)

#             # BUTTONS------------------------------
#             btn_frame = CTkFrame(card, fg_color="#ffffff", corner_radius=0)
#             btn_frame.pack(pady=(0, 15))

#             open_btn = CTkButton(
#                 btn_frame, 
#                 text="Open",
#                 width=50, height=22,
#                 corner_radius=10,
#                 fg_color="#ffb7ce",
#                 hover_color="#ffe7eb",
#                 text_color="#ffffff",
#                 font=("Arial", 9, "bold"),
#                 command=lambda aid=album_id, aname=name: self.open_album(aid, aname)
#             ).pack(side="left", padx=2)

#             rename_btn = CTkButton(
#                 btn_frame,
#                 text="Rename",
#                 width=55, height=22,
#                 corner_radius=10,
#                 fg_color="#ffd6dc",
#                 hover_color="#ffe7eb",
#                 text_color="#c75b7a",
#                 font=("Arial", 9, "bold"),
#                 command=lambda aid=album_id, aname=name: self.open_rename_dialog(aid, aname)
#             ).pack(side="left", padx=2)

#             delete_btn = CTkButton(
#                 btn_frame,
#                 text="Delete",
#                 width=55,
#                 height=22, corner_radius=10,
#                 fg_color="#ff8fa3",
#                 hover_color="#ffccd5",
#                 text_color="#ffffff",
#                 font=("Arial", 9, "bold"),
#                 command=lambda aid=album_id: self.confirm_delete(aid)
#             ).pack(side="left", padx=2)

#             # HOVER EFFECT------------------------------
#             def on_enter(e, c=card):
#                 c.configure(border_color="#ff8fa3")

#             def on_leave(e, c=card):
#                 c.configure(border_color="#ffb7ce")

#             card.bind("<Enter>", on_enter)
#             card.bind("<Leave>", on_leave)

#             col += 1

#             if col >= 9:
#                 col = 0
#                 row += 1

#     # OPEN ALBUM------------------------------
#     def open_album(self, album_id, album_name):

#         PhotoViewer(
#         self.frame,
#         album_id,
#         album_name,
#         self.user_id
#     )

#     # ADD ALBUM------------------------------
#     def open_add_dialog(self):

#         dialog = CTkToplevel(self.frame)
#         dialog.title("Create Album")
#         dialog.geometry("320x180")
#         dialog.resizable(False, False)
#         dialog.grab_set()

#         dialog.configure(fg_color="#ffd6dc")

#         CTkLabel(
#             dialog,
#             text="Create New Album",
#             font=("Arial", 18, "bold"),
#             text_color="#c75b7a"
#         ).pack(pady=(20, 10))

#         entry = CTkEntry(
#             dialog,
#             width=240,
#             height=35,
#             fg_color="#ffffff",
#             border_width=0,
#             corner_radius=15,
#             placeholder_text="Album name"
#         )

#         entry.pack()
#         entry.focus()

#         error_label = CTkLabel(
#             dialog,
#             text="",
#             text_color="#ff4d6d",
#             font=("Arial", 11)
#         )

#         error_label.pack(pady=(5, 0))

#         def confirm():
#             name = entry.get().strip()
#             if not name:
#                 error_label.configure(text="Album name cannot be empty.")
#                 return
#             add_album(name, user_id=self.user_id)
#             self.load_albums()
#             dialog.destroy()

#         CTkButton(
#             dialog,
#             text="Create Album",
#             width=180,
#             height=35,
#             fg_color="#ffb7ce",
#             hover_color="#ffe7eb",
#             text_color="#ffffff",
#             corner_radius=15,
#             font=("Arial", 12, "bold"),
#             command=confirm
#         ).pack(pady=18)

#         dialog.bind("<Return>", lambda e: confirm())

#     # RENAME ALBUM------------------------------
#     def open_rename_dialog(self, album_id, old_name):

#         dialog = CTkToplevel(self.frame)
#         dialog.title("Rename Album")
#         dialog.geometry("320x180")
#         dialog.resizable(False, False)
#         dialog.grab_set()

#         dialog.configure(fg_color="#ffd6dc")

#         CTkLabel(
#             dialog,
#             text="Rename Album",
#             font=("Arial", 18, "bold"),
#             text_color="#c75b7a"
#         ).pack(pady=(20, 10))

#         entry = CTkEntry(
#             dialog,
#             width=240,
#             height=35,
#             fg_color="#ffffff",
#             border_width=0,
#             corner_radius=15
#         )

#         entry.insert(0, old_name)
#         entry.pack()
#         entry.focus()

#         def confirm():

#             new_name = entry.get().strip()

#             if new_name:
#                 rename_album(album_id, new_name)
#                 self.load_albums()
#                 dialog.destroy()

#         CTkButton(
#             dialog,
#             text="Save Changes",
#             width=180,
#             height=35,
#             fg_color="#ffb7ce",
#             hover_color="#ffe7eb",
#             text_color="#ffffff",
#             corner_radius=15,
#             font=("Arial", 12, "bold"),
#             command=confirm
#         ).pack(pady=18)

#         dialog.bind("<Return>", lambda e: confirm())

#     # DELETE ALBUM------------------------------
#     def confirm_delete(self, album_id):

#         dialog = CTkToplevel(self.frame)
#         dialog.title("Delete Album")
#         dialog.geometry("300x170")
#         dialog.resizable(False, False)
#         dialog.grab_set()

#         dialog.configure(fg_color="#ffd6dc")

#         CTkLabel(
#             dialog,
#             text="Delete this album?",
#             font=("Arial", 17, "bold"),
#             text_color="#c75b7a"
#         ).pack(pady=(25, 10))

#         CTkLabel(
#             dialog,
#             text="Photos will remain. \nOnly the album will be deleted.",
#             font=("Arial", 12),
#             text_color="gray"
#         ).pack()

#         btn_frame = CTkFrame(
#             dialog,
#             fg_color="transparent"
#         )

#         btn_frame.pack(pady=20)

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
#             delete_album(album_id)
#             self.load_albums()
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

#     # SHOW PAGE------------------------------
#     def show(self):

#         self.on_toggle(True)

#         self.header_frame.pack(
#             fill="x",
#             padx=10,
#             pady=(10, 5)
#         )

#         self.titlebar.pack(
#             side="left"
#         )

#         self.add_btn.pack(
#             side="right"
#         )

#         self.search_entry.pack(
#             fill="x",
#             padx=10,
#             pady=(0, 10)
#         )

#         self.folders_frame.pack(
#             fill="both",
#             expand=True,
#             padx=10,
#             pady=(0, 10)
#         )

#         self.load_albums()

#     # HIDE PAGE--
#     def hide(self):

#         self.on_toggle(False)

#         self.header_frame.pack_forget()
#         self.search_entry.pack_forget()
#         self.folders_frame.pack_forget()

from customtkinter import *
from database import (
    get_albums,
    add_album,
    delete_album,
    rename_album,
    get_album_photo_count
)
from PhotoViewer import PhotoViewer

class AlbumPage:
    def __init__(self, Frame, on_toggle, on_open_album=None, user_id=None):
        self.frame = Frame
        self.on_toggle = on_toggle
        self.on_open_album = on_open_album
        self.user_id = user_id

        # HEADER---------------------------------
        self.header_frame = CTkFrame(Frame, fg_color="transparent")

        self.titlebar = CTkLabel(
            self.header_frame,
            text="Albums",
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
            text="Total Albums: 0",
            font=("Arial", 13, "bold"),
            text_color="#c75b7a"
        )

        self.add_btn = CTkButton(
            self.header_frame,
            text="+ New Album",
            width=130,
            height=35,
            fg_color="#ffb7ce",
            hover_color="#ffe7eb",
            corner_radius=15,
            font=("Arial", 12, "bold"),
            text_color="#ffffff",
            command=self.open_add_dialog
        )

        # SEARCH BAR------------------------------
        self.search_entry = CTkEntry(
            Frame,
            placeholder_text="Search albums...",
            height=35,
            corner_radius=15,
            fg_color="#ffe7eb",
            border_width=0,
            text_color="#000000",
            placeholder_text_color="gray",
            font=("Arial", 12)
        )

        self.search_entry.bind("<KeyRelease>", lambda e: self.load_albums())

        # ALBUM GRID------------------------------
        self.folders_frame = CTkScrollableFrame(
            Frame,
            fg_color="transparent"
        )

    # LOAD ALBUMS----------------------------------
    def load_albums(self):

        for widget in self.folders_frame.winfo_children():
            widget.destroy()

        search_text = self.search_entry.get().lower().strip()

        albums = get_albums(user_id=self.user_id)

        filtered = []

        for album in albums:
            album_id, name = album

            if search_text in name.lower():
                filtered.append(album)

        # ✅ UPDATE TOTAL COUNT (ADDED)
        total_albums = len(filtered)
        self.total_label.configure(text=f"Total Albums: {total_albums}")

        if not filtered:
            CTkLabel(
                self.folders_frame,
                text="No albums found 🌸",
                text_color="gray",
                font=("Arial", 15)
            ).pack(pady=50)
            return

        row = 0
        col = 0

        for album_id, name in filtered:

            card = CTkFrame(
                self.folders_frame,
                width=500,
                height=500,
                fg_color="#ffffff",
                corner_radius=20,
                border_width=2,
                border_color="#ffe7eb"
            )

            card.grid(row=row, column=col, padx=8, pady=8, sticky="n")
            card.grid_propagate(True)

            cover = CTkFrame(
                card,
                width=155,
                height=80,
                fg_color="#ffd6dc",
                corner_radius=12
            )
            cover.pack(pady=(10, 0))
            cover.pack_propagate(False)

            CTkLabel(
                cover,
                text="📁",
                font=("Arial", 30)
            ).pack(expand=True)

            CTkLabel(
                card,
                text=name,
                font=("Arial", 13, "bold"),
                text_color="#c75b7a"
            ).pack()

            count = get_album_photo_count(album_id)
            CTkLabel(
                card,
                text=f"{count} photos",
                font=("Arial", 10),
                text_color="gray"
            ).pack(pady=(0, 2))

            btn_frame = CTkFrame(card, fg_color="#ffffff", corner_radius=0)
            btn_frame.pack(pady=(0, 15))

            CTkButton(
                btn_frame,
                text="Open",
                width=50, height=22,
                corner_radius=10,
                fg_color="#ffb7ce",
                hover_color="#ffe7eb",
                text_color="#ffffff",
                font=("Arial", 9, "bold"),
                command=lambda aid=album_id, aname=name: self.open_album(aid, aname)
            ).pack(side="left", padx=2)

            CTkButton(
                btn_frame,
                text="Rename",
                width=55, height=22,
                corner_radius=10,
                fg_color="#ffd6dc",
                hover_color="#ffe7eb",
                text_color="#c75b7a",
                font=("Arial", 9, "bold"),
                command=lambda aid=album_id, aname=name: self.open_rename_dialog(aid, aname)
            ).pack(side="left", padx=2)

            CTkButton(
                btn_frame,
                text="Delete",
                width=55,
                height=22,
                corner_radius=10,
                fg_color="#ff8fa3",
                hover_color="#ffccd5",
                text_color="#ffffff",
                font=("Arial", 9, "bold"),
                command=lambda aid=album_id: self.confirm_delete(aid)
            ).pack(side="left", padx=2)

            def on_enter(e, c=card):
                c.configure(border_color="#ff8fa3")

            def on_leave(e, c=card):
                c.configure(border_color="#ffb7ce")

            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

            col += 1
            if col >= 9:
                col = 0
                row += 1

    # OPEN ALBUM------------------------------
    def open_album(self, album_id, album_name):
        PhotoViewer(self.frame, album_id, album_name, self.user_id)

    # ADD ALBUM------------------------------
    def open_add_dialog(self):
        dialog = CTkToplevel(self.frame)
        dialog.title("Create Album")
        dialog.geometry("320x180")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(fg_color="#ffd6dc")

        CTkLabel(
            dialog,
            text="Create New Album",
            font=("Arial", 18, "bold"),
            text_color="#c75b7a"
        ).pack(pady=(20, 10))

        entry = CTkEntry(dialog, width=240, height=35, fg_color="#ffffff")
        entry.pack()
        entry.focus()

        error_label = CTkLabel(dialog, text="", text_color="#ff4d6d")
        error_label.pack()

        def confirm():
            name = entry.get().strip()
            if not name:
                error_label.configure(text="Album name cannot be empty.")
                return
            add_album(name, user_id=self.user_id)
            self.load_albums()
            dialog.destroy()

        CTkButton(
            dialog,
            text="Create Album",
            command=confirm
        ).pack(pady=18)

    # RENAME ALBUM / DELETE ALBUM (UNCHANGED BELOW THIS POINT)
    def open_rename_dialog(self, album_id, old_name):
        dialog = CTkToplevel(self.frame)
        dialog.title("Rename Album")
        dialog.geometry("320x180")
        dialog.grab_set()
        dialog.configure(fg_color="#ffd6dc")

        entry = CTkEntry(dialog, width=240, height=35)
        entry.insert(0, old_name)
        entry.pack()
        entry.focus()

        def confirm():
            new_name = entry.get().strip()
            if new_name:
                rename_album(album_id, new_name)
                self.load_albums()
                dialog.destroy()

        CTkButton(dialog, text="Save Changes", command=confirm).pack(pady=18)

    def confirm_delete(self, album_id):
        dialog = CTkToplevel(self.frame)
        dialog.title("Delete Album")
        dialog.geometry("300x170")
        dialog.grab_set()
        dialog.configure(fg_color="#ffd6dc")

        CTkLabel(dialog, text="Delete this album?").pack(pady=20)

        def delete_now():
            delete_album(album_id)
            self.load_albums()
            dialog.destroy()

        CTkButton(dialog, text="Delete", command=delete_now).pack()
    
    # SHOW PAGE------------------------------
    def show(self):

        self.on_toggle(True)

        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.titlebar.pack(side="left")

        # ✅ TOTAL LABEL
        self.total_label.pack(side="left", padx=15)

        self.add_btn.pack(side="right")

        self.search_entry.pack(fill="x", padx=10, pady=(0, 10))

        self.folders_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.load_albums()

    # HIDE PAGE------------------------------
    def hide(self):
        self.on_toggle(False)
        self.header_frame.pack_forget()
        self.search_entry.pack_forget()
        self.folders_frame.pack_forget()
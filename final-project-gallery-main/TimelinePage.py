# from customtkinter import *
# from PIL import Image
# import os
# from datetime import datetime
# from database import get_photos

# from database import (
#     add_photo,
#     get_photos_by_album,
#     delete_photo
# )
# class TimelinePage:
#     def __init__(self, frame, on_toggle, user_id):
#         self.frame = frame
#         self.on_toggle = on_toggle
#         self.user_id = user_id
#         self.images = [] 
#         self.selected = set()

#         # HEADER------------------------------
#         self.header_frame = CTkFrame(frame, fg_color="transparent")

#         self.titlebar = CTkLabel(
#             self.header_frame,
#             text="Timeline",
#             width=300,
#             height=35,
#             fg_color="#ffb7ce",
#             corner_radius=15,
#             font=("Arial", 18, "bold"),
#             text_color="#ffffff"
#         )

#         # ADD PHOTO BUTTON ------------------------------
#         self.add_btn = CTkButton(
#             self.header_frame,
#             text="+ Add Photos",
#             width=130,
#             height=35,
#             fg_color="#ffb7ce",
#             hover_color="#ffe7eb",
#             corner_radius=15,
#             font=("Arial", 12, "bold"),
#             text_color="#ffffff",
#             command=self.import_photos
#         )

#         # DELETE SELECTED BUTTON------------------------------ 
#         self.delete_btn = CTkButton(
#             self.header_frame,
#             text="🗑 Delete Selected",
#             width=140,
#             height=35,
#             fg_color="#ff8fa3",
#             hover_color="#ffccd5",
#             corner_radius=15,
#             font=("Arial", 12, "bold"),
#             text_color="#ffffff",
#             command=self.delete_selected
#         )

#         # SCROLLABLE CONTENT------------------------------
#         self.scroll_frame = CTkScrollableFrame(
#             frame,
#             fg_color="#ffffff",
#             corner_radius=25
#         )

#     # LOAD----------------------------------------------
#     def load_timeline(self):
#         photos = get_photos(user_id=self.user_id)
#         for widget in self.scroll_frame.winfo_children():
#             widget.destroy()
#         self.images.clear()
#         self.selected.clear()

#         if not photos:
#             CTkLabel(
#                 self.scroll_frame,
#                 text="No photos yet 🌸",
#                 text_color="gray",
#                 font=("Arial", 16)
#             ).pack(pady=60)
#             return

#         # GROUP BY DATE------------------------------
#         groups = {}   # "May 16, 2026" -> [photo tuples]
#         for photo in photos:
#             # photo = (id, filename, filepath, title, album_id, is_favorite, thumbnail_path, uploaded_at)
#             uploaded_at = photo[7]
#             try:
#                 dt = datetime.strptime(uploaded_at[:10], "%Y-%m-%d")
#                 label = dt.strftime("%B %d, %Y")
#             except Exception:
#                 label = "Unknown Date"

#             if label not in groups:
#                 groups[label] = []
#             groups[label].append(photo)

#         # RENDER EACH GROUP------------------------------
#         for date_label, group_photos in groups.items():
#             self._render_group(date_label, group_photos)

#     # RENDER ONE DATE GROUP------------------------------
#     def _render_group(self, date_label, group_photos):

#         # DATE HEADER------------------------------
#         header = CTkFrame(self.scroll_frame, fg_color="transparent")
#         header.pack(fill="x", padx=15, pady=(18, 4))

#         CTkLabel(
#             header,
#             text=date_label,
#             font=("Arial", 15, "bold"),
#             text_color="#c75b7a"
#         ).pack(side="left")

#         # DIVIDER LINE------------------------------
#         divider = CTkFrame(
#             self.scroll_frame,
#             height=1,
#             fg_color="#ffd6dc"
#         )
#         divider.pack(fill="x", padx=15, pady=(0, 8))

#         # PHOTO GRID------------------------------
#         COLS = 8
#         THUMB = 160
#         col = 0
#         row = 0

#         grid = CTkFrame(self.scroll_frame, fg_color="transparent")
#         grid.pack(anchor="center", padx=10, pady=(0, 8))

#         for photo in group_photos:
#             photo_id  = photo[0]
#             filename  = photo[1]
#             filepath  = photo[2]

#             if not os.path.exists(filepath):
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
#                 height=THUMB + 20,
#                 fg_color="#ffe7eb",
#                 corner_radius=16
#             )
#             card.grid(row=row, column=col, padx=10, pady=10)
#             card.grid_propagate(False)

#             # IMAGE BUTTON------------------------------
#             img_btn = CTkButton(
#                 card,
#                 image=ctk_img,
#                 text="",
#                 width=THUMB,
#                 height=THUMB,
#                 fg_color="transparent",
#                 hover_color="#ffd6dc",
#                 corner_radius=10,
#             )
#             img_btn.pack(expand=True)
#             img_btn.bind("<Button-1>", lambda e, p=filepath: self.open_fullscreen(p))

#             # HOVER CHECKBOX------------------------------
#             check_var = IntVar(value=1 if photo_id in self.selected else 0)

#             checkbox = CTkCheckBox(
#                 card,
#                 text="",
#                 width=24,
#                 height=24,
#                 variable=check_var,
#                 fg_color="#ffb7ce",
#                 hover_color="#ff8fa3",
#                 border_color="#ffffff",
#                 corner_radius=6,
#                 command=lambda pid=photo_id, v=check_var: self._toggle_select(pid, v)
#             )

#             checkbox.bind("<Button-1>", lambda e: e.widget.focus_set())

#             # show checkbox on hover------------------------------
#             def on_enter(e, cb=checkbox):
#                 cb.place(x=8, y=8)

#             def on_leave(e, cb=checkbox, pid=photo_id):
#                 if pid not in self.selected:
#                     cb.place_forget()

#             card.bind("<Enter>", on_enter)
#             card.bind("<Leave>", on_leave)
#             img_btn.bind("<Enter>", on_enter)
#             img_btn.bind("<Leave>", on_leave)

#             if photo_id in self.selected:
#                 checkbox.place(x=8, y=8)

#             col += 1
#             if col >= COLS:
#                 col = 0
#                 row += 1

#         for c in range(COLS):
#             grid.grid_columnconfigure(c, weight=1)

#     # SELECT / DESELECT------------------------------
#     def _toggle_select(self, photo_id, var):
#         if var.get():
#             self.selected.add(photo_id)
#         else:
#             self.selected.discard(photo_id)

#     # FULLSCREEN VIEWER------------------------------
#     def open_fullscreen(self, filepath):
#         viewer = CTkToplevel(self.frame)
#         viewer.geometry("1000x700")
#         viewer.title("Photo Viewer")
#         viewer.configure(fg_color="#1a1a1a")
#         viewer.grab_set()

#         try:
#             img = Image.open(filepath)
#             w, h = img.size
#             scale = min(950 / w, 650 / h)
#             new_size = (int(w * scale), int(h * scale))
#             img = img.resize(new_size, Image.LANCZOS)

#             ctk_img = CTkImage(light_image=img, dark_image=img, size=new_size)

#             lbl = CTkLabel(viewer, image=ctk_img, text="")
#             lbl.image = ctk_img
#             lbl.pack(expand=True)
#         except Exception as e:
#             CTkLabel(viewer, text=f"Could not open image.\n{e}",
#                      text_color="gray").pack(expand=True)

#         # close on Escape------------------------------
#         viewer.bind("<Escape>", lambda e: viewer.destroy())

#     # SHOW / HIDE----------------------------------------------
#     def show(self):
#         self.on_toggle(True)
#         self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
#         self.titlebar.pack(side="left")
#         self.add_btn.pack(side="right")
#         self.delete_btn.pack(side="right", padx=(0, 5))
#         self.scroll_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
#         self.load_timeline()

#     def hide(self):
#         self.on_toggle(False)
#         self.header_frame.pack_forget()
#         self.delete_btn.pack_forget()
#         self.add_btn.pack_forget()
#         self.scroll_frame.pack_forget()

#     # DELETE SELECTED------------------------------
#     def delete_selected(self):
#         from database import delete_photo

#         if not self.selected:
#             return

#         dialog = CTkToplevel(self.frame)
#         dialog.title("Delete Photos")
#         dialog.geometry("300x160")
#         dialog.resizable(False, False)
#         dialog.grab_set()
#         dialog.configure(fg_color="#ffd6dc")

#         CTkLabel(
#             dialog,
#             text=f"Delete {len(self.selected)} photo(s)?",
#             font=("Arial", 14, "bold"),
#             text_color="#c75b7a"
#         ).pack(pady=(20, 6))

#         CTkLabel(
#             dialog,
#             text="They will be moved to trash.",
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

#         def confirm():
#             for photo_id in list(self.selected):
#                 delete_photo(photo_id)
#             self.selected.clear()
#             self.load_timeline()
#             dialog.destroy()

#         CTkButton(
#             btn_frame,
#             text="Delete",
#             width=90,
#             fg_color="#ff8fa3",
#             hover_color="#ffccd5",
#             text_color="#ffffff",
#             command=confirm
#         ).pack(side="left", padx=5)

#     # IMPORT PHOTOS------------------------------
#     def import_photos(self):
#         from tkinter import filedialog
#         import shutil
#         from database import add_photo

#         filepaths = filedialog.askopenfilenames(
#             title="Select Photos",
#             filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")]
#         )

#         if not filepaths:
#             return

#         base_dir = os.path.dirname(os.path.abspath(__file__))
#         photos_dir = os.path.join(base_dir, "photos")
#         os.makedirs(photos_dir, exist_ok=True)

#         for filepath in filepaths:
#             filename = os.path.basename(filepath)
#             name, ext = os.path.splitext(filename)
#             destination = os.path.join(photos_dir, filename)

#             counter = 1
#             while os.path.exists(destination):
#                 destination = os.path.join(photos_dir, f"{name}_{counter}{ext}")
#                 counter += 1

#             filename = os.path.basename(destination)
#             shutil.copy(filepath, destination)
#             add_photo(
#                 filename=filename,
#                 filepath=destination,
#                 album_id=None,
#                 user_id=self.user_id
#             )

#         self.load_timeline()

from customtkinter import *
from PIL import Image
import os
from datetime import datetime
from database import get_photos

from database import (
    add_photo,
    get_photos_by_album,
    delete_photo
)

class TimelinePage:
    def __init__(self, frame, on_toggle, user_id):
        self.frame = frame
        self.on_toggle = on_toggle
        self.user_id = user_id
        self.images = [] 
        self.selected = set()

        # HEADER------------------------------
        self.header_frame = CTkFrame(frame, fg_color="transparent")

        self.titlebar = CTkLabel(
            self.header_frame,
            text="Timeline",
            width=300,
            height=35,
            fg_color="#ffb7ce",
            corner_radius=15,
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )

        # TOTAL PHOTOS LABEL ------------------------------
        self.total_label = CTkLabel(
            self.header_frame,
            text="Total Photos: 0",
            font=("Arial", 13, "bold"),
            text_color="#c75b7a"
        )

        # ADD PHOTO BUTTON ------------------------------
        self.add_btn = CTkButton(
            self.header_frame,
            text="+ Add Photos",
            width=130,
            height=35,
            fg_color="#ffb7ce",
            hover_color="#ffe7eb",
            corner_radius=15,
            font=("Arial", 12, "bold"),
            text_color="#ffffff",
            command=self.import_photos
        )

        # DELETE SELECTED BUTTON------------------------------ 
        self.delete_btn = CTkButton(
            self.header_frame,
            text="🗑 Delete Selected",
            width=140,
            height=35,
            fg_color="#ff8fa3",
            hover_color="#ffccd5",
            corner_radius=15,
            font=("Arial", 12, "bold"),
            text_color="#ffffff",
            command=self.delete_selected
        )

        # SCROLLABLE CONTENT------------------------------
        self.scroll_frame = CTkScrollableFrame(
            frame,
            fg_color="#ffffff",
            corner_radius=25
        )

    # LOAD----------------------------------------------
    def load_timeline(self):
        photos = get_photos(user_id=self.user_id)

        # UPDATE TOTAL COUNT ------------------------------
        total = len(photos)
        self.total_label.configure(text=f"Total Photos: {total}")

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.images.clear()
        self.selected.clear()

        if not photos:
            CTkLabel(
                self.scroll_frame,
                text="No photos yet 🌸",
                text_color="gray",
                font=("Arial", 16)
            ).pack(pady=60)
            return

        # GROUP BY DATE------------------------------
        groups = {}

        for photo in photos:
            uploaded_at = photo[7]

            try:
                dt = datetime.strptime(uploaded_at[:10], "%Y-%m-%d")
                label = dt.strftime("%B %d, %Y")
            except Exception:
                label = "Unknown Date"

            if label not in groups:
                groups[label] = []

            groups[label].append(photo)

        # RENDER EACH GROUP------------------------------
        for date_label, group_photos in groups.items():
            self._render_group(date_label, group_photos)

    # RENDER ONE DATE GROUP------------------------------
    def _render_group(self, date_label, group_photos):

        # DATE HEADER------------------------------
        header = CTkFrame(self.scroll_frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(18, 4))

        CTkLabel(
            header,
            text=date_label,
            font=("Arial", 15, "bold"),
            text_color="#c75b7a"
        ).pack(side="left")

        # DIVIDER LINE------------------------------
        divider = CTkFrame(
            self.scroll_frame,
            height=1,
            fg_color="#ffd6dc"
        )
        divider.pack(fill="x", padx=15, pady=(0, 8))

        # PHOTO GRID------------------------------
        COLS = 8
        THUMB = 160
        col = 0
        row = 0

        grid = CTkFrame(self.scroll_frame, fg_color="transparent")
        grid.pack(anchor="center", padx=10, pady=(0, 8))

        for photo in group_photos:
            photo_id  = photo[0]
            filename  = photo[1]
            filepath  = photo[2]

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
                height=THUMB + 20,
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
                corner_radius=10,
            )

            img_btn.pack(expand=True)
            img_btn.bind("<Button-1>", lambda e, p=filepath: self.open_fullscreen(p))

            # HOVER CHECKBOX------------------------------
            check_var = IntVar(value=1 if photo_id in self.selected else 0)

            checkbox = CTkCheckBox(
                card,
                text="",
                width=24,
                height=24,
                variable=check_var,
                fg_color="#ffb7ce",
                hover_color="#ff8fa3",
                border_color="#ffffff",
                corner_radius=6,
                command=lambda pid=photo_id, v=check_var: self._toggle_select(pid, v)
            )

            checkbox.bind("<Button-1>", lambda e: e.widget.focus_set())

            # show checkbox on hover------------------------------
            def on_enter(e, cb=checkbox):
                cb.place(x=8, y=8)

            def on_leave(e, cb=checkbox, pid=photo_id):
                if pid not in self.selected:
                    cb.place_forget()

            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

            img_btn.bind("<Enter>", on_enter)
            img_btn.bind("<Leave>", on_leave)

            if photo_id in self.selected:
                checkbox.place(x=8, y=8)

            col += 1

            if col >= COLS:
                col = 0
                row += 1

        for c in range(COLS):
            grid.grid_columnconfigure(c, weight=1)

    # SELECT / DESELECT------------------------------
    def _toggle_select(self, photo_id, var):
        if var.get():
            self.selected.add(photo_id)
        else:
            self.selected.discard(photo_id)

    # FULLSCREEN VIEWER------------------------------
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

    # SHOW / HIDE----------------------------------------------
    def show(self):
        self.on_toggle(True)

        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))

        self.titlebar.pack(side="left")
        self.total_label.pack(side="left", padx=15)

        self.add_btn.pack(side="right")
        self.delete_btn.pack(side="right", padx=(0, 5))

        self.scroll_frame.pack(
            side="top",
            fill="both",
            expand=True,
            padx=10,
            pady=(5, 10)
        )

        self.load_timeline()

    def hide(self):
        self.on_toggle(False)

        self.header_frame.pack_forget()
        self.delete_btn.pack_forget()
        self.add_btn.pack_forget()
        self.scroll_frame.pack_forget()

    # DELETE SELECTED------------------------------
    def delete_selected(self):
        from database import delete_photo

        if not self.selected:
            return

        dialog = CTkToplevel(self.frame)
        dialog.title("Delete Photos")
        dialog.geometry("300x160")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(fg_color="#ffd6dc")

        CTkLabel(
            dialog,
            text=f"Delete {len(self.selected)} photo(s)?",
            font=("Arial", 14, "bold"),
            text_color="#c75b7a"
        ).pack(pady=(20, 6))

        CTkLabel(
            dialog,
            text="They will be moved to trash.",
            font=("Arial", 11),
            text_color="gray"
        ).pack()

        btn_frame = CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=16)

        CTkButton(
            btn_frame,
            text="Cancel",
            width=90,
            fg_color="#ffffff",
            hover_color="#ffe7eb",
            text_color="#c75b7a",
            command=dialog.destroy
        ).pack(side="left", padx=5)

        def confirm():
            for photo_id in list(self.selected):
                delete_photo(photo_id)

            self.selected.clear()
            self.load_timeline()
            dialog.destroy()

        CTkButton(
            btn_frame,
            text="Delete",
            width=90,
            fg_color="#ff8fa3",
            hover_color="#ffccd5",
            text_color="#ffffff",
            command=confirm
        ).pack(side="left", padx=5)

    # IMPORT PHOTOS------------------------------
    def import_photos(self):
        from tkinter import filedialog
        import shutil
        from database import add_photo

        filepaths = filedialog.askopenfilenames(
            title="Select Photos",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")]
        )

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
                destination = os.path.join(
                    photos_dir,
                    f"{name}_{counter}{ext}"
                )
                counter += 1

            filename = os.path.basename(destination)

            shutil.copy(filepath, destination)

            add_photo(
                filename=filename,
                filepath=destination,
                album_id=None,
                user_id=self.user_id
            )

        self.load_timeline()
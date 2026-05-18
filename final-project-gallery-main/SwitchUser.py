from customtkinter import *
from database import get_all_users, validate_user
import hashlib


class SwitchUserDialog:
    def __init__(self, parent, current_user_id, on_switch):
        self.parent = parent
        self.current_user_id = current_user_id
        self.on_switch = on_switch

        self.dialog = CTkToplevel(parent)
        self.dialog.title("Switch User")
        self.dialog.geometry("500x580")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.configure(fg_color="#ffd6dc")

        # HEADER------------------------------
        CTkLabel(
            self.dialog,
            text="Switch User",
            font=("Arial", 20, "bold"),
            text_color="#c75b7a"
        ).pack(pady=(30, 5))

        CTkLabel(
            self.dialog,
            text="Select a profile to switch to",
            font=("Arial", 12),
            text_color="gray"
        ).pack(pady=(0, 20))

        # USER LIST------------------------------
        self.user_frame = CTkScrollableFrame(
            self.dialog,
            fg_color="transparent",
            height=200
        )
        self.user_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.selected_user_id = None
        self.selected_username = None

        self.load_users()

        # ADD NEW ACCOUNT BUTTON------------------------------
        CTkButton(
            self.dialog,
            text="+ Add New Account",
            width=280,
            height=38,
            corner_radius=12,
            fg_color="#ffe7eb",
            hover_color="#ffd6dc",
            text_color="#c75b7a",
            font=("Arial", 12, "bold"),
            command=self.open_register
        ).pack(pady=(0, 10))


        # DIVIDER------------------------------
        CTkFrame(
            self.dialog,
            height=1,
            fg_color="#ffb7ce"
        ).pack(fill="x", padx=20, pady=(0, 15))

        # PASSWORD SECTION------------------------------
        CTkLabel(
            self.dialog,
            text="Enter password to confirm:",
            font=("Arial", 12),
            text_color="#c75b7a"
        ).pack(padx=20, anchor="w")

        self.password_entry = CTkEntry(
            self.dialog,
            placeholder_text="Password",
            width=280,
            height=38,
            corner_radius=15,
            fg_color="#ffe7eb",
            border_width=0,
            text_color="#000000",
            font=("Arial", 13),
            show="*"
        )
        self.password_entry.pack(pady=(5, 5))

        self.error_label = CTkLabel(
            self.dialog,
            text="",
            text_color="#c0392b",
            font=("Arial", 11)
        )
        self.error_label.pack()

        # SWITCH BUTTON------------------------------
        CTkButton(
            self.dialog,
            text="Switch",
            width=280,
            height=38,
            corner_radius=15,
            fg_color="#ffb7ce",
            hover_color="#ffe7eb",
            text_color="#ffffff",
            font=("Arial", 13, "bold"),
            command=self.confirm_switch
        ).pack(pady=(5, 20))

        self.dialog.bind("<Return>", lambda e: self.confirm_switch())

    # LOAD USERS--------------------------------------------------------------------------------
    def load_users(self):
        for widget in self.user_frame.winfo_children():
            widget.destroy()

        users = get_all_users()

        for user_id, username in users:
            is_current = user_id == self.current_user_id

            # ROW FRAME---------------------------------
            row = CTkFrame(self.user_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)

            # USER BUTTON------------------------------
            CTkButton(
                row,
                text=f"👤 {username}" + (" (current)" if is_current else ""),
                width=210,
                height=40,
                corner_radius=12,
                fg_color="#ffb7ce" if is_current else "#ffe7eb",
                hover_color="#ffd6dc",
                text_color="#c75b7a",
                font=("Arial", 12, "bold"),
                command=lambda uid=user_id, uname=username: self.select_user(uid, uname)
            ).pack(side="left", padx=(0, 5))

            # DELETE BUTTON------------------------------
            CTkButton(
                row,
                text="🗑",
                width=40,
                height=40,
                corner_radius=12,
                fg_color="#ff8fa3",
                hover_color="#ffccd5",
                text_color="#ffffff",
                font=("Arial", 14),
                command=lambda uid=user_id, uname=username: self.confirm_delete_account(uid, uname)
            ).pack(side="left")

    # DELETE ACCOUNT-------------------------------------------------------------------------------------
    def confirm_delete_account(self, user_id, username):
        if user_id == self.current_user_id:
            self.error_label.configure(
                text="Cannot delete current account.",
                text_color="#c0392b"
            )
            return

        dialog = CTkToplevel(self.dialog)
        dialog.title("Delete Account")
        dialog.geometry("300x180")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(fg_color="#ffd6dc")

        CTkLabel(
            dialog,
            text=f"Delete '{username}'?",
            font=("Arial", 14, "bold"),
            text_color="#c75b7a"
        ).pack(pady=(25, 6))

        CTkLabel(
            dialog,
            text="All their photos and albums\nwill be permanently deleted.",
            font=("Arial", 11),
            text_color="gray",
            justify="center"
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

        def delete_now():
            from database import delete_user
            delete_user(user_id)
            self.load_users()
            dialog.destroy()
            self.error_label.configure(
                text=f"Account '{username}' deleted.",
                text_color="#27ae60"
            )

        CTkButton(
            btn_frame,
            text="Delete",
            width=90,
            fg_color="#ff8fa3",
            hover_color="#ffccd5",
            text_color="#ffffff",
            command=delete_now
        ).pack(side="left", padx=5)

    # REGISTER NEW ACCOUNT------------------------------
    def open_register(self):
        reg = CTkToplevel(self.dialog)
        reg.title("Create Account")
        reg.geometry("380x420+400+200")
        reg.resizable(False, False)
        reg.grab_set()
        reg.configure(fg_color="#ffd6dc")

        CTkLabel(reg, text="🌸 Create Account", font=("Arial", 20, "bold"),
                text_color="#c75b7a").pack(pady=(40, 5))
        CTkLabel(reg, text="Fill in your details", font=("Arial", 12),
                text_color="gray").pack(pady=(0, 25))

        new_user = CTkEntry(reg, placeholder_text="Username", width=260, height=38,
                            corner_radius=15, fg_color="#ffe7eb", border_width=0,
                            text_color="#000000", font=("Arial", 13))
        new_user.pack(pady=6)
        new_user.focus()

        new_pass = CTkEntry(reg, placeholder_text="Password", width=260, height=38,
                            corner_radius=15, fg_color="#ffe7eb", border_width=0,
                            text_color="#000000", font=("Arial", 13), show="*")
        new_pass.pack(pady=6)

        confirm_pass = CTkEntry(reg, placeholder_text="Confirm Password", width=260, height=38,
                                corner_radius=15, fg_color="#ffe7eb", border_width=0,
                                text_color="#000000", font=("Arial", 13), show="*")
        confirm_pass.pack(pady=6)

        error = CTkLabel(reg, text="", text_color="#c0392b", font=("Arial", 11))
        error.pack(pady=(4, 0))

        def confirm():
            from database import register_user
            username = new_user.get().strip()
            password = new_pass.get()
            confirmed = confirm_pass.get()

            if not username or not password:
                error.configure(text="Please fill in all fields.")
                return
            if password != confirmed:
                error.configure(text="Passwords do not match.")
                return
            if len(password) < 6:
                error.configure(text="Password must be at least 6 characters.")
                return

            success = register_user(username, password)
            if success:
                reg.destroy()
                self.load_users()
                self.error_label.configure(
                    text=f"Account created!",
                    text_color="#27ae60"
                )
            else:
                error.configure(text="Username already exists.")

        CTkButton(reg, text="Create Account", width=260, height=38, corner_radius=15,
                fg_color="#ffb7ce", hover_color="#ffe7eb", text_color="#ffffff",
                font=("Arial", 13, "bold"), command=confirm).pack(pady=16)

        reg.bind("<Return>", lambda e: confirm())

    # SELECT USER------------------------------
    def select_user(self, user_id, username):
        self.selected_user_id = user_id
        self.selected_username = username
        self.error_label.configure(text=f"Selected: {username}", text_color="#27ae60")
        self.password_entry.focus()

    # CONFIRM SWITCH------------------------------
    def confirm_switch(self):
        if not self.selected_user_id:
            self.error_label.configure(text="Please select a user first.", text_color="#c0392b")
            return

        if self.selected_user_id == self.current_user_id:
            self.error_label.configure(text="You're already on this account.", text_color="#c0392b")
            return

        password = self.password_entry.get()
        if not password:
            self.error_label.configure(text="Please enter a password.", text_color="#c0392b")
            return

        user_id = validate_user(self.selected_username, password)
        if user_id:
            self.dialog.destroy()
            self.on_switch(user_id)
        else:
            self.error_label.configure(text="Incorrect password.", text_color="#c0392b")
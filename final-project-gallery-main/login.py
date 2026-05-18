from customtkinter import *
from database import validate_user, register_user


class LoginWindow:
    def __init__(self):
        self.app = CTk()
        self.app.title("wiileen's gallery - Login")
        self.app.geometry("380x420+400+200")
        self.app.resizable(False, False)

        frame = CTkFrame(self.app, fg_color="#ffd6dc", corner_radius=0)
        frame.pack(fill="both", expand=True)

        CTkLabel(frame, text="🌸 wiileen's gallery", font=("Arial", 20, "bold"), text_color="#c75b7a").pack(pady=(40, 5))
        CTkLabel(frame, text="Sign in to continue", font=("Arial", 12), text_color="gray").pack(pady=(0, 25))

        self.username = CTkEntry(frame, placeholder_text="Username", width=260, height=38,
                                 corner_radius=15, fg_color="#ffe7eb", border_width=0,
                                 text_color="#000000", font=("Arial", 13))
        self.username.pack(pady=6)

        self.password = CTkEntry(frame, placeholder_text="Password", width=260, height=38,
                                 corner_radius=15, fg_color="#ffe7eb", border_width=0,
                                 text_color="#000000", font=("Arial", 13), show="*")
        self.password.pack(pady=6)

        self.error_label = CTkLabel(frame, text="", text_color="#c0392b", font=("Arial", 11))
        self.error_label.pack(pady=(4, 0))

        CTkButton(frame, text="Login", width=260, height=38, corner_radius=15,
                  fg_color="#ffb7ce", hover_color="#ffe7eb", text_color="#ffffff",
                  font=("Arial", 13, "bold"), command=self.login).pack(pady=(12, 4))
        
        # SIGN UP BUTTON------------------------------
        CTkButton(frame, text="Sign Up", width=260, height=38, corner_radius=15,
                  fg_color="#ffe7eb", hover_color="#ffb7ce", text_color="#c75b7a",
                  font=("Arial", 13, "bold"), command=self.open_signup).pack(pady=4)

        self.app.bind("<Return>", lambda e: self.login())
        self.success = False
        self.app.mainloop()

    def login(self):
        user = self.username.get().strip()
        pwd = self.password.get()
        user_id = validate_user(user, pwd)
        if user_id:
            self.success = True
            self.user_id = user_id
            self.app.destroy()
        else:
            self.error_label.configure(text="Invalid username or password.")

    # SIGN UP------------------------------
    def open_signup(self):
        dialog = CTkToplevel(self.app)
        dialog.title("Create Account")
        dialog.geometry("380x420+400+200")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(fg_color="#ffd6dc")

        CTkLabel(dialog, text="🌸 Create Account", font=("Arial", 20, "bold"), text_color="#c75b7a").pack(pady=(40, 5))
        CTkLabel(dialog, text="Fill in your details", font=("Arial", 12), text_color="gray").pack(pady=(0, 25))

        new_user = CTkEntry(dialog, placeholder_text="Username", width=260, height=38,
                            corner_radius=15, fg_color="#ffe7eb", border_width=0,
                            text_color="#000000", font=("Arial", 13))
        new_user.pack(pady=6)
        new_user.focus()

        new_pass = CTkEntry(dialog, placeholder_text="Password", width=260, height=38,
                            corner_radius=15, fg_color="#ffe7eb", border_width=0,
                            text_color="#000000", font=("Arial", 13), show="*")
        new_pass.pack(pady=6)

        confirm_pass = CTkEntry(dialog, placeholder_text="Confirm Password", width=260, height=38,
                                corner_radius=15, fg_color="#ffe7eb", border_width=0,
                                text_color="#000000", font=("Arial", 13), show="*")
        confirm_pass.pack(pady=6)

        error = CTkLabel(dialog, text="", text_color="#c0392b", font=("Arial", 11))
        error.pack(pady=(4, 0))

        def confirm():
            username = new_user.get().strip()
            password = new_pass.get()
            confirm = confirm_pass.get()

            if not username or not password:
                error.configure(text="Please fill in all fields.")
                return
            if password != confirm:
                error.configure(text="Passwords do not match.")
                return
            if len(password) < 6:
                error.configure(text="Password must be at least 6 characters.")
                return

            success = register_user(username, password)
            if success:
                dialog.destroy()
                self.error_label.configure(text="Account created! You can now log in.", text_color="#27ae60")
            else:
                error.configure(text="Username already exists.")

        CTkButton(dialog, text="Create Account", width=260, height=38, corner_radius=15,
                  fg_color="#ffb7ce", hover_color="#ffe7eb", text_color="#ffffff",
                  font=("Arial", 13, "bold"), command=confirm).pack(pady=16)

        dialog.bind("<Return>", lambda e: confirm())
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, messagebox, StringVar, Radiobutton, font
from tkinter import ttk
from generator import PasswordGenerator
from analyzer import analyze_password

# Kali dark theme colors
KALI_BG = "#222629"
KALI_FG = "#86c232"
KALI_ACCENT = "#45a29e"
KALI_ENTRY_BG = "#393e46"
KALI_ENTRY_FG = "#eeeeee"
KALI_BUTTON_BG = "#393e46"
KALI_BUTTON_FG = "#86c232"
KALI_HIGHLIGHT = "#232931"

LABEL_FONT = ("Segoe UI", 12, "bold")

class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")
        master.configure(bg=KALI_BG)
        master.geometry("600x600")  # Larger window

        style = ttk.Style(master)
        style.theme_use('clam')
        style.configure("TLabel", background=KALI_BG, foreground=KALI_FG, font=LABEL_FONT)
        style.configure("TButton", background=KALI_BUTTON_BG, foreground=KALI_BUTTON_FG, borderwidth=0, font=LABEL_FONT)
        style.configure("TEntry", fieldbackground=KALI_ENTRY_BG, foreground=KALI_ENTRY_FG)
        style.configure("TProgressbar", background=KALI_ACCENT, troughcolor=KALI_HIGHLIGHT, bordercolor=KALI_HIGHLIGHT, lightcolor=KALI_ACCENT, darkcolor=KALI_ACCENT)
        style.map("TButton", background=[('active', KALI_ACCENT)])

        # Mode selection
        self.mode_var = StringVar(value="inbuilt")
        self.inbuilt_radio = Radiobutton(master, text="Inbuilt Mode", variable=self.mode_var, value="inbuilt", command=self.switch_mode,
                                         bg=KALI_BG, fg=KALI_FG, selectcolor=KALI_HIGHLIGHT, activebackground=KALI_BG, activeforeground=KALI_ACCENT, font=LABEL_FONT)
        self.inbuilt_radio.pack(pady=(10, 0))
        self.simple_radio = Radiobutton(master, text="Simple Mode (Text to Password)", variable=self.mode_var, value="simple", command=self.switch_mode,
                                        bg=KALI_BG, fg=KALI_FG, selectcolor=KALI_HIGHLIGHT, activebackground=KALI_BG, activeforeground=KALI_ACCENT, font=LABEL_FONT)
        self.simple_radio.pack(pady=(0, 10))

        self.label = Label(master, text="Password Length:", bg=KALI_BG, fg=KALI_FG, font=LABEL_FONT)
        self.label.pack()

        self.length_entry = Entry(master, bg=KALI_ENTRY_BG, fg=KALI_ENTRY_FG, insertbackground=KALI_FG)
        self.length_entry.pack(pady=(0, 10))

        self.input_label = Label(master, text="Input Text (for Simple Mode):", bg=KALI_BG, fg=KALI_FG, font=LABEL_FONT)
        self.input_label.pack()
        self.input_entry = Entry(master, bg=KALI_ENTRY_BG, fg=KALI_ENTRY_FG, insertbackground=KALI_FG)
        self.input_entry.pack(pady=(0, 10))

        self.generate_button = Button(master, text="Generate Password", command=self.generate_password,
                                      bg=KALI_BUTTON_BG, fg=KALI_BUTTON_FG, activebackground=KALI_ACCENT, activeforeground=KALI_FG, font=LABEL_FONT)
        self.generate_button.pack(pady=(0, 10))

        self.password_text = Text(master, height=2, width=40, bg=KALI_ENTRY_BG, fg=KALI_ACCENT, insertbackground=KALI_FG)
        self.password_text.pack(pady=(0, 10))

        # Copy button
        self.copy_button = Button(master, text="Copy Password", command=self.copy_password,
                                  bg=KALI_BUTTON_BG, fg=KALI_BUTTON_FG, activebackground=KALI_ACCENT, activeforeground=KALI_FG, font=LABEL_FONT)
        self.copy_button.pack(pady=(0, 10))

        # Brute-force time label
        self.brute_force_time_var = StringVar()
        self.brute_force_time_label = Label(master, textvariable=self.brute_force_time_var, bg=KALI_BG, fg=KALI_ACCENT, font=LABEL_FONT)
        self.brute_force_time_label.pack(pady=(0, 10))

        # Complexity gauge
        self.complexity_label = Label(master, text="Password Complexity:", bg=KALI_BG, fg=KALI_FG, font=LABEL_FONT)
        self.complexity_label.pack()
        self.complexity_gauge = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate", maximum=5, style="TProgressbar")
        self.complexity_gauge.pack(pady=(0, 10))

        self.analyze_button = Button(master, text="Analyze Password", command=self.analyze_password,
                                     bg=KALI_BUTTON_BG, fg=KALI_BUTTON_FG, activebackground=KALI_ACCENT, activeforeground=KALI_FG, font=LABEL_FONT)
        self.analyze_button.pack(pady=(0, 10))

        self.analysis_text = Text(master, height=8, width=60, bg=KALI_ENTRY_BG, fg=KALI_FG, insertbackground=KALI_FG)
        self.analysis_text.pack(pady=(0, 10))

        self.scrollbar = Scrollbar(master, command=self.analysis_text.yview, bg=KALI_BG, troughcolor=KALI_HIGHLIGHT)
        self.scrollbar.pack(side="right", fill="y")
        self.analysis_text.config(yscrollcommand=self.scrollbar.set)

        self.switch_mode()

    def switch_mode(self):
        mode = self.mode_var.get()
        if mode == "inbuilt":
            self.label.config(state="normal")
            self.length_entry.config(state="normal")
            self.input_label.config(state="disabled")
            self.input_entry.config(state="disabled")
        else:
            self.label.config(state="disabled")
            self.length_entry.config(state="disabled")
            self.input_label.config(state="normal")
            self.input_entry.config(state="normal")

    def generate_password(self):
        mode = self.mode_var.get()
        if mode == "inbuilt":
            length_str = self.length_entry.get()
            if not length_str.isdigit() or int(length_str) < 1:
                messagebox.showerror("Invalid Input", "Please enter a valid positive integer for password length.")
                return
            length = int(length_str)
            generator = PasswordGenerator()
            password = generator.generate_password(length)
        else:
            user_text = self.input_entry.get()
            if not user_text:
                messagebox.showerror("Invalid Input", "Please enter text to convert into a password.")
                return
            password = self.simple_text_to_password(user_text)

        self.password_text.delete(1.0, END)
        self.password_text.insert(END, password)

        # Show brute-force time
        generator = PasswordGenerator()
        brute_force_time = generator.get_brute_force_time(password)
        self.brute_force_time_var.set(f"Estimated brute-force time: {brute_force_time}")

        # Update complexity gauge
        score = self.get_complexity_score(password)
        self.complexity_gauge['value'] = score

    def analyze_password(self):
        password = self.password_text.get(1.0, END).strip()
        analysis = analyze_password(password)
        self.analysis_text.delete(1.0, END)
        self.analysis_text.insert(END, analysis)

        # Update complexity gauge when analyzing
        score = self.get_complexity_score(password)
        self.complexity_gauge['value'] = score

        # Show brute-force time
        generator = PasswordGenerator()
        brute_force_time = generator.get_brute_force_time(password)
        self.brute_force_time_var.set(f"Estimated brute-force time: {brute_force_time}")

    def get_complexity_score(self, password):
        import string
        score = 0
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in string.punctuation for c in password):
            score += 1
        if len(password) >= 12:
            score += 1
        return score

    def simple_text_to_password(self, text):
        substitutions = {
            'a': '@', 'A': '@',
            'i': '!', 'I': '!',
            'e': '3', 'E': '3',
            'o': '0', 'O': '0',
            's': '$', 'S': '$',
            'l': '1', 'L': '1',
            't': '7', 'T': '7',
            'b': '8', 'B': '8',
            'g': '9', 'G': '9',
            'z': '2', 'Z': '2',
            'h': '#', 'H': '#',
            'm': 'M', 'M': 'M',
            'n': 'N', 'N': 'N',
            'u': 'U', 'U': 'U',
            'w': 'W', 'W': 'W',
        }
        return ''.join(substitutions.get(c, c) for c in text)

    def copy_password(self):
        password = self.password_text.get(1.0, END).strip()
        if password:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

if __name__ == "__main__":
    root = Tk()
    gui = PasswordGeneratorGUI(root)
    root.mainloop()
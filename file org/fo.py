import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

# A dictionary mapping file extensions to folder names.
# You can easily customize this to add more file types.
EXTENSION_MAP = {
    # Images
    '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
    '.bmp': 'Images', '.svg': 'Images', '.tiff': 'Images', '.webp': 'Images',
    '.heic': 'Images',
    
    # Documents
    '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
    '.txt': 'Text Documents', '.rtf': 'Documents', '.odt': 'Documents',
    '.md': 'Text Documents',
    
    # Spreadsheets & Presentations
    '.xls': 'Spreadsheets', '.xlsx': 'Spreadsheets', '.csv': 'Spreadsheets',
    '.ppt': 'Presentations', '.pptx': 'Presentations',
    
    # Audio
    '.mp3': 'Audio', '.wav': 'Audio', '.aac': 'Audio', '.flac': 'Audio',
    '.ogg': 'Audio', '.m4a': 'Audio',
    
    # Video
    '.mp4': 'Videos', '.mov': 'Videos', '.avi': 'Videos', '.mkv': 'Videos',
    '.wmv': 'Videos', '.flv': 'Videos',
    
    # Archives
    '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives', '.tar': 'Archives',
    '.gz': 'Archives',
    
    # Code & Scripts
    '.py': 'Scripts', '.js': 'Scripts', '.html': 'Web Files', '.css': 'Web Files',
    '.java': 'Code', '.cpp': 'Code', '.c': 'Code', '.sh': 'Scripts',
    
    # Executables & Installers
    '.exe': 'Executables', '.msi': 'Installers', '.dmg': 'Installers',
}


class FileOrganizerApp(TkinterDnD.Tk):
    """
    A GUI application for organizing files in a directory based on their extension.
    """
    def __init__(self):
        super().__init__()
        self.title("Automatic File Organizer")
        self.geometry("600x450")
        self.configure(bg="#2E2E2E")

        # --- Style Configuration ---
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12, "bold"), borderwidth=0)
        style.map("TButton",
                  foreground=[('active', 'white')],
                  background=[('active', '#555555'), ('!disabled', '#007ACC')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        style.configure("TEntry", font=("Helvetica", 12), borderwidth=1, relief="solid")
        style.configure("Title.TLabel", font=("Helvetica", 20, "bold"))
        style.configure("Instruction.TLabel", font=("Helvetica", 11), foreground="#B0B0B0")

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # --- UI Elements ---
        title_label = ttk.Label(main_frame, text="File Organizer", style="Title.TLabel")
        title_label.pack(pady=(0, 20))

        # --- Drag and Drop Area ---
        self.drop_target = tk.Label(
            main_frame,
            text="Drag and Drop a Folder Here",
            font=("Helvetica", 14),
            relief="ridge",  # <-- changed from "dashed" to "ridge"
            borderwidth=2,
            bg="#3C3C3C",
            fg="white",
            padx=20,
            pady=60
        )
        self.drop_target.pack(fill=tk.X, pady=10)
        
        # Register the drop target
        self.drop_target.drop_target_register(DND_FILES)
        self.drop_target.dnd_bind('<<Drop>>', self.handle_drop)

        ttk.Label(main_frame, text="or select a directory manually:", style="Instruction.TLabel").pack()

        # --- Path Entry and Browse Button ---
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=10)
        
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, font=("Helvetica", 12))
        self.path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5)
        
        browse_button = ttk.Button(path_frame, text="Browse...", command=self.select_directory)
        browse_button.pack(side=tk.RIGHT, padx=(10, 0))

        # --- Organize Button ---
        self.organize_button = ttk.Button(main_frame, text="Organize Files", command=self.organize_files)
        self.organize_button.pack(pady=20, ipady=10, fill=tk.X)


    def handle_drop(self, event):
        """Handle the file drop event."""
        # The path might be enclosed in curly braces {}
        path = event.data.strip('{}')
        if os.path.isdir(path):
            self.path_var.set(path)
            self.drop_target.config(text=f"Folder Selected:\n{os.path.basename(path)}")
        else:
            messagebox.showerror("Error", "Please drop a valid folder, not a file.")
            self.drop_target.config(text="Drag and Drop a Folder Here")


    def select_directory(self):
        """Open a dialog to select a directory."""
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
            self.drop_target.config(text=f"Folder Selected:\n{os.path.basename(path)}")


    def organize_files(self):
        """The core logic to organize files in the selected directory."""
        directory_path = self.path_var.get()
        if not os.path.isdir(directory_path):
            messagebox.showerror("Error", "Please select a valid directory first.")
            return

        try:
            files_moved = 0
            # Get a list of all items in the directory
            for item_name in os.listdir(directory_path):
                source_path = os.path.join(directory_path, item_name)

                # Skip directories and the script itself
                if os.path.isdir(source_path) or item_name == os.path.basename(__file__):
                    continue

                # Get the file extension
                _, file_extension = os.path.splitext(item_name)
                file_extension = file_extension.lower()

                # Determine the destination folder name
                if file_extension in EXTENSION_MAP:
                    folder_name = EXTENSION_MAP[file_extension]
                else:
                    # For unknown extensions, create a folder like 'XYZ Files'
                    folder_name = f"{file_extension[1:].upper()} Files" if file_extension else "Other"

                # Create the destination folder if it doesn't exist
                dest_folder_path = os.path.join(directory_path, folder_name)
                if not os.path.exists(dest_folder_path):
                    os.makedirs(dest_folder_path)

                # Move the file
                destination_path = os.path.join(dest_folder_path, item_name)
                shutil.move(source_path, destination_path)
                files_moved += 1

            messagebox.showinfo("Success", f"Organization complete!\nMoved {files_moved} files.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            # Reset the UI
            self.path_var.set("")
            self.drop_target.config(text="Drag and Drop a Folder Here")


if __name__ == "__main__":
    # To run this, you need to install tkinterdnd2:
    # pip install tkinterdnd2
    app = FileOrganizerApp()
    app.mainloop()

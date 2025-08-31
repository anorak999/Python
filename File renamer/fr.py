import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD  # <-- Add this import

class FileRenamerApp(TkinterDnD.Tk):  # <-- Change tk.Tk to TkinterDnD.Tk
    def __init__(self):
        super().__init__()

        self.title("Advanced File Renamer")
        self.geometry("900x700")
        self.configure(bg="#f0f0f0")

        self.files_to_rename = []
        self.preview_names = []

        # --- Main Layout ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Left Column: File Selection & Preview ---
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nswe", padx=(0, 10))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # File Selection
        selection_frame = ttk.LabelFrame(left_frame, text="1. Select Files", padding="10")
        selection_frame.pack(fill=tk.X, pady=(0, 10))

        add_files_btn = ttk.Button(selection_frame, text="Add Files", command=self.add_files)
        add_files_btn.pack(side=tk.LEFT, padx=(0, 5))

        add_folder_btn = ttk.Button(selection_frame, text="Add Folder", command=self.add_folder)
        add_folder_btn.pack(side=tk.LEFT)

        clear_btn = ttk.Button(selection_frame, text="Clear List", command=self.clear_file_list)
        clear_btn.pack(side=tk.RIGHT)

        # Drag-and-drop area
        self.drop_label = ttk.Label(selection_frame, text="Or drag files/folders here", relief="ridge", padding=10)
        self.drop_label.pack(fill=tk.X, pady=(10, 0))
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop_files)

        # File Listbox (Original vs. Preview)
        preview_frame = ttk.LabelFrame(left_frame, text="Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(preview_frame, columns=("original", "renamed"), show="headings")
        self.tree.heading("original", text="Original Name")
        self.tree.heading("renamed", text="Renamed Preview")
        self.tree.pack(fill=tk.BOTH, expand=True)


        # --- Right Column: Renaming Options ---
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="ns", padx=(10, 0))
        
        options_frame = ttk.LabelFrame(right_frame, text="2. Renaming Rules", padding="10")
        options_frame.pack(fill=tk.X)
        
        self.notebook = ttk.Notebook(options_frame)
        self.notebook.pack(pady=5, padx=5, fill="both", expand="yes")

        # Find & Replace Tab
        self.replace_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.replace_tab, text='Find & Replace')
        self.create_replace_tab()

        # Add Text Tab
        self.add_text_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_text_tab, text='Add Text')
        self.create_add_text_tab()

        # Numbering Tab
        self.numbering_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.numbering_tab, text='Numbering')
        self.create_numbering_tab()

        # Case Change Tab
        self.case_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.case_tab, text='Change Case')
        self.create_case_tab()
        
        # Action Buttons
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        preview_btn = ttk.Button(action_frame, text="Update Preview", command=self.update_preview)
        preview_btn.pack(fill=tk.X, pady=(0, 5))
        
        rename_btn = ttk.Button(action_frame, text="Apply Rename", command=self.apply_rename, style="Accent.TButton")
        rename_btn.pack(fill=tk.X)
        
        # Style
        self.style = ttk.Style(self)
        self.style.configure("Accent.TButton", foreground="white", background="#0078D7")


    def create_replace_tab(self):
        ttk.Label(self.replace_tab, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.find_entry = ttk.Entry(self.replace_tab)
        self.find_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.replace_tab, text="Replace with:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.replace_entry = ttk.Entry(self.replace_tab)
        self.replace_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.replace_tab.grid_columnconfigure(1, weight=1)

    def create_add_text_tab(self):
        ttk.Label(self.add_text_tab, text="Prefix:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.prefix_entry = ttk.Entry(self.add_text_tab)
        self.prefix_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.add_text_tab, text="Suffix:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.suffix_entry = ttk.Entry(self.add_text_tab)
        self.suffix_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.add_text_tab.grid_columnconfigure(1, weight=1)

    def create_numbering_tab(self):
        ttk.Label(self.numbering_tab, text="Pattern:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.number_pattern_entry = ttk.Entry(self.numbering_tab)
        self.number_pattern_entry.insert(0, "{name}-{num}{ext}")
        self.number_pattern_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.numbering_tab, text="Start at:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.start_num_spinbox = ttk.Spinbox(self.numbering_tab, from_=0, to=9999)
        self.start_num_spinbox.set(1)
        self.start_num_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.numbering_tab, text="Padding:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.padding_spinbox = ttk.Spinbox(self.numbering_tab, from_=0, to=10)
        self.padding_spinbox.set(3)
        self.padding_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        self.numbering_tab.grid_columnconfigure(1, weight=1)

    def create_case_tab(self):
        self.case_var = tk.StringVar(value="lower")
        cases = [("Lowercase", "lower"), ("UPPERCASE", "upper"), ("Title Case", "title")]
        for i, (text, value) in enumerate(cases):
            ttk.Radiobutton(self.case_tab, text=text, variable=self.case_var, value=value).pack(anchor="w", padx=5, pady=2)


    def add_files(self):
        files = filedialog.askopenfilenames(title="Select files")
        if files:
            self.files_to_rename.extend(files)
            self.update_file_list()

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    self.files_to_rename.append(filepath)
            self.update_file_list()

    def clear_file_list(self):
        self.files_to_rename.clear()
        self.update_file_list()

    def update_file_list(self):
        self.tree.delete(*self.tree.get_children())
        for f in self.files_to_rename:
            self.tree.insert("", "end", values=(os.path.basename(f), ""))
        self.update_preview()

    def update_preview(self):
        self.preview_names = []
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        
        start_num = int(self.start_num_spinbox.get()) if self.start_num_spinbox.get().isdigit() else 1

        for i, filepath in enumerate(self.files_to_rename):
            path, full_filename = os.path.split(filepath)
            filename, ext = os.path.splitext(full_filename)
            new_name = filename # Start with the original name (without extension)

            if current_tab == 'Find & Replace':
                find_text = self.find_entry.get()
                replace_text = self.replace_entry.get()
                if find_text:
                    new_name = new_name.replace(find_text, replace_text)

            elif current_tab == 'Add Text':
                prefix = self.prefix_entry.get()
                suffix = self.suffix_entry.get()
                new_name = f"{prefix}{new_name}{suffix}"

            elif current_tab == 'Numbering':
                pattern = self.number_pattern_entry.get()
                num = start_num + i
                pad = int(self.padding_spinbox.get()) if self.padding_spinbox.get().isdigit() else 0
                num_str = str(num).zfill(pad)
                
                new_full_name = pattern.format(name=filename, num=num_str, ext=ext)
                self.preview_names.append(os.path.join(path, new_full_name))
                continue # Skip the default extension joining for this tab

            elif current_tab == 'Change Case':
                case_type = self.case_var.get()
                if case_type == "lower":
                    new_name = new_name.lower()
                elif case_type == "upper":
                    new_name = new_name.upper()
                elif case_type == "title":
                    new_name = new_name.title()

            new_full_name = new_name + ext
            self.preview_names.append(os.path.join(path, new_full_name))
        
        # Update Treeview with preview
        for i, item_id in enumerate(self.tree.get_children()):
            if i < len(self.preview_names):
                self.tree.item(item_id, values=(os.path.basename(self.files_to_rename[i]), os.path.basename(self.preview_names[i])))

    def apply_rename(self):
        self.update_preview() # Ensure preview is current
        if not self.files_to_rename or not self.preview_names:
            messagebox.showerror("Error", "No files to rename or preview generated.")
            return

        if messagebox.askyesno("Confirm Rename", f"Are you sure you want to rename {len(self.files_to_rename)} files?"):
            renamed_count = 0
            error_count = 0
            for old_path, new_path in zip(self.files_to_rename, self.preview_names):
                try:
                    if old_path != new_path:
                        os.rename(old_path, new_path)
                        renamed_count += 1
                except Exception as e:
                    print(f"Error renaming {old_path}: {e}")
                    error_count += 1
            
            messagebox.showinfo("Success", f"Successfully renamed {renamed_count} files.\n{error_count} errors occurred.")
            self.clear_file_list()

    def on_drop_files(self, event):
        # event.data is a string of file paths separated by space
        dropped = self.tk.splitlist(event.data)
        for path in dropped:
            if os.path.isfile(path):
                self.files_to_rename.append(path)
            elif os.path.isdir(path):
                for filename in os.listdir(path):
                    filepath = os.path.join(path, filename)
                    if os.path.isfile(filepath):
                        self.files_to_rename.append(filepath)
        self.update_file_list()


if __name__ == "__main__":
    app = FileRenamerApp()
    app.mainloop()

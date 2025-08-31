import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageTk
import pyfiglet
import pyperclip
import os

# Global variables
current_ascii_art = ""
ascii_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
ascii_width = 100
ascii_charset = "".join(ascii_chars)
current_image_path = None
dark_mode = False

def text_to_ascii(text, font="standard"):
    """Converts a given text to ASCII art using pyfiglet."""
    try:
        ascii_art = pyfiglet.figlet_format(text, font=font)
        return ascii_art
    except Exception as e:
        return f"Error: {e}"

def image_to_ascii(image_path, width=100, charset=ascii_chars):
    """Converts an image file to ASCII art."""
    try:
        img = Image.open(image_path)
        img = img.convert('L')  # Convert to grayscale

        # Calculate new dimensions while maintaining aspect ratio
        aspect_ratio = img.height / img.width
        new_height = int(width * aspect_ratio * 0.5)
        img = img.resize((width, new_height))

        pixels = img.getdata()
        ascii_str = ""
        scale = len(charset) - 1
        for pixel_value in pixels:
            ascii_str += charset[int(pixel_value / 255 * scale)]

        ascii_art = ""
        for i in range(0, len(ascii_str), width):
            ascii_art += ascii_str[i:i + width] + "\n"

        return ascii_art
    except Exception as e:
        return f"Error: {e}"

def copy_to_clipboard():
    """Copies the generated ASCII art to the clipboard."""
    global current_ascii_art
    if current_ascii_art:
        try:
            pyperclip.copy(current_ascii_art)
            status_var.set("Copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {e}")
    else:
        messagebox.showwarning("Warning", "No ASCII art to copy.")

def save_to_file():
    """Saves the generated ASCII art to a text file."""
    global current_ascii_art
    if not current_ascii_art:
        messagebox.showwarning("Warning", "No ASCII art to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(current_ascii_art)
            status_var.set(f"Saved to {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

def update_ascii_art(art):
    """Updates the Text widget with the new ASCII art."""
    global current_ascii_art
    current_ascii_art = art
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, current_ascii_art)
    output_text.config(state='disabled')

def handle_text_mode():
    """Switches the GUI to text mode."""
    text_frame.pack(fill='both', expand=True, padx=10, pady=10)
    image_frame.pack_forget()
    status_var.set("Text to ASCII mode")

def handle_image_mode():
    """Switches the GUI to image mode."""
    image_frame.pack(fill='both', expand=True, padx=10, pady=10)
    text_frame.pack_forget()
    status_var.set("Image to ASCII mode")

def generate_text_ascii():
    """Generates ASCII art from text input."""
    text = text_entry.get()
    font = font_var.get()
    if text:
        art = text_to_ascii(text, font)
        update_ascii_art(art)
        status_var.set("Generated ASCII art from text.")
    else:
        messagebox.showwarning("Warning", "Please enter some text.")

def generate_image_ascii():
    """Prompts the user to select an image file and generates ASCII art."""
    global current_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        current_image_path = file_path
        show_image_preview(file_path)
        width = int(width_var.get())
        charset = charset_entry.get() or ascii_chars
        art = image_to_ascii(file_path, width, charset)
        update_ascii_art(art)
        status_var.set("Generated ASCII art from image.")

def show_image_preview(image_path):
    """Displays a thumbnail preview of the selected image."""
    try:
        img = Image.open(image_path)
        img.thumbnail((120, 120))
        img_tk = ImageTk.PhotoImage(img)
        image_preview_label.config(image=img_tk)
        image_preview_label.image = img_tk
    except Exception:
        image_preview_label.config(image='', text="Preview failed")

def handle_drag_and_drop(event):
    """Handles drag and drop for image files (Windows only)."""
    file_path = event.data.strip().strip('{}')
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        global current_image_path
        current_image_path = file_path
        show_image_preview(file_path)
        width = int(width_var.get())
        charset = charset_entry.get() or ascii_chars
        art = image_to_ascii(file_path, width, charset)
        update_ascii_art(art)
        status_var.set("Generated ASCII art from dropped image.")
    else:
        messagebox.showwarning("Invalid File", "Please drop a valid image file.")

def update_ascii_width(val):
    width_label.config(text=f"Width: {val}")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#222" if dark_mode else "#f0f0f0"
    fg = "#fff" if dark_mode else "#000"
    root.config(bg=bg)
    main_frame.config(style="Dark.TFrame" if dark_mode else "TFrame")
    output_text.config(bg=bg, fg=fg, insertbackground=fg)
    status_bar.config(bg=bg, fg=fg)
    for widget in [text_frame, image_frame]:
        widget.config(style="Dark.TFrame" if dark_mode else "TFrame")

# Main window setup
root = tk.Tk()
root.title("ASCII Art Generator")
root.geometry("900x650")

# Style
style = ttk.Style()
style.theme_use('clam')
style.configure("Dark.TFrame", background="#222")
style.configure("TFrame", background="#f0f0f0")

# Menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

mode_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Mode", menu=mode_menu)
mode_menu.add_command(label="Text to ASCII", command=handle_text_mode)
mode_menu.add_command(label="Image to ASCII", command=handle_image_mode)

option_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=option_menu)
option_menu.add_command(label="Toggle Dark/Light Theme", command=toggle_theme)
option_menu.add_command(label="Save ASCII Art", command=save_to_file)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=root.quit)

# Main frame for content
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill='both', expand=True)

# Output display area
output_label = ttk.Label(main_frame, text="Generated ASCII Art:")
output_label.pack(anchor='w', pady=(0, 5))

output_text = tk.Text(main_frame, wrap='none', font=("Courier", 8), width=100, height=28, state='disabled')
output_text.pack(fill='both', expand=True)

# Copy and Save buttons
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=8)
copy_button = ttk.Button(button_frame, text="Copy to Clipboard 📋", command=copy_to_clipboard)
copy_button.pack(side='left', padx=5)
save_button = ttk.Button(button_frame, text="Save to File 💾", command=save_to_file)
save_button.pack(side='left', padx=5)

# Text mode frame
text_frame = ttk.Frame(main_frame)
text_label = ttk.Label(text_frame, text="Enter Text:")
text_label.pack(anchor='w')
text_entry = ttk.Entry(text_frame, width=50)
text_entry.pack(fill='x', pady=(0, 5))

font_label = ttk.Label(text_frame, text="Font:")
font_label.pack(anchor='w')
font_var = tk.StringVar(value="standard")
font_list = sorted(pyfiglet.FigletFont.getFonts())
font_combo = ttk.Combobox(text_frame, textvariable=font_var, values=font_list, width=30)
font_combo.pack(fill='x', pady=(0, 5))

generate_text_button = ttk.Button(text_frame, text="Generate Text ASCII", command=generate_text_ascii)
generate_text_button.pack()

# Image mode frame
image_frame = ttk.Frame(main_frame)
image_label = ttk.Label(image_frame, text="Drag & Drop Image or Click 'Browse'")
image_label.pack(pady=10)
browse_button = ttk.Button(image_frame, text="Browse Image 📂", command=generate_image_ascii)
browse_button.pack()

# ASCII width slider
width_var = tk.IntVar(value=100)
width_label = ttk.Label(image_frame, text=f"Width: {width_var.get()}")
width_label.pack()
width_slider = ttk.Scale(image_frame, from_=40, to=200, orient='horizontal', variable=width_var, command=lambda v: update_ascii_width(int(float(v))))
width_slider.pack(fill='x', padx=10, pady=5)

# ASCII charset entry
charset_label = ttk.Label(image_frame, text="ASCII Charset (optional):")
charset_label.pack(anchor='w')
charset_entry = ttk.Entry(image_frame, width=30)
charset_entry.insert(0, ascii_charset)
charset_entry.pack(fill='x', pady=(0, 5))

# Image preview
image_preview_label = ttk.Label(image_frame, text="No image selected", anchor='center')
image_preview_label.pack(pady=5)

# Drag and drop functionality (Windows only)
try:
    import tkinterdnd2 as tkdnd
    root.tk.call('package', 'require', 'tkdnd')
    image_frame.drop_target_register(tkdnd.DND_FILES)
    image_frame.dnd_bind('<<Drop>>', handle_drag_and_drop)
except Exception:
    # Fallback: no drag-and-drop
    pass

# Status bar
status_var = tk.StringVar(value="Ready")
status_bar = tk.Label(root, textvariable=status_var, anchor='w', relief='sunken')
status_bar.pack(fill='x', side='bottom')

# Initial mode
handle_text_mode()

root.mainloop()
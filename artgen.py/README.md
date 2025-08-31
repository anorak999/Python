# ASCII Art Generator

A modern Python GUI application for generating ASCII art from text or images. Built with **Tkinter**, **Pillow**, **PyFiglet**, and **Pyperclip**.

---

## Features

* **Text to ASCII Art:** Generate stylized ASCII banners from any text with multiple font options.
* **Image to ASCII Art:** Convert `.png`, `.jpg`, `.jpeg`, or `.bmp` images into ASCII art. Adjust output width and character sets for customized results.
* **Copy & Save:** Copy ASCII art directly to your clipboard or save it as a `.txt` file.
* **Theme Support:** Switch between dark and light themes for comfortable usage.
* **Image Preview:** Preview a thumbnail of the selected image before conversion.
* **Drag & Drop (Windows):** Drag image files into the app window for quick conversion.
* **Status Bar:** Receive instant feedback (e.g., "Copied to clipboard," "Saved successfully," or error messages).

---

## Requirements

* Python 3.7+
* [Pillow](https://pypi.org/project/Pillow/)
* [pyfiglet](https://pypi.org/project/pyfiglet/)
* [pyperclip](https://pypi.org/project/pyperclip/)
* [tkinterdnd2](https://pypi.org/project/tkinterdnd2/) *(optional, for drag-and-drop support on Windows)*

---

## Installation

1. **Clone or download** this repository.
2. **Install dependencies:**

   ```bash
   pip install pillow pyfiglet pyperclip
   ```

   For Windows users who want drag-and-drop support:

   ```bash
   pip install tkinterdnd2
   ```

---

## Usage

Run the application with:

```bash
python artgen.py
```

### Text to ASCII

1. Choose **"Text to ASCII"** from the menu.
2. Enter text, select a font, and click **"Generate Text ASCII"**.

### Image to ASCII

1. Choose **"Image to ASCII"** from the menu.
2. Click **"Browse Image"** or drag an image into the window.
3. Adjust width and character set, then generate the ASCII output.

### Copy & Save

Use the **"Copy to Clipboard"** or **"Save to File"** buttons under the output area.

### Theme Toggle

Switch between dark and light modes from the **Options** menu.



---

Created by **anoraK999**

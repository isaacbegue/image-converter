import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, UnidentifiedImageError
import os

def select_images():
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp")]
    )
    if file_paths:
        entry_image_paths.delete(0, tk.END)
        entry_image_paths.insert(0, ";".join(file_paths))

def convert_images():
    input_paths = entry_image_paths.get().split(";")
    output_format = dropdown_format.get().lower()

    print(f"DEBUG: input_paths={input_paths}, output_format={output_format}")

    if not input_paths or not output_format:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    # Open a dialog to select the output folder
    output_dir = filedialog.askdirectory(title="Select Output Directory")

    print(f"DEBUG: output_dir={output_dir}")

    if not output_dir:
        return  # User cancelled the directory selection

    try:
        for input_path in input_paths:
            img = Image.open(input_path)
            print(f"DEBUG: Converting {input_path}")

            if output_format in ["jpg", "jpeg"]:
                img = img.convert("RGB")  # Ensures conversion to RGB mode for JPG

            base_name = os.path.basename(input_path)
            file_name, _ = os.path.splitext(base_name)
            output_file = os.path.join(output_dir, f"{file_name}.{output_format}")

            img.save(output_file, "JPEG" if output_format in ["jpg", "jpeg"] else output_format.upper())
            print(f"DEBUG: Saved {output_file}")

        messagebox.showinfo("Success", f"Images successfully converted and saved to {output_dir}")
    except UnidentifiedImageError:
        messagebox.showerror("Error", "One or more selected files could not be identified as images.")
    except OSError as e:
        messagebox.showerror("Error", f"An OS error occurred: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        print(f"DEBUG: Exception details: {e}")

# Create the main window
root = tk.Tk()
root.title("Image Converter")
root.geometry("500x400")

# Image Paths
label_image_paths = tk.Label(root, text="Image Paths:")
label_image_paths.pack(pady=10)
entry_image_paths = tk.Entry(root, width=60)
entry_image_paths.pack(pady=5)
button_browse_images = tk.Button(root, text="Browse", command=select_images)
button_browse_images.pack(pady=5)

# Output Format
label_format = tk.Label(root, text="Select Output Format:")
label_format.pack(pady=10)
formats = ["JPG", "PNG", "BMP", "GIF", "TIFF"]
dropdown_format = tk.StringVar(root)
dropdown_format.set(formats[0])
dropdown_menu = tk.OptionMenu(root, dropdown_format, *formats)
dropdown_menu.pack(pady=5)

# Convert Button
button_convert = tk.Button(root, text="Convert Images", command=convert_images)
button_convert.pack(pady=20)

# Start the application
root.mainloop()

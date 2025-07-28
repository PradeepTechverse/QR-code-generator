import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import os
from datetime import datetime
import csv

# History storage
qr_history = []

# Theme configurations
themes = {
    "Default": {"bg": "#F0F4F8", "fg": "#2B3A67", "entry_bg": "#FFFFFF", "entry_fg": "#2B3A67"},
    "Dark": {"bg": "#2B2B2B", "fg": "#E0E0E0", "entry_bg": "#3C3C3C", "entry_fg": "#E0E0E0"},
    "Pastel": {"bg": "#FCE4EC", "fg": "#880E4F", "entry_bg": "#F8BBD0", "entry_fg": "#880E4F"}
}

# QR code size mappings
size_map = {"Small": 10, "Medium": 15, "Large": 20}

def generate_qr_code(text, size, fill_color, back_color, border):
    if not text.strip():
        messagebox.showerror("Error", "Please enter text or URL.")
        return None

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Add to history without saving yet
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    qr_history.append((text, timestamp, None))  # Filename will be updated on download
    update_history()
    
    return img

def download_qr_code():
    if not qr_history or not qr_history[-1][2] is None:
        messagebox.showerror("Error", "No QR code to download!")
        return
    
    text, timestamp, _ = qr_history[-1]
    size = size_map[size_var.get()]
    fill_color = fill_color_var.get()
    back_color = back_color_var.get()
    border = border_scale.get()
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    filename = f"qrcodes/qrcode_{timestamp}.png"
    try:
        os.makedirs("qrcodes", exist_ok=True)
        img.save(filename)
        qr_history[-1] = (text, timestamp, filename)  # Update filename in history
        update_history()
        messagebox.showinfo("Success", f"QR code saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save QR code: {e}")

def update_history():
    history_listbox.delete(0, tk.END)
    for i, (text, time, filename) in enumerate(qr_history[-5:], 1):  # Show last 5
        display_text = f"{text[:20]}..." if len(text) > 20 else text
        history_listbox.insert(tk.END, f"{i}. {display_text} ({time})")

def export_history():
    if not qr_history:
        messagebox.showerror("Error", "No QR codes to export!")
        return
    try:
        with open("qr_history_export.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Index", "Text", "Timestamp", "Filename"])
            for i, (text, time, filename) in enumerate(qr_history, 1):
                writer.writerow([i, text, time, filename or "Not downloaded"])
        messagebox.showinfo("Success", "History exported to qr_history_export.csv")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export history: {e}")

def on_generate():
    text = text_entry.get()
    size = size_map[size_var.get()]
    fill_color = fill_color_var.get()
    back_color = back_color_var.get()
    border = border_scale.get()
    
    img = generate_qr_code(text, size, fill_color, back_color, border)
    if img:
        # Resize for smaller preview (200x200)
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        qr_label.config(image=tk_img)
        qr_label.image = tk_img  # Keep reference to avoid garbage collection

def choose_fill_color():
    color = colorchooser.askcolor(title="Choose Fill Color")[1]
    if color:
        fill_color_var.set(color)
        fill_color_button.config(bg=color)

def choose_back_color():
    color = colorchooser.askcolor(title="Choose Background Color")[1]
    if color:
        back_color_var.set(color)
        back_color_button.config(bg=color)

def apply_theme(theme_name):
    theme = themes[theme_name]
    root.configure(bg=theme["bg"])
    main_frame.configure(bg=theme["bg"])
    style.configure("TCheckbutton", background=theme["bg"], foreground=theme["fg"])
    style.configure("TButton", background=theme["bg"], foreground=theme["fg"])
    style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
    text_entry.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
    history_listbox.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
    for widget in main_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=theme["bg"], fg=theme["fg"])

def create_tooltip(widget, text):
    tooltip = tk.Toplevel(root)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("+1000+1000")
    label = tk.Label(tooltip, text=text, bg="#FFFFE0", fg="black", relief="solid", borderwidth=1, font=("Helvetica", 10))
    label.pack()

    def show(event):
        x = widget.winfo_rootx() + 20
        y = widget.winfo_rooty() + 20
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def hide(event):
        tooltip.withdraw()

    widget.bind("<Enter>", show)
    widget.bind("<Leave>", hide)
    return tooltip

# Create the main window
root = tk.Tk()
root.title("Artsy QR Code Generator")
root.geometry("600x600")  # Reduced height due to smaller preview
root.resizable(False, False)
root.configure(bg=themes["Default"]["bg"])

# Style configuration
style = ttk.Style()
style.configure("TCheckbutton", background=themes["Default"]["bg"], foreground=themes["Default"]["fg"], font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TLabel", background=themes["Default"]["bg"], foreground=themes["Default"]["fg"])

# Main frame
main_frame = tk.Frame(root, bg=themes["Default"]["bg"])
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Title
tk.Label(main_frame, text="QR Code Generator", font=("Helvetica", 16, "bold"), bg=themes["Default"]["bg"], fg=themes["Default"]["fg"]).pack(pady=10)

# Theme selection
theme_var = tk.StringVar(value="Default")
theme_menu = ttk.OptionMenu(main_frame, theme_var, "Default", *themes.keys(), command=apply_theme)
theme_menu.pack(pady=5)
create_tooltip(theme_menu, "Select a theme for the app")

# Text input
tk.Label(main_frame, text="Enter Text or URL:", font=("Helvetica", 12), bg=themes["Default"]["bg"], fg=themes["Default"]["fg"]).pack()
text_entry = tk.Entry(main_frame, width=40, font=("Helvetica", 12), bg=themes["Default"]["entry_bg"], fg=themes["Default"]["entry_fg"])
text_entry.pack(pady=5)
create_tooltip(text_entry, "Enter text or URL for the QR code")

# Customization options
tk.Label(main_frame, text="Customize QR Code:", font=("Helvetica", 12), bg=themes["Default"]["bg"], fg=themes["Default"]["fg"]).pack(pady=5)

# Size selection
size_var = tk.StringVar(value="Medium")
size_menu = ttk.OptionMenu(main_frame, size_var, "Medium", "Small", "Medium", "Large")
size_menu.pack(pady=5)
create_tooltip(size_menu, "Select QR code size")

# Color selection
fill_color_var = tk.StringVar(value="black")
back_color_var = tk.StringVar(value="white")
color_frame = tk.Frame(main_frame, bg=themes["Default"]["bg"])
color_frame.pack(pady=5)
fill_color_button = tk.Button(color_frame, text="Fill Color", command=choose_fill_color, bg="black", fg="white")
fill_color_button.pack(side="left", padx=5)
create_tooltip(fill_color_button, "Choose QR code fill color")
back_color_button = tk.Button(color_frame, text="Background Color", command=choose_back_color, bg="white", fg="black")
back_color_button.pack(side="left", padx=5)
create_tooltip(back_color_button, "Choose QR code background color")

# Border size
tk.Label(main_frame, text="Border Size:", font=("Helvetica", 12), bg=themes["Default"]["bg"], fg=themes["Default"]["fg"]).pack()
border_scale = tk.Scale(main_frame, from_=1, to=10, orient="horizontal", bg=themes["Default"]["bg"], fg=themes["Default"]["fg"])
border_scale.set(4)  # Default border
border_scale.pack(pady=5)
create_tooltip(border_scale, "Adjust QR code border size")

# Buttons
button_frame = tk.Frame(main_frame, bg=themes["Default"]["bg"])
button_frame.pack(pady=10)
generate_button = ttk.Button(button_frame, text="Generate QR", command=on_generate)
generate_button.pack(side="left", padx=5)
create_tooltip(generate_button, "Generate and display QR code")
download_button = ttk.Button(button_frame, text="Download QR", command=download_qr_code)
download_button.pack(side="left", padx=5)
create_tooltip(download_button, "Download QR code as PNG")
export_button = ttk.Button(button_frame, text="Export History", command=export_history)
export_button.pack(side="left", padx=5)
create_tooltip(export_button, "Export QR code history as CSV")

# QR code preview
qr_label = tk.Label(main_frame, bg=themes["Default"]["bg"])
qr_label.pack(pady=10)
create_tooltip(qr_label, "QR code preview (200x200)")

# History panel
tk.Label(main_frame, text="QR Code History (Last 5):", font=("Helvetica", 12), bg=themes["Default"]["bg"], fg=themes["Default"]["fg"]).pack(pady=5)
history_frame = tk.Frame(main_frame, bg=themes["Default"]["bg"])
history_frame.pack(fill="x", padx=20)
scrollbar = tk.Scrollbar(history_frame, orient="vertical")
history_listbox = tk.Listbox(history_frame, width=40, height=5, font=("Helvetica", 10), bg=themes["Default"]["entry_bg"], fg=themes["Default"]["entry_fg"], yscrollcommand=scrollbar.set)
scrollbar.config(command=history_listbox.yview)
scrollbar.pack(side="right", fill="y")
history_listbox.pack(fill="x")
create_tooltip(history_listbox, "Last 5 generated QR codes")

# Auto-generate on launch
root.after(100, lambda: text_entry.insert(0, "https://example.com") or on_generate())

# Start the main loop
root.mainloop()
# QR-code-generator
# 🎨 Artsy QR Code Generator

A user-friendly QR code generator built using Python and Tkinter with support for customizable colors, themes, and exportable QR history.

---

## 📌 Features

- 🎯 Generate QR codes from any text or URL
- 🎨 Custom fill & background color selection
- 📐 QR size and border customization
- 🌓 Theme support: Default, Dark, Pastel
- 🖼️ Real-time QR code preview (200x200)
- 💾 Download QR code as PNG
- 📜 Save and export history as CSV
- 🧠 Tooltip hints for better UX

---

## 📷 GUI Preview

<img width="602" height="634" alt="image" src="https://github.com/user-attachments/assets/00bd0c36-c2f3-4481-bbed-f6ea5fdbf772" />


---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** – for the GUI
- **qrcode** – for QR generation
- **Pillow (PIL)** – for image rendering
- **CSV** – to export QR history

---

## 📦 Installation

1. **Clone the repo**

```bash
git clone https://github.com/your-username/qr-code-generator.git
cd qr-code-generator
Install dependencies


-------pip install qrcode[pil]------
Note: Pillow is automatically included in the above command.

🚀 Run the App
-------python main.py--------------
The GUI will launch automatically with an example QR code.

📁 Output
All generated QR codes are saved under the qrcodes/ folder.

QR generation history can be exported to qr_history_export.csv.

📌 How it Works
User enters a URL or text.

Customizes the QR:

Size (Small, Medium, Large)

Colors (fill & background)

Border width

Clicks Generate QR

Preview appears instantly.

Optionally, clicks Download to save as image.

Export History saves all generated QR details to a CSV file.

🧪 Validations & Error Handling
Empty text input alert

Prevents duplicate downloads

Catch-all try-except for image saving/export errors

🔐 Security Considerations
Local execution (no network calls)

Input sanitized before processing

OS-safe file saving

🚧 Known Limitations
Logo embedding not yet supported

No QR scanner support (future enhancement)

Output folder path is hardcoded as qrcodes/

📈 Future Improvements
Add logo inside QR code

QR code scanning feature

Support PDF or SVG export

Drag & drop text input

🙋‍♂️ Author
Pradeep
📧 Optional: pradeepsworld775@gmail.com
🌐 Optional: 

📝 License
This project is open-source under the MIT License.

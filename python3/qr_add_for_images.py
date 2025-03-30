import qrcode
from PIL import Image, ImageDraw, ImageEnhance
import tkinter as tk
from tkinter import filedialog, messagebox

def generate_stealth_qr():
    url = url_entry.get()
    image_path = image_path_label.cget("text")
    opacity = float(opacity_slider.get()) / 100
    position = (int(x_entry.get()), int(y_entry.get()))
    qr_size = int(size_entry.get())
    
    try:
        # 1. Generar QR
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=0)
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="white", back_color="black").convert("RGBA")
        
        # 2. Redimensionar y ajustar opacidad
        qr_img = qr_img.resize((qr_size, qr_size))
        alpha = qr_img.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        qr_img.putalpha(alpha)
        
        # 3. Cargar imagen de fondo
        background = Image.open(image_path)
        
        # Convertir a RGBA si es JPEG
        if background.mode != 'RGBA':
            background = background.convert("RGBA")
        
        # 4. Pegar QR
        background.paste(qr_img, position, qr_img)
        
        # 5. Guardar en formato compatible
        output_path = f"stealth_qr_{image_path.split('/')[-1].split('.')[0]}.png"
        background.save(output_path, format="PNG")  # Forzamos PNG para preservar transparencia
        
        result_label.config(text=f"QR generado en: {output_path}")
        background.show()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}\nSolución: Usa PNG para transparencia o JPEG sin alpha")

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if file_path:
        image_path_label.config(text=file_path)

# Configuración de la interfaz
app = tk.Tk()
app.title("Generador de QR Stealth - Stay Gold Crypto")
app.geometry("500x400")

# Campos de entrada
tk.Label(app, text="URL:").pack()
url_entry = tk.Entry(app, width=50)
url_entry.pack()
url_entry.insert(0, "https://staygoldcrypto.com/main")

tk.Label(app, text="Imagen de fondo:").pack()
image_path_label = tk.Label(app, text="", fg="blue")
image_path_label.pack()
tk.Button(app, text="Seleccionar imagen", command=select_image).pack()

tk.Label(app, text="Posición (X,Y):").pack()
position_frame = tk.Frame(app)
position_frame.pack()
x_entry = tk.Entry(position_frame, width=5)
x_entry.pack(side=tk.LEFT)
x_entry.insert(0, "100")
tk.Label(position_frame, text=",").pack(side=tk.LEFT)
y_entry = tk.Entry(position_frame, width=5)
y_entry.pack(side=tk.LEFT)
y_entry.insert(0, "100")

tk.Label(app, text="Tamaño QR (px):").pack()
size_entry = tk.Entry(app, width=5)
size_entry.pack()
size_entry.insert(0, "200")

tk.Label(app, text="Opacidad (0-100%):").pack()
opacity_slider = tk.Scale(app, from_=5, to=100, orient=tk.HORIZONTAL)
opacity_slider.set(30)
opacity_slider.pack()

# Botón de generación
generate_btn = tk.Button(app, text="Generar QR Stealth", command=generate_stealth_qr)
generate_btn.pack(pady=20)

# Resultado
result_label = tk.Label(app, text="", fg="green")
result_label.pack()

app.mainloop()

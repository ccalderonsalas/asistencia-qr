import os
import pandas as pd
import qrcode
import urllib.parse

# URL base del formulario de Google (reemplaza con tu enlace real)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScv6cazqFQBkeQTrz9upAyth4Kl8Rj2HTFOTOPb5zJ1IM_AVQ/formResponse"

# Campos del formulario
ENTRY_NOMBRE = "entry.29459669"
ENTRY_GRUPO = "entry.429982578"

# Leer datos de estudiantes desde CSV
df = pd.read_csv("estudiantes.csv")

# Carpetas base de salida
html_base = os.path.join("docs", "html")
qr_base = os.path.join("docs", "qrs")

# Crear carpetas base si no existen
os.makedirs(html_base, exist_ok=True)
os.makedirs(qr_base, exist_ok=True)

for _, row in df.iterrows():
    nombre = row["nombre"].strip()
    grupo = row["grupo"].strip()

    # Sanitizar nombre para nombre de archivo (sin espacios, acentos o caracteres especiales)
    nombre_archivo = (
        nombre.upper()
        .replace("Á", "A").replace("É", "E").replace("Í", "I")
        .replace("Ó", "O").replace("Ú", "U").replace("Ñ", "N")
        .replace("Ü", "U").replace(" ", "_")
    )

    # Crear carpetas por grupo
    html_dir = os.path.join(html_base, grupo)
    qr_dir = os.path.join(qr_base, grupo)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(qr_dir, exist_ok=True)

    # Codificar nombre para envío por formulario
    nombre = urllib.parse.quote(nombre)

    # Crear contenido HTML
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Registro de asistencia</title>
</head>
<body>
  <h1>Hola, {nombre}</h1>
  <p>Haz clic en el botón para registrar tu asistencia.</p>
  <form action="{FORM_URL}" method="post" target="_self" onsubmit="this.style.display='none'; document.getElementById('mensaje').style.display='block'">
    <input type="hidden" name="{ENTRY_NOMBRE}" value="{nombre}">
    <input type="hidden" name="{ENTRY_GRUPO}" value="{grupo}">
    <input type="submit" value="Registrar asistencia">
  </form>
  <div id="mensaje" style="display:none;">
    <h3>✅ ¡Asistencia registrada con éxito!</h3>
    <p>Gracias, {nombre}. Puedes cerrar esta página.</p>
  </div>
</body>
</html>
"""

    # Guardar archivo HTML
    html_path = os.path.join(html_dir, f"{nombre_archivo}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Crear URL del archivo HTML para el QR
    url = f"https://ccalderonsalas.github.io/asistencia-qr/html/{grupo}/{nombre_archivo}.html"

    # Generar y guardar código QR
    qr = qrcode.make(url)
    qr_path = os.path.join(qr_dir, f"{nombre_archivo}.png")
    qr.save(qr_path)

print("✅ ¡Todo listo! HTMLs y QRs generados correctamente.")

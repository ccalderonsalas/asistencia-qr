import csv
import os
import qrcode

# HTML base
TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Registro de asistencia</title>
</head>
<body>
  <h1>Hola, {{ nombre }}</h1>
  <p>Haz clic en el botón para registrar tu asistencia.</p>
  <form action="https://docs.google.com/forms/d/e/1FAIpQLScv6cazqFQBkeQTrz9upAyth4Kl8Rj2HTFOTOPb5zJ1IM_AVQ/formResponse" method="post" target="_self" onsubmit="this.style.display='none'; document.getElementById('mensaje').style.display='block'">
    <input type="hidden" name="entry.29459669" value="{{ nombre }}">
    <input type="hidden" name="entry.429982578" value="{{ grupo }}">
    <input type="submit" value="Registrar asistencia">
  </form>

  <div id="mensaje" style="display:none;">
    <h3>✅ ¡Asistencia registrada con éxito!</h3>
    <p>Gracias, {{ nombre }}. Puedes cerrar esta página.</p>
  </div>
</body>
</html>
"""



def crear_archivos_estudiantes(nombre_archivo):
    with open(nombre_archivo, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            grupo = fila['Grupo'].replace(" ", "").strip()
            nombre = fila['Nombre'].replace(" ", "_").upper().strip()

            # Carpetas de salida
            output_dir = os.path.join(".", grupo)
            qr_dir = os.path.join("qrs", grupo)
            os.makedirs(output_dir, exist_ok=True)
            os.makedirs(qr_dir, exist_ok=True)

            # Ruta del archivo HTML
            html_path = os.path.join(output_dir, f"{nombre}.html")

            # Reemplazar plantilla
            contenido = TEMPLATE.replace("{{ nombre }}", fila['Nombre'])

            # Guardar archivo HTML
            with open(html_path, "w", encoding="utf-8") as archivo_html:
                archivo_html.write(contenido)

            # Generar URL pública
            url = f"https://ccalderonsalas.github.io/asistencia-qr/{grupo}/{nombre}.html"

            # Generar código QR
            qr_path = os.path.join(qr_dir, f"{nombre}.png")
            qr = qrcode.make(url)
            qr.save(qr_path)

if __name__ == "__main__":
    crear_archivos_estudiantes("estudiantes.csv")

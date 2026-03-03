"""
PROYECTO: Extractor MEC - MODO DIRECTO
MOTOR: Python (pdfplumber) únicamente.
USO: Para archivos que ya tienen un OCR de alta calidad.
"""

from src.lector import extraer_texto_de_pdf  # Importamos solo la extracción directa
from src.conversor import conversor_csv
from src.exportador import csv_a_excel 
import os

def ejecutar_directo():
    # Ruta del archivo (puedes cambiarla según necesites)
    ruta_pdf = "/home/hugo/Descargas/angel.pdf"
    
    if not os.path.exists(ruta_pdf):
        print(f"❌ El archivo no existe en: {ruta_pdf}")
        return

    # Preparación de nombres
    nombre_base = os.path.basename(ruta_pdf).replace(".pdf", "").replace(" ", "_")
    nombre_txt = f"{nombre_base}_directo.txt"
    nombre_csv = f"{nombre_base}_directo.csv"

    print(f"\n⚡ --- Iniciando PROCESO DIRECTO para: {nombre_base} ---")

    # 1. Extracción directa (sin pasar por OCRmyPDF)
    # Aquí confiamos en la capa de texto que ya trae el PDF
    texto = extraer_texto_de_pdf(ruta_pdf)
    
    if texto and len(texto.strip()) > 0:
        # Guardar respaldo en TXT
        with open(nombre_txt, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"✓ TXT generado (lectura directa): {nombre_txt}")
        
        # 2. Conversión a CSV
        conversor_csv(nombre_txt)
        
        # 3. Exportación a Excel
        if os.path.exists(nombre_csv):
            csv_a_excel(nombre_csv)
            print(f"✅ Excel creado con éxito (Modo Directo).")
        else:
            print(f"⚠️ No se generó el CSV, revisa la marca de corte en el TXT.")
            
    else:
        print("❌ Error: El PDF no tiene texto extraíble o está vacío.")

if __name__ == "__main__":
    ejecutar_directo()
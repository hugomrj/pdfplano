"""
PROYECTO: Extractor de Ingresos del Personal (MEC)
MOTOR: Linux (OCRmyPDF) + Python (pdfplumber)
REQUERIMIENTOS: sudo apt install ocrmypdf tesseract-ocr-spa unpaper
"""
from src.lector import procesar_documento_completo  # Nombre de la nueva función orquestadora
from src.conversor import conversor_csv
from src.exportador import csv_a_excel 
import os

def ejecutar():
    # Ruta del archivo
    ruta_pdf = "/home/hugo/Descargas/1318-2025-RAMIREZ (1).pdf"
    
    if not os.path.exists(ruta_pdf):
        print(f"❌ El archivo no existe en: {ruta_pdf}")
        return

    # Definición de nombres de archivos (quitamos espacios para evitar líos en Linux)
    nombre_base = os.path.basename(ruta_pdf).replace(".pdf", "").replace(" ", "_")
    nombre_txt = f"{nombre_base}.txt"
    nombre_csv = f"{nombre_base}.csv"

    print(f"\n--- Iniciando proceso para: {nombre_base} ---")

    # 1. Ejecutar el flujo completo de lectura:
    # (optimizar_pdf_con_ocr -> extraer_texto_de_anexo)
    texto = procesar_documento_completo(ruta_pdf)
    
    if texto:
        # Guardar el respaldo en TXT
        with open(nombre_txt, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"✓ TXT generado: {nombre_txt}")
        
        # 2. Limpiar y convertir a CSV
        conversor_csv(nombre_txt)
        
        # 3. Convertir el CSV resultante a Excel
        if os.path.exists(nombre_csv):
            csv_a_excel(nombre_csv)
            print(f"✅ Excel creado con éxito.")
        else:
            print(f"⚠️ No se encontró {nombre_csv}")
            
    else:
        print("❌ Error: No se pudo extraer texto del documento.")

if __name__ == "__main__":
    ejecutar()


    
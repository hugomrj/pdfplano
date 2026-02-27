from src.lector import extraer_desde_anexo
from src.conversor import conversor_csv
import os

def ejecutar():
    ruta_pdf = "/home/hugo/Documentos/mec/RESOLUCIONES DE INGRESOS/2025/08/1318-2025-RAMIREZ.pdf"
    nombre_txt = os.path.basename(ruta_pdf).replace(".pdf", ".txt")

    # 1. Extraer (OCR)
    texto = extraer_desde_anexo(ruta_pdf)
    
    if texto:
        with open(nombre_txt, "w", encoding="utf-8") as f:
            f.write(texto)
        
        # 2. Limpiar y convertir a CSV
        conversor_csv(nombre_txt)
    else:
        print("No se encontró la marca de corte.")

if __name__ == "__main__":
    ejecutar()
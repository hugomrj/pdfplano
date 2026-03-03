import subprocess
import pdfplumber
import os
import re

# Tu marca de corte original
MARCA_DE_CORTE = r"ANEXO.*INGRESOS.*PERSONAL"

def optimizar_pdf_con_ocr(ruta_pdf_original):
    # Usamos el nombre original pero le añadimos el sufijo
    nombre_archivo = os.path.basename(ruta_pdf_original).replace(".pdf", "_OPTIMIZADO.pdf")
    # Es mejor crear el temporal en la misma carpeta o en /tmp
    ruta_optimizado = os.path.join(os.path.dirname(ruta_pdf_original), nombre_archivo)
    
    print(f"🧹 Optimizando imagen y aplicando OCR (Linux)...")
    
    comando = [
        "ocrmypdf",
        "--language", "spa",
        "--deskew",
        "--clean",
        "--rotate-pages",
        "--force-ocr",
        "--jobs", "4",  # <--- IMPORTANTE: Usa 4 núcleos para ir más rápido
        ruta_pdf_original,
        ruta_optimizado
    ]
    
    try:
        subprocess.run(
            comando, 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        return ruta_optimizado
    except Exception as e:
        print(f"❌ Error en el motor Linux: {e}")
        return None





def extraer_texto_de_pdf(ruta_pdf):
    print(f"📄 Extrayendo datos con pdfplumber: {os.path.basename(ruta_pdf)}")
    
    lineas_limpias = []
    disparador_encontrado = False

    with pdfplumber.open(ruta_pdf) as pdf:
        for i, pagina in enumerate(pdf.pages):
            texto_pagina = pagina.extract_text(layout=True)
            
            if not texto_pagina:
                continue

            # Dividimos el texto de la página en líneas para procesarlas una a una
            for linea in texto_pagina.split('\n'):
                # Eliminamos espacios en blanco al inicio y al final de la línea
                linea_procesada = linea.strip()
                
                # Omitimos líneas que quedaron vacías o que son solo números de página
                if not linea_procesada or "Página" in linea_procesada:
                    continue

                if not disparador_encontrado:
                    # Buscamos la marca de corte en la línea limpia
                    match = re.search(MARCA_DE_CORTE, linea_procesada, re.IGNORECASE)
                    if match:
                        print(f"🎯 Marca de corte encontrada en página {i+1}")
                        disparador_encontrado = True
                        lineas_limpias.append(linea_procesada)
                else:
                    # Filtro extra: Solo agregamos líneas que tengan contenido real
                    # (evita líneas que son solo puntos ........ o rayas ------)
                    if len(re.findall(r'\w', linea_procesada)) > 2:
                        lineas_limpias.append(linea_procesada)

    # Retornamos todo el texto unido por saltos de línea, ya sin espacios al inicio
    return "\n".join(lineas_limpias)






def procesar_documento_completo(ruta_pdf_inicial):
    # 1. Limpieza con Linux
    ruta_limpia = optimizar_pdf_con_ocr(ruta_pdf_inicial)
    
    if not ruta_limpia:
        return None
        
    # 2. Extracción con Python
    texto_final = extraer_texto_de_pdf(ruta_limpia)
    
    # 3. Auto-limpieza de disco
    if ruta_limpia and os.path.exists(ruta_limpia):
        os.remove(ruta_limpia)
        
    return texto_final



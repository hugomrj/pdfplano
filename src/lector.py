import pytesseract
from pdf2image import convert_from_path
import re

# ==========================================================
# CONFIGURACIÓN DE MARCA DE CORTE (Modifica esto cuando quieras)
# ==========================================================
# El patrón busca: ANEXO + cualquier cosa + INGRESOS + cualquier cosa + PERSONAL
MARCA_DE_CORTE = r"ANEXO.*INGRESOS.*PERSONAL"
# ==========================================================

def extraer_desde_anexo(ruta_pdf):
    print(f"Analizando documento: {ruta_pdf}")
    
    # Convertir a imágenes
    paginas = convert_from_path(ruta_pdf, 300)
    
    texto_acumulado = ""
    disparador_encontrado = False

    for i, pagina in enumerate(paginas):
        print(f"Escaneando página {i+1}...")
        texto_pagina = pytesseract.image_to_string(pagina, lang='spa')
        
        if not disparador_encontrado:
            # Buscamos la marca de corte definida arriba
            match = re.search(MARCA_DE_CORTE, texto_pagina, re.IGNORECASE)
            
            if match:
                print(f"¡Punto de inicio encontrado en página {i+1}!")
                disparador_encontrado = True
                
                # Cortamos exactamente donde empieza la coincidencia del patrón
                punto_inicio = match.start()
                texto_acumulado += texto_pagina[punto_inicio:]
        else:
            # Una vez activado, acumulamos el resto de páginas
            texto_acumulado += texto_pagina

    return texto_acumulado



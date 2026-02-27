import csv
import re
import os

def conversor_csv(ruta_txt):
    ruta_csv = ruta_txt.replace(".txt", ".csv")
    
    with open(ruta_txt, "r", encoding="utf-8") as f:
        # Cargamos líneas ignorando las que dicen "Página" o están vacías
        lineas = [l.strip() for l in f.readlines() if l.strip() and "Página" not in l]

    datos_limpios = []
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        
        # Buscamos el patrón de Cédula (ej: 2.584.593)
        match_cedula = re.search(r"(\d{1,3}(?:\.\d{3}){2})", linea)
        
        if match_cedula:
            try:
                cedula = match_cedula.group(1)
                
                # Buscamos la fecha (01/08/2025) como ancla
                match_fecha = re.search(r"\d{2}/\d{2}/\d{4}", linea)
                
                if match_fecha:
                    pos_cedula_fin = linea.find(cedula) + len(cedula)
                    pos_fecha_inicio = match_fecha.start()
                    pos_fecha_fin = match_fecha.end()
                    
                    # El nombre está entre la cédula y la fecha
                    nombre = linea[pos_cedula_fin:pos_fecha_inicio].strip()
                    
                    # La escuela empieza después de la fecha + algunos códigos 
                    # (saltamos unos 15 caracteres para evitar los IDs numéricos pegados a la fecha)
                    resto_linea = linea[pos_fecha_fin:].strip()
                    escuela = re.sub(r"^\d+\s+\d+\s+", "", resto_linea) # Limpiamos códigos iniciales
                else:
                    nombre = "Error en formato"
                    escuela = "Error en formato"

                # --- Línea 2: Cargo (justo debajo) ---
                cargo_limpio = "No encontrado"
                if i + 1 < len(lineas):
                    linea_siguiente = lineas[i+1]
                    # Si la línea siguiente NO tiene otra cédula, es el cargo
                    if not re.search(r"(\d{1,3}(?:\.\d{3}){2})", linea_siguiente):
                        # Limpiamos el número de orden y el texto repetitivo
                        cargo_limpio = re.sub(r"^\d+\s+INTERINO SIN CONCURSO\s+-\s+-\s+", "", linea_siguiente)
                        i += 1 # Consumimos la línea del cargo

                datos_limpios.append({
                    "Cedula": cedula,
                    "Nombre": nombre,
                    "Escuela": escuela,
                    "Cargo": cargo_limpio
                })

            except Exception as e:
                print(f"Error procesando registro en línea {i}: {e}")
        
        i += 1

    # Guardar resultados
    if datos_limpios:
        columnas = ["Cedula", "Nombre", "Escuela", "Cargo"]
        with open(ruta_csv, "w", encoding="utf-8", newline="") as f_csv:
            writer = csv.DictWriter(f_csv, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(datos_limpios)
        print(f"✓ Conversión exitosa: {len(datos_limpios)} registros en {ruta_csv}")
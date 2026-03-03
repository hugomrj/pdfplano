import csv
import re
import os

def conversor_csv(ruta_txt):
    ruta_csv = ruta_txt.replace(".txt", ".csv")
    
    with open(ruta_txt, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]

    datos_finales = []
    regex_numeros = r"(\d{1,3}(?:\.\d{3}){1,2})" 
    regex_fecha = r"(\d{2}/\d{2}/\d{4})"

    i = 0
    while i < len(lineas):
        linea = lineas[i]
        
        if "Página" in linea or "ANEXO" in linea or "Exped." in linea or "Ordenl" in linea:
            i += 1
            continue

        matches_numeros = re.findall(regex_numeros, linea)
        match_fecha = re.search(regex_fecha, linea)

        if len(matches_numeros) >= 2 and match_fecha:
            try:
                # 1. Cédula y Fecha
                cedula_con_puntos = matches_numeros[1]
                cedula = cedula_con_puntos.replace(".", "")
                fecha = match_fecha.group(1)
                
                # 2. Nombre
                idx_cedula_fin = linea.find(cedula_con_puntos) + len(cedula_con_puntos)
                idx_fecha_inicio = match_fecha.start()
                nombre = linea[idx_cedula_fin:idx_fecha_inicio].strip()

                # 3. Bloque después de la fecha
                bloque_final = linea[match_fecha.end():].strip()
                
                # --- NUEVO: CPuesto (Primer bloque numérico después de la fecha) ---
                match_puesto = re.search(r"^(\d+)", bloque_final)
                cpuesto = match_puesto.group(1) if match_puesto else ""
                
                # Asignación: último número con puntos de la línea
                match_monto = re.search(r"(\d{1,3}(?:\.\d{3}){1,2})$", linea)
                asignacion = match_monto.group(1).replace(".", "") if match_monto else ""
                
                # Categoría
                match_cat = re.search(r"\b(LCE|ZZ\d|LCH|Z\d\d|ZZ\d\d)\b", bloque_final)
                categoria = match_cat.group(1) if match_cat else ""
                
                # Turno
                match_turno = re.search(r"\s(M|T|MT|N)\s", bloque_final)
                turno = match_turno.group(1) if match_turno else ""

                # 4. Capturar el Orden
                orden = ""
                if i + 1 < len(lineas):
                    proxima = lineas[i+1]
                    match_orden = re.match(r"^(\d+)\s?º?$", proxima)
                    if match_orden:
                        orden = match_orden.group(1)
                        i += 1 

                datos_finales.append({
                    "Orden": orden,
                    "Cedula": cedula,
                    "Nombre": nombre,
                    "Antiguedad": fecha,
                    "CPuesto": cpuesto, # <--- Nuevo campo
                    "Turno": turno,
                    "Categoria": categoria,
                    "Asignacion": asignacion,
                    "Raw": bloque_final[:50] 
                })

            except Exception as e:
                print(f"⚠️ Error procesando línea: {linea[:30]}... -> {e}")

        i += 1

    if datos_finales:
        # Definimos las columnas incluyendo el nuevo campo CPuesto
        columnas = ["Orden", "Cedula", "Nombre", "Antiguedad", "CPuesto", "Turno", "Categoria", "Asignacion", "Raw"]
        
        with open(ruta_csv, "w", encoding="utf-8", newline="") as f:
            # delimiter=';' para que Excel lo abra bien por defecto
            writer = csv.DictWriter(f, fieldnames=columnas, delimiter=';', extrasaction='ignore')
            writer.writeheader()
            writer.writerows(datos_finales)
        print(f"✅ Proceso completo: {len(datos_finales)} registros en {ruta_csv}")
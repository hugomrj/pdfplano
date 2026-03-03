import pandas as pd
import os

def csv_a_excel(ruta_csv):
    """Convierte un CSV de ingresos del personal a un archivo Excel (.xlsx)"""
    try:
        ruta_excel = ruta_csv.replace(".csv", ".xlsx")
        # Leemos el CSV con el separador que usaste (punto y coma)
        df = pd.read_csv(ruta_csv, sep=';', encoding='utf-8')
        
        # Guardamos a Excel usando el motor openpyxl
        df.to_excel(ruta_excel, index=False, engine='openpyxl')
        print(f"📊 Proceso finalizado. Excel creado: {ruta_excel}")
        
    except Exception as e:
        print(f"❌ Error al exportar a Excel: {e}")
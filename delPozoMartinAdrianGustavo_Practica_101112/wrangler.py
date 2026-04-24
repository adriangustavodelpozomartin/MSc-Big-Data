#!/usr/bin/env python
# coding: utf-8

# In[120]:


import json
import csv
import os
import logging
import re

# 📋 Configurar logging
logging.basicConfig(
    filename='wrangler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# 🛠️ Cargar diccionario de traducciones
def cargar_traducciones(ruta_diccionario):
    """
    Carga el diccionario de traducciones desde un archivo JSON.
    Parámetros:
        - ruta_diccionario (str): Ruta al archivo JSON de traducciones.
    Retorna:
        - dict: Diccionario con las traducciones.
    """
    try:
        with open(ruta_diccionario, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error cargando traducciones: {e}")
        return {"sociedades": {}, "vias": {}}


# 🛠️ Extraer provincia del nombre del archivo
def extraer_provincia_desde_nombre(json_path):
    """
    Extrae la provincia del nombre del archivo JSON.
    Parámetros:
        - json_path (str): Ruta al archivo JSON.
    Retorna:
        - provincia (str): Provincia extraída.
    """
    try:
        nombre_archivo = os.path.basename(json_path)
        partes = nombre_archivo.split('_')
        if len(partes) > 2:
            return partes[2].split('.')[0].capitalize()
        else:
            return 'desconocida'
    except Exception as e:
        logging.error(f"Error al extraer la provincia: {e}")
        return 'desconocida'


# 🛠️ Procesar un archivo JSON del Crawler
def procesar_wrangler(json_path, output_dir, diccionario_traducciones):
    """
    Procesa un archivo JSON del Crawler y guarda un CSV con los datos estructurados.
    Parámetros:
        - json_path (str): Ruta al archivo JSON del Crawler.
        - output_dir (str): Directorio de salida para el CSV.
        - diccionario_traducciones (dict): Diccionario con las traducciones.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            empresas = json.load(f)
    except Exception as e:
        logging.error(f"Error al leer el archivo JSON: {e}")
        return

    provincia = extraer_provincia_desde_nombre(json_path)
    resultado = []

    for empresa in empresas:
        try:
            # ✅ Filtrar solo las empresas con Acto legal "Constitución"
            if empresa.get('Acto legal', '').lower() != 'constitución':
                continue

            # ✅ Extraer los datos necesarios
            nombre = empresa.get('Nombre', '').upper()
            tipo_sociedad = diccionario_traducciones['sociedades'].get(
                re.search(r'\b(SL|SA|SLL|SC|SLP)\b', nombre).group(0), 'desconocido'
            ) if re.search(r'\b(SL|SA|SLL|SC|SLP)\b', nombre) else 'desconocido'
            
            comienzo_operaciones = empresa.get('Comienzo de operaciones', '')
            capital_social = empresa.get('Capital', '').replace('.', '').replace(',', '.')
            capital_social = float(capital_social) if capital_social else None
            
            domicilio_completo = empresa.get('Domicilio', '')
            tipo_via_match = re.match(r'(C/|CALLE|AVDA|PLAZA|PASEO|CAMINO|CTRA|CMNO|TRVA)', domicilio_completo)
            tipo_via = diccionario_traducciones['vias'].get(tipo_via_match.group(0), 'desconocido') if tipo_via_match else 'desconocido'
            
            # ✅ Mejorar extracción del nombre de la vía
            nombre_via_match = re.search(
                r'(C/|CALLE|AVDA|PLAZA|PASEO|CAMINO|CTRA|CMNO|TRVA)\s+(.+?)\s+(?=\d+|S/N|Km\s\d+(?:,\d+)?|\()',
                domicilio_completo
            )
            nombre_via = nombre_via_match.group(2) if nombre_via_match else 'desconocido'
            
            # ✅ Extraer número, "S/N" o "Km X,XXX"
            numero_match = re.search(r'(Km\s\d+(?:,\d+)?|\d+|S/N)', domicilio_completo)
            numero = numero_match.group(0) if numero_match else 'desconocido'
            
            # ✅ Extraer ciudad (entre paréntesis)
            ciudad_match = re.search(r'\((.*?)\)', domicilio_completo)
            ciudad = ciudad_match.group(1) if ciudad_match else 'desconocida'
            
            resultado.append({
                'Nombre': nombre,
                'TipoDeSociedad': tipo_sociedad,
                'ComienzoDeOperaciones': comienzo_operaciones,
                'CapitalSocial': capital_social,
                'DomicilioCompleto': domicilio_completo,
                'TipoDeVia': tipo_via,
                'NombreDeVia': nombre_via,
                'Numero': numero,
                'Ciudad': ciudad,
                'Provincia': provincia
            })

        except Exception as e:
            logging.error(f"Error al procesar una empresa: {e}")

    # 📊 Guardar el resultado en CSV con separador ';'
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'empresas_septiembre.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'Nombre', 'TipoDeSociedad', 'ComienzoDeOperaciones', 'CapitalSocial',
            'DomicilioCompleto', 'TipoDeVia', 'NombreDeVia', 'Numero', 'Ciudad', 'Provincia'
        ], delimiter=';')
        writer.writeheader()
        writer.writerows(resultado)

    logging.info(f"Datos guardados correctamente en {csv_path}")

# 🛠️ Función para procesar una carpeta con archivos JSON
def procesar_carpeta_wrangler(input_dir, output_dir, diccionario_traducciones):
    """
    Procesa todos los archivos JSON de una carpeta y guarda un único CSV consolidado.
    Parámetros:
        - input_dir (str): Ruta a la carpeta con archivos JSON.
        - output_dir (str): Directorio de salida para el CSV.
        - diccionario_traducciones (dict): Diccionario con las traducciones.
    """
    resultado_total = []

    # ✅ Recorrer todos los archivos en la carpeta
    for archivo in os.listdir(input_dir):
        if archivo.endswith('.json'):
            json_path = os.path.join(input_dir, archivo)
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    empresas = json.load(f)
                
                provincia = extraer_provincia_desde_nombre(json_path)

                for empresa in empresas:
                    try:
                        # ✅ Filtrar solo las empresas con Acto legal "Constitución"
                        if empresa.get('Acto legal', '').lower() != 'constitución':
                            continue

                        nombre = empresa.get('Nombre', '').upper()
                        tipo_sociedad = diccionario_traducciones['sociedades'].get(
                            re.search(r'\b(SL|SA|SLL|SC|SLP)\b', nombre).group(0), 'desconocido'
                        ) if re.search(r'\b(SL|SA|SLL|SC|SLP)\b', nombre) else 'desconocido'
                        
                        comienzo_operaciones = empresa.get('Comienzo de operaciones', '')
                        capital_social = empresa.get('Capital', '').replace('.', '').replace(',', '.')
                        capital_social = float(capital_social) if capital_social else None
                        
                        domicilio_completo = empresa.get('Domicilio', '')
                        tipo_via_match = re.match(r'(C/|CALLE|AVDA|PLAZA|PASEO|CAMINO|CTRA|CMNO|TRVA)', domicilio_completo)
                        tipo_via = diccionario_traducciones['vias'].get(tipo_via_match.group(0), 'desconocido') if tipo_via_match else 'desconocido'
                        
                        nombre_via_match = re.search(
                            r'(C/|CALLE|AVDA|PLAZA|PASEO|CAMINO|CTRA|CMNO|TRVA)\s+(.+?)\s+(?=\d+|S/N|Km\s\d+(?:,\d+)?|\()',
                            domicilio_completo
                        )
                        nombre_via = nombre_via_match.group(2) if nombre_via_match else 'desconocido'
                        
                        numero_match = re.search(r'(Km\s\d+(?:,\d+)?|\d+|S/N)', domicilio_completo)
                        numero = numero_match.group(0) if numero_match else 'desconocido'
                        
                        ciudad_match = re.search(r'\((.*?)\)', domicilio_completo)
                        ciudad = ciudad_match.group(1) if ciudad_match else 'desconocida'
                        
                        resultado_total.append({
                            'Nombre': nombre,
                            'TipoDeSociedad': tipo_sociedad,
                            'ComienzoDeOperaciones': comienzo_operaciones,
                            'CapitalSocial': capital_social,
                            'DomicilioCompleto': domicilio_completo,
                            'TipoDeVia': tipo_via,
                            'NombreDeVia': nombre_via,
                            'Numero': numero,
                            'Ciudad': ciudad,
                            'Provincia': provincia
                        })

                    except Exception as e:
                        logging.error(f"Error al procesar una empresa en {json_path}: {e}")
            
            except Exception as e:
                logging.error(f"Error al procesar el archivo JSON {json_path}: {e}")

    # 📊 Guardar el resultado consolidado en un único archivo CSV
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'empresas_septiembre_2024.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'Nombre', 'TipoDeSociedad', 'ComienzoDeOperaciones', 'CapitalSocial',
            'DomicilioCompleto', 'TipoDeVia', 'NombreDeVia', 'Numero', 'Ciudad', 'Provincia'
        ], delimiter=';')
        writer.writeheader()
        writer.writerows(resultado_total)

    logging.info(f"Datos consolidados guardados correctamente en {csv_path}")
    print(f"✅ Datos consolidados guardados en {csv_path}")


# 🛠️ Función principal para la fase Wrangler
def wrangler_main(filepath, output_dir, ruta_diccionario):
    """
    Punto de entrada para la fase Wrangler.
    Parámetros:
        - filepath (str): Ruta al archivo JSON o carpeta con archivos JSON.
        - output_dir (str): Directorio donde se guardará el CSV.
        - ruta_diccionario (str): Ruta al archivo JSON con el diccionario de traducciones.
    """
    # ✅ Cargar diccionario de traducciones
    diccionario_traducciones = cargar_traducciones(ruta_diccionario)
    
    if not diccionario_traducciones:
        print("❌ Error: No se pudo cargar el diccionario de traducciones.")
        return
    
    # ✅ Procesar archivo o carpeta
    if os.path.isfile(filepath):
        logging.info(f"Fase Wrangler: Procesando archivo JSON {filepath}")
        procesar_wrangler(filepath, output_dir, diccionario_traducciones)
    elif os.path.isdir(filepath):
        logging.info(f"Fase Wrangler: Procesando carpeta de archivos JSON {filepath}")
        procesar_carpeta_wrangler(filepath, output_dir, diccionario_traducciones)
    else:
        logging.error("❌ La ruta proporcionada no es válida. Debe ser un archivo JSON o una carpeta.")
        print("❌ La ruta proporcionada no es válida. Debe ser un archivo JSON o una carpeta.")


# In[ ]:





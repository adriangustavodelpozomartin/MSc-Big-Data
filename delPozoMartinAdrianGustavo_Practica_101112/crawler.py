#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import re
import json
import logging
from pdfminer.high_level import extract_text

# 📋 Configurar logging
logging.basicConfig(
    filename='crawler.log',  # Archivo donde se guardarán los logs
    level=logging.INFO,  # Nivel de log (INFO, ERROR, WARNING, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato del mensaje
)


# 🛠️ Función para extraer texto de un PDF
def extraer_texto(pdf_path):
    """
    Extrae y limpia el texto de un archivo PDF.
    
    Parámetros:
        - pdf_path (str): Ruta al archivo PDF.
    
    Retorna:
        - texto (str): Texto extraído y limpiado del PDF.
    """
    try:
        # Extraer el texto del archivo PDF
        texto = extract_text(pdf_path)
        logging.info(f"Texto extraído correctamente del archivo: {pdf_path}")
    except Exception as e:
        # Registrar el error si no se pudo extraer el texto
        logging.error(f"Error extrayendo texto del archivo {pdf_path}: {e}")
        return None

    # 🛡️ Limpieza del texto
    patrones_a_eliminar = [
        r'BOLETÍN OFICIAL DEL REGISTRO MERCANTIL.*',  # Encabezado principal
        r'\bNúm\.\s*\d+\b',  # Números de boletín
        r'\bPág\.\s*\d+\b',  # Números de página
        r'\b(?:Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo)\s+\d+\s+de\s+\w+\s+de\s+\d{4}\b',  # Encabezados de fecha
        r'^\s*\S\s*$',  # Líneas con un solo carácter
        r'https?:\/\/\S+',  # URLs
        r'SECCIÓN PRIMERA\s*\nEmpresarios\s*\nActos inscritos\s*\n',  # Encabezado de sección
        r'D\.L\.:.*?ISSN:.*'  # Información del pie de página
    ]
    
    # Aplicar cada patrón al texto
    for patron in patrones_a_eliminar:
        texto = re.sub(patron, '', texto, flags=re.MULTILINE)
    
    # Eliminar espacios extra y reducir múltiples saltos de línea
    texto = re.sub(r'[ \t]+', ' ', texto).strip()
    texto = re.sub(r'\n{2,}', '\n\n', texto)
    
    return texto


# 🛠️ Función para extraer la provincia desde el texto
def extraer_provincia(texto):
    """
    Extrae la provincia desde el texto del PDF.
    
    Parámetros:
        - texto (str): Texto del PDF.
    
    Retorna:
        - provincia (str): Provincia extraída.
    """
    try:
        # Extraer la primera línea como provincia
        provincia = texto.splitlines()[0].strip()
        # Reemplazar caracteres no válidos en nombres de archivos
        provincia = re.sub(r'\W+', '_', provincia)
        logging.info(f"Provincia extraída: {provincia}")
        return provincia
    except Exception as e:
        logging.error(f"Error extrayendo la provincia: {e}")
        return 'desconocida'


# 🛠️ Función para procesar un archivo PDF
def procesar_pdf(pdf_path, output_dir):
    """
    Procesa un archivo PDF, extrae datos de empresas y los guarda en archivos JSON y JSONL.
    
    Parámetros:
        - pdf_path (str): Ruta al archivo PDF.
        - output_dir (str): Directorio donde se guardarán los archivos JSON y JSONL.
    
    Retorna:
        - None
    """
    texto = extraer_texto(pdf_path)  # Extraer texto del PDF
    if not texto:
        logging.error(f"No se pudo procesar el archivo PDF: {pdf_path}")
        return
    
    # Extraer fecha desde el nombre de la carpeta
    fecha = os.path.basename(os.path.dirname(pdf_path))
    provincia = extraer_provincia(texto)
    
    # 📝 Extraer datos de empresas usando un patrón
    patron = r'(\d{5,6} - .*?)\n(.*?)(?=\n\d{5,6} - |\Z)'
    resultados = re.findall(patron, texto, re.S)
    
    # Filtrar empresas relevantes
    empresas_filtradas = [
        (empresa.strip(), descripcion.strip())
        for empresa, descripcion in resultados
        if any(palabra in descripcion for palabra in ['Constitución', 'Extinción'])
    ]
    
    # Procesar cada empresa
    empresas_procesadas = []
    for empresa, descripcion in empresas_filtradas:
        empresas_procesadas.append(procesar_empresa(empresa, descripcion))
    
    # 📁 Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # 📄 Guardar en JSON y JSONL
    json_path = os.path.join(output_dir, f"empresas_{fecha}_{provincia}.json")
    jsonl_path = os.path.join(output_dir, f"empresas_{fecha}_{provincia}.jsonl")
    
    with open(json_path, 'w', encoding='utf-8') as archivo_json:
        json.dump(empresas_procesadas, archivo_json, ensure_ascii=False, indent=4)
    logging.info(f"Datos guardados en formato JSON: {json_path}")
    
    with open(jsonl_path, 'w', encoding='utf-8') as archivo_jsonl:
        for empresa in empresas_procesadas:
            archivo_jsonl.write(json.dumps(empresa, ensure_ascii=False) + '\n')
    logging.info(f"Datos guardados en formato JSONL: {jsonl_path}")



# 🛠️ Función para procesar una carpeta de PDFs (soporta subcarpetas)
def procesar_carpeta_pdfs(folder_path, output_dir):
    """
    Procesa archivos PDF en una carpeta y sus subcarpetas recursivamente.

    Parámetros:
        - folder_path (str): Ruta a la carpeta que contiene archivos PDF o subcarpetas con PDFs.
        - output_dir (str): Directorio donde se guardarán los archivos JSON y JSONL.
    """
    try:
        # 📂 Recorrer la carpeta y sus subcarpetas
        for root, dirs, files in os.walk(folder_path):
            for archivo in files:
                if archivo.endswith('.pdf'):
                    # 📄 Procesar cada archivo PDF encontrado
                    pdf_path = os.path.join(root, archivo)
                    logging.info(f"Procesando archivo PDF: {pdf_path}")
                    procesar_pdf(pdf_path, output_dir)
        
        logging.info(f"✅ Procesamiento completo para la carpeta y subcarpetas: {folder_path}")
    except Exception as e:
        logging.error(f"❌ Error al procesar la carpeta {folder_path}: {e}")


# 🛠️ Función para procesar una empresa
def procesar_empresa(empresa, descripcion):
    """
    Procesa una empresa y su descripción para extraer los campos clave.
    
    Parámetros:
        - empresa (str): Información de la empresa (ID y Nombre).
        - descripcion (str): Descripción de la empresa con detalles adicionales.
    
    Retorna:
        - dict: Diccionario con los datos extraídos.
    """
    # 🆔 Extraer ID y Nombre
    match = re.match(r'(\d{5,6}) - (.*)', empresa)
    if match:
        id_empresa = match.group(1)
        nombre_empresa = match.group(2)
    else:
        id_empresa = None
        nombre_empresa = None
    
    # 📝 Eliminar saltos de línea en la descripción
    descripcion = descripcion.replace('\n', ' ')
    
    # 🏷️ Identificar Acto Legal
    if 'Constitución' in descripcion:
        acto_legal = 'Constitución'
    elif 'Extinción' in descripcion:
        acto_legal = 'Extinción'
    else:
        acto_legal = 'Desconocido'
    
    datos = {'Acto legal': acto_legal}
    
    # 🔍 Patrón general para claves y valores
    patrones_claves = {
        'Comienzo de operaciones': r'(Comienzo de operaciones):\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)',
        'Objeto social': r'(Objeto social):\s*(.*?)(?=\s*(?:Domicilio|Capital|Socio único|Adm\. Unico|Adm\. Solid\.|Liquidador|Disolución|Juzgado|Juez|Declaración de unipersonalidad|Nombramientos|Datos registrales|$))',
        'Domicilio': r'(Domicilio):\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)',
        'Capital': r'(Capital):\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)',
        'Socio único': r'(Socio único):\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)',
        'Adm. Unico': r'(Adm\. Unico):\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)',
        'Adm. Solid.': r'(Adm\. Solid\.):\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)',
        'Liquidador': r'(Liquidador):\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)',
        'Disolución': r'(Disolución)\.\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)',
        'Juzgado': r'(Juzgado):\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)',
        'Juez': r'(Juez):\s*(.*?)(?=\s+[A-Z][a-z]|$|\Z)'
    }
    
    # 🧠 Procesar patrones dependiendo del acto legal
    if acto_legal == 'Constitución':
        claves_relevantes = ['Comienzo de operaciones', 'Objeto social', 'Domicilio', 'Capital', 'Socio único', 'Adm. Unico', 'Adm. Solid.' ]
    elif acto_legal == 'Extinción':
        claves_relevantes = ['Liquidador', 'Disolución', 'Juzgado', 'Juez', 'Adm. Unico', 'Adm. Solid.']
    else:
        claves_relevantes = patrones_claves.keys()
    
    # 🔄 Extraer la información
    for clave in claves_relevantes:
        patron = patrones_claves[clave]
        coincidencia = re.search(patron, descripcion)
        if coincidencia:
            datos[clave] = coincidencia.group(2).strip()
    
    # 📦 Crear el diccionario final
    empresa_dict = {
        'Nombre': nombre_empresa,
        'Id': id_empresa,
        **datos  # Añadir los datos extraídos
    }
    
    return empresa_dict


# 🛠️ Función principal para la fase Crawler
def crawler_main(filepath):
    """
    Punto de entrada para la fase Crawler.
    Parámetros:
        - filepath (str): Ruta al archivo PDF o carpeta de PDFs.
    """
    output_dir = 'data/outputs/crawler'
    if os.path.isfile(filepath):
        logging.info(f"Fase Crawler: Procesando archivo PDF {filepath}")
        procesar_pdf(filepath, output_dir)
    elif os.path.isdir(filepath):
        logging.info(f"Fase Crawler: Procesando carpeta de PDFs {filepath}")
        procesar_carpeta_pdfs(filepath, output_dir)
    else:
        logging.error("La ruta proporcionada no es válida.")


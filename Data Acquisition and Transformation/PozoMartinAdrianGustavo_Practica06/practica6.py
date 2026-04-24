{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "40724c98-f5ac-47bb-af3d-7ea57df0f5e7",
   "metadata": {},
   "source": [
    "# PRÁCTICA 6"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "d91a26b1-2b93-4668-995e-ef703857ed09",
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests,re\n",
    "from bs4 import BeautifulSoup\n",
    "import json"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "e1249795-5b4e-407e-8668-86f6343e8a9d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Definimos la URL de la página web que contiene los datos que queremos extraer.\n",
    "url = \"https://en.wikipedia.org/wiki/Comillas_Pontifical_University\"\n",
    "\n",
    "# Hacemos una solicitud HTTP para descargar el contenido de la página web.\n",
    "response = requests.get(url)\n",
    "\n",
    "# Utilizamos BeautifulSoup para  \"parsear\" el contenido HTML de la página.\n",
    "# Esto nos permitirá buscar elementos específicos dentro del HTML.\n",
    "soup = BeautifulSoup(response.content, \"html.parser\")\n",
    "\n",
    "# Buscamos todas las tablas en el HTML que tengan la clase \"infobox vcard\".\n",
    "target_tables = soup.find_all(\"table\", class_=\"infobox vcard\")  # \"table\" es la etiqueta HTML y \"infobox vcard\" es la clase de la tabla.\n",
    "\n",
    "#  find_all(\"a\", class_=\"mw-file-description\"):\n",
    "#  Esta instrucción busca dentro de target_tables[0] todos los enlaces (<a>), ya que \"a\" indica etiquetas de tipo enlace.\n",
    "#  Solo selecciona los enlaces que tienen el atributo class=\"mw-file-description\".\n",
    "#  Devuelve una lista con todos esos elementos <a> que coinciden con ese criterio.\n",
    "#  Finalmente, la variable logos almacenará todos los enlaces (<a>) con la clase mw-file-description encontrados dentro de target_tables[0].\n",
    "logos = target_tables[0].find_all(\"a\",class_=\"mw-file-description\")\n",
    "\n",
    "# Extraemos las URLs de los logos de la página web.\n",
    "# Cada elemento de logos es un objeto Tag de BeautifulSoup que representa una etiqueta <a> del HTML.\n",
    "# href: Es el atributo que contiene la dirección (URL) a la que apunta el enlace.\n",
    "url_logos = [logo[\"href\"] for logo in logos]\n",
    "\n",
    "# Convertimos las URLs relativas en URLs absolutas\n",
    "url_logos[0] = \"https://en.wikipedia.org/\"+url_logos[0]\n",
    "url_logos[1] = \"https://en.wikipedia.org/\"+url_logos[1]\n",
    "\n",
    "# Buscamos todas las etiquetas <td> dentro de la tabla que tengan alguna de las siguientes clases:\n",
    "#    \"infobox-data\": Etiquetas <td> con datos normales.\n",
    "#    \"infobox-full-data nickname\": Etiquetas <td> que contienen nombres o apodos, como el lema en latín.\n",
    "raw_cells = target_tables[0].find_all(\"td\", class_=[\"infobox-data\", \"infobox-full-data nickname\"])\n",
    "\n",
    "# El método get_text() de BeautifulSoup extrae el texto contenido dentro de un elemento HTML.\n",
    "raw_texts = [element.get_text() for element in raw_cells]\n",
    "\n",
    "for i in range(len(raw_texts)):\n",
    "    \n",
    "    # Sustituimos cualquier ocurrencia del carácter especial \\xa0 por un espacio normal (' ').\n",
    "    raw_texts[i] = re.sub(r'\\xa0', ' ', raw_texts[i])\n",
    "    \n",
    "    # Eliminamos cualquier texto que esté dentro de corchetes [], incluyendo los corchetes. (lo usamos para quitar referencias a las fuentes)\n",
    "    raw_texts[i] = re.sub(r'\\[.*?\\]', '', raw_texts[i])\n",
    "\n",
    "# Modificamos el primer elemento (raw_texts[0]), que contiene el lema en latín con el prefijo Latin: (es decir, dejamos solo el contenido \n",
    "# útil del lema en latín.\n",
    "raw_texts[0] = raw_texts[0].split(': ')[1]\n",
    "\n",
    "# Construimos la lista de claves que se utilizarán como nombres para las entradas del diccionario university_data.\n",
    "keys = [\"seal\", \"motto_latin\", \"motto_spanish\", \"motto_english\",\"type\",\n",
    "        \"established\",\"religious_affiliation\",\"chancellor\",\"vice_chancellor\",\n",
    "        \"rector\",\"students\", \"location\", \"campus\", \"colors\", \"website\", \"logo\"]\n",
    "\n",
    "# Construimos el diccionario. El cuanto a los values tenemos:\n",
    "#    url_logos[:1]: Seleccionamos el primer elemento de url_logos, que corresponde al enlace de la primera imagen.\n",
    "#    raw_texts: Contiene los datos procesados de las celdas <td> (como lema, tipo, estudiantes, etc.).\n",
    "#    url_logos[1:]: Seleccionamos el segundo elemento de url_logos, que corresponde al enlace del logo inferior.\n",
    "university_data = dict(zip(keys, url_logos[:1] + raw_texts + url_logos[1:]))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "669c5077-786a-48c0-a96a-9d8121986877",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'seal': 'https://en.wikipedia.org//wiki/File:Comillas_Pontifical_University_seal.svg',\n",
       " 'motto_latin': 'Pontificia Universitas Comillensis Matriti',\n",
       " 'motto_spanish': 'El Valor de la Excelencia',\n",
       " 'motto_english': 'The Value of Excellence',\n",
       " 'type': 'Private Catholic Pontifical higher education institution',\n",
       " 'established': 1890,\n",
       " 'religious_affiliation': 'Roman Catholic Church (Jesuit)',\n",
       " 'chancellor': 'Very Rev.Arturo Sosa, SJ',\n",
       " 'vice_chancellor': 'Rev.Joaquín Barrero Díaz, SJ',\n",
       " 'rector': 'Dr. P. Enrique Sanz Giménez-Rico, SJ',\n",
       " 'students': 11149,\n",
       " 'location': 'Madrid, Spain',\n",
       " 'campus': 'Both urban and rural.',\n",
       " 'colors': 'Yellow & Black',\n",
       " 'website': 'www.comillas.edu',\n",
       " 'logo': 'https://en.wikipedia.org//wiki/File:Comillas_Universidad_Pontificia_logo_(2018).jpg'}"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Convertimos el campo \"established\" al formato adecuado.\n",
    "# El valor original incluye un año seguido de texto adicional como \"; 134 years ago\".\n",
    "# Nos quedamos solo con el año (la parte antes del punto y coma).\n",
    "university_data['established'] = university_data['established'].split(';')[0]\n",
    "\n",
    "# Transformamos el año, que todavía es un texto, en un número entero.\n",
    "university_data['established'] = int(university_data['established'])\n",
    "\n",
    "# Ahora procesamos el campo \"students\".\n",
    "# Como el número incluye comas (\"11,149\"), eliminamos las comas del texto para después convertir el dato a número sin problema.\n",
    "university_data['students'] = re.sub(r',', '', university_data['students'])\n",
    "\n",
    "# Convertimos el número de estudiantes, que es un texto, en un número entero.\n",
    "university_data['students'] = int(university_data['students'])\n",
    "\n",
    "# Mostramos el diccionario actualizado con los campos ya convertidos al formato correcto.\n",
    "university_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "afd8abc6-4393-4d50-ad1f-486ae7f2d1eb",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Abrimos o creamos el archivo university_data.json en modo escritura (\"w\") y guardamos el diccionario university_data en formato JSON, \n",
    "# respetando caracteres especiales (tildes, ñ) con ensure_ascii=False y aplicamos una sangría de 4 espacios (indent=4) para hacerlo \n",
    "# legible. Al finalizar, el archivo se cierra automáticamente gracias al uso de with.\n",
    "with open(\"university_data.json\", \"w\", encoding=\"utf-8\") as output_file:\n",
    "    json.dump(university_data, output_file, ensure_ascii=False, indent=4)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a377e9fb-3026-4b6e-8fb3-b80c57371c2f",
   "metadata": {},
   "source": [
    "---\n",
    "## OPCIÓN 2"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "bf202e9d-3ae4-4a1a-a2b5-b8d58f5d3f1b",
   "metadata": {},
   "source": [
    "El código es análogo al anterior con la salvedad de que introducimos la instrucción raw_texts[-1] = \"https://\" + raw_texts[-1] para que al clickar en el string que contiene la web de la universidad nos lleve al enlace correspodiente.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "0a29ce2f-9f05-4d5f-8364-bd72c928875e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Definimos la URL de la página web que contiene los datos que queremos extraer.\n",
    "url = \"https://en.wikipedia.org/wiki/Comillas_Pontifical_University\"\n",
    "\n",
    "# Hacemos una solicitud HTTP para descargar el contenido de la página web.\n",
    "response = requests.get(url)\n",
    "\n",
    "# Utilizamos BeautifulSoup para  \"parsear\" el contenido HTML de la página.\n",
    "# Esto nos permitirá buscar elementos específicos dentro del HTML.\n",
    "soup = BeautifulSoup(response.content, \"html.parser\")\n",
    "\n",
    "# Buscamos todas las tablas en el HTML que tengan la clase \"infobox vcard\".\n",
    "target_tables = soup.find_all(\"table\", class_=\"infobox vcard\")  # \"table\" es la etiqueta HTML y \"infobox vcard\" es la clase de la tabla.\n",
    "\n",
    "#  find_all(\"a\", class_=\"mw-file-description\"):\n",
    "#  Esta instrucción busca dentro de target_tables[0] todos los enlaces (<a>), ya que \"a\" indica etiquetas de tipo enlace.\n",
    "#  Solo selecciona los enlaces que tienen el atributo class=\"mw-file-description\".\n",
    "#  Devuelve una lista con todos esos elementos <a> que coinciden con ese criterio.\n",
    "#  Finalmente, la variable logos almacenará todos los enlaces (<a>) con la clase mw-file-description encontrados dentro de target_tables[0].\n",
    "logos = target_tables[0].find_all(\"a\",class_=\"mw-file-description\")\n",
    "\n",
    "# Extraemos las URLs de los logos de la página web.\n",
    "# Cada elemento de logos es un objeto Tag de BeautifulSoup que representa una etiqueta <a> del HTML.\n",
    "# href: Es el atributo que contiene la dirección (URL) a la que apunta el enlace.\n",
    "url_logos = [logo[\"href\"] for logo in logos]\n",
    "\n",
    "# Convertimos las URLs relativas en URLs absolutas\n",
    "url_logos[0] = \"https://en.wikipedia.org/\"+url_logos[0]\n",
    "url_logos[1] = \"https://en.wikipedia.org/\"+url_logos[1]\n",
    "\n",
    "# Buscamos todas las etiquetas <td> dentro de la tabla que tengan alguna de las siguientes clases:\n",
    "#    \"infobox-data\": Etiquetas <td> con datos normales.\n",
    "#    \"infobox-full-data nickname\": Etiquetas <td> que contienen nombres o apodos, como el lema en latín.\n",
    "raw_cells = target_tables[0].find_all(\"td\", class_=[\"infobox-data\", \"infobox-full-data nickname\"])\n",
    "\n",
    "# El método get_text() de BeautifulSoup extrae el texto contenido dentro de un elemento HTML.\n",
    "raw_texts = [element.get_text() for element in raw_cells]\n",
    "\n",
    "for i in range(len(raw_texts)):\n",
    "    \n",
    "    # Sustituimos cualquier ocurrencia del carácter especial \\xa0 por un espacio normal (' ').\n",
    "    raw_texts[i] = re.sub(r'\\xa0', ' ', raw_texts[i])\n",
    "    \n",
    "    # Eliminamos cualquier texto que esté dentro de corchetes [], incluyendo los corchetes. (lo usamos para quitar referencias a las fuentes)\n",
    "    raw_texts[i] = re.sub(r'\\[.*?\\]', '', raw_texts[i])\n",
    "\n",
    "# Modificamos el primer elemento (raw_texts[0]), que contiene el lema en latín con el prefijo Latin: (es decir, dejamos solo el contenido \n",
    "# útil del lema en latín.\n",
    "raw_texts[0] = raw_texts[0].split(': ')[1]\n",
    "\n",
    "# Construimos la lista de claves que se utilizarán como nombres para las entradas del diccionario university_data.\n",
    "keys = [\"seal\", \"motto_latin\", \"motto_spanish\", \"motto_english\",\"type\",\n",
    "        \"established\",\"religious_affiliation\",\"chancellor\",\"vice_chancellor\",\n",
    "        \"rector\",\"students\", \"location\", \"campus\", \"colors\", \"website\", \"logo\"]\n",
    "\n",
    "#Añadimos la cadena \"https://\" a la web para que nos lleve directamente a ella.\n",
    "raw_texts[-1] = \"https://\" + raw_texts[-1]\n",
    "\n",
    "# Construimos el diccionario. El cuanto a los values tenemos:\n",
    "#    url_logos[:1]: Seleccionamos el primer elemento de url_logos, que corresponde al enlace de la primera imagen.\n",
    "#    raw_texts: Contiene los datos procesados de las celdas <td> (como lema, tipo, estudiantes, etc.).\n",
    "#    url_logos[1:]: Seleccionamos el segundo elemento de url_logos, que corresponde al enlace del logo inferior.\n",
    "university_data = dict(zip(keys, url_logos[:1] + raw_texts + url_logos[1:]))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "60159275-777f-4b26-a70d-b07d3792bb98",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'seal': 'https://en.wikipedia.org//wiki/File:Comillas_Pontifical_University_seal.svg',\n",
       " 'motto_latin': 'Pontificia Universitas Comillensis Matriti',\n",
       " 'motto_spanish': 'El Valor de la Excelencia',\n",
       " 'motto_english': 'The Value of Excellence',\n",
       " 'type': 'Private Catholic Pontifical higher education institution',\n",
       " 'established': 1890,\n",
       " 'religious_affiliation': 'Roman Catholic Church (Jesuit)',\n",
       " 'chancellor': 'Very Rev.Arturo Sosa, SJ',\n",
       " 'vice_chancellor': 'Rev.Joaquín Barrero Díaz, SJ',\n",
       " 'rector': 'Dr. P. Enrique Sanz Giménez-Rico, SJ',\n",
       " 'students': 11149,\n",
       " 'location': 'Madrid, Spain',\n",
       " 'campus': 'Both urban and rural.',\n",
       " 'colors': 'Yellow & Black',\n",
       " 'website': 'https://www.comillas.edu',\n",
       " 'logo': 'https://en.wikipedia.org//wiki/File:Comillas_Universidad_Pontificia_logo_(2018).jpg'}"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Convertimos el campo \"established\" al formato adecuado.\n",
    "# El valor original incluye un año seguido de texto adicional como \"; 134 years ago\".\n",
    "# Nos quedamos solo con el año (la parte antes del punto y coma).\n",
    "university_data['established'] = university_data['established'].split(';')[0]\n",
    "\n",
    "# Transformamos el año, que todavía es un texto, en un número entero.\n",
    "university_data['established'] = int(university_data['established'])\n",
    "\n",
    "# Ahora procesamos el campo \"students\".\n",
    "# Como el número incluye comas (\"11,149\"), eliminamos las comas del texto para después convertir el dato a número sin problema.\n",
    "university_data['students'] = re.sub(r',', '', university_data['students'])\n",
    "\n",
    "# Convertimos el número de estudiantes, que es un texto, en un número entero.\n",
    "university_data['students'] = int(university_data['students'])\n",
    "\n",
    "# Mostramos el diccionario actualizado con los campos ya convertidos al formato correcto.\n",
    "university_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "126608e6-3ce9-4052-a4a6-3084d95ee6a8",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Abrimos o creamos el archivo university_data.json en modo escritura (\"w\") y guardamos el diccionario university_data en formato JSON, \n",
    "# respetando caracteres especiales (tildes, ñ) con ensure_ascii=False y aplicamos una sangría de 4 espacios (indent=4) para hacerlo \n",
    "# legible. Al finalizar, el archivo se cierra automáticamente gracias al uso de with.\n",
    "with open(\"university_data_2.json\", \"w\", encoding=\"utf-8\") as output_file:\n",
    "    json.dump(university_data, output_file, ensure_ascii=False, indent=4)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

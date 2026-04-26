# Indexacion de datos en SolR

### Objetivo de la práctica

Vamos a indexar una colección de datos en SolR. Indexar una colección implica insertar datos.
Para ello usaremos el fichero `books.csv` en la carpeta de `resources` y usaremos un `IndexHandler`que provee SolR.


### Generacón de una instancia (config de SolR)

Lo primero que tenemos que hacer es generar una configuración por defecto de SolR.

Para ello, en el Edge ejecutamos lo siguiente:

> solrctl instancedir --generate $HOME/solr_configs

Sustituimos el fichero por defecto `schema.xml` por el que tenemos en `resources`

Subimos la configuración a SolR con el siguiente comando:

>solrctl instancedir --create books_mbdXX $HOME/solr_configs

Ya podemos ver el core en la UI de SolR.

### Creación de una colección vacía

Asociado al core anterior, vamos a crear una colección vacía.

https://solr.apache.org/guide/6_6/collections-api.html

> GET http://worker02.bigdata.alumnos.upcont.es:8983/solr/admin/collections?action=DELETE...

> GET http://worker02.bigdata.alumnos.upcont.es:8983/solr/admin/collections?action=CREATE...

### Indexacion

Vamos a indexar nuestros datos, usando la documentación:

https://solr.apache.org/guide/7_1/uploading-data-with-index-handlers.html

>POST http://worker02.bigdata.alumnos.upcont.es:8983/solr/books_mbdXX/update?commit=true&header=true&skip=series_t,sequence_i
>Content-Type: application/csv

>< <path_name>/books.csv`

### Cambiar el schema.xml

Cambiar el schema para que el autor sea más sencillo de buscar.
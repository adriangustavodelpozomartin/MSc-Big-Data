Información sobre los archivos que se encuentran en la carpeta:


1. "practica_9_spider.ipynb" contiene el código de la fase Spider.
2. "practica_9_crawler.ipynb" contienen el código de la fase Crawler.

Archivos generados

Este proyecto incluye tres archivos de salida principales:

1. "datos_ofertas.csv", output de la fase Spider. 

2. output_def.csv

En este archivo, encontrará los resultados obtenidos tras la ejecución inicial del código. Sin embargo, para algunas empresas, como las 7 y 8 (contando desde 0), faltan ciertos datos. Este problema se debe a la duración insuficiente de los tiempos de espera configurados mediante time.sleep en el código.

3. output_def_time_sleeps.csv

Este archivo contiene los resultados de una prueba adicional realizada para las empresas 7 y 8. En esta prueba, se incrementaron los tiempos de espera en el código, lo que permitió obtener todos los datos disponibles para dichas empresas. Este archivo demuestra que los datos que faltaban en output_def.csv no se debían a un problema en la lógica del código, sino a tiempos de espera insuficientes durante la ejecución.

Sin embargo, no se ejecutó el código con estos tiempos de espera más largos para todas las empresas, ya que habría requerido un tiempo de ejecución excesivo (más de una hora).


#!/bin/bash

# Definir las variables necesarias
APP_NAME="Procesamiento GAIA"
INPUT_FILE="hdfs:///user/mbd31/file_list.txt"
BATCH_SIZE=1000

# Crear el archivo scala que contiene el código
cat <<EOL > procesamiento-gaia.scala
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

val spark = SparkSession.builder()
  .appName("$APP_NAME")
  .getOrCreate()

// Leer el archivo de la lista de archivos en HDFS
val fileList = spark.sparkContext.textFile("$INPUT_FILE").collect()

// Definir el tamaño del lote
val batchSize = $BATCH_SIZE

// Filtrar los archivos no vacíos
val filteredFileList = fileList.filter(_.nonEmpty)

// Calcular el número de lotes
val numBatches = math.ceil(filteredFileList.length.toDouble / batchSize).toInt

// Inicializamos un contador total
var totalStars = 0L

// Procesar los archivos en lotes
for (i <- 0 until numBatches) {
  // Determinar los límites del lote
  val start = i * batchSize
  val end = math.min(start + batchSize, filteredFileList.length)
  
  // Obtener el lote actual
  val batchFiles = filteredFileList.slice(start, end)
  
  // Leer los archivos del lote en un DataFrame
  val dfBatch = spark.read.option("header", "true").csv(batchFiles: _*)
  
  // Contar el número de estrellas en el lote actual
  val starCount = dfBatch.count()
  
  // Acumular el número de estrellas
  totalStars += starCount
  
  // Mostrar el resultado parcial
  println(s"Lote \$i: Número de estrellas = \$starCount")
}

// Mostrar el total de estrellas
println(s"Número total de estrellas en todos los lotes = \$totalStars")

spark.stop()
EOL

# Ejecutar el script de Spark utilizando spark-submit
/opt/cloudera/parcels/SPARK2/bin/spark-submit procesamiento-gaia.scala
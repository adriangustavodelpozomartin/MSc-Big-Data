import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions._


val fileList = spark.sparkContext.textFile("hdfs:///user/mbd31/file_list.txt").collect()

// Definir el tamaño del lote
val batchSize = 1000
val filteredFileList = fileList.filter(_.nonEmpty)
val numBatches = math.ceil(filteredFileList.length.toDouble / batchSize).toInt

// Ejercicio 1
var totalStars = 0L
for (i <- 0 until numBatches) {
  val start = i * batchSize
  val end = math.min(start + batchSize, filteredFileList.length)
  val batchFiles = filteredFileList.slice(start, end)
  val dfBatch = spark.read.option("header", "true").csv(batchFiles: _*)
  val starCount = dfBatch.count()
  totalStars += starCount
  println(s"Lote $i: Número de estrellas = $starCount")
}
println(s"Número total de estrellas en todos los lotes = $totalStars")

// Ejercicio 2
var validStarCount = 0L
for (i <- 0 until numBatches) {
  val start = i * batchSize
  val end = math.min(start + batchSize, filteredFileList.length)
  val batchFiles = filteredFileList.slice(start, end)
  val dfBatch = spark.read.option("header", "true").csv(batchFiles: _*)
  val conditionDf = dfBatch.withColumn("condition", $"astrometric_n_good_obs_al" + $"astrometric_n_bad_obs_al" === $"astrometric_n_obs_al")
  val validCount = conditionDf.filter($"condition" === true).count()
  validStarCount += validCount
  println(s"Lote $i: Número de estrellas que cumplen la condición = $validCount")
}
println(s"Número total de estrellas que cumplen la condición: $validStarCount")



// Variable para almacenar los resultados
var groupByGoodObsTotal: DataFrame = spark.emptyDataFrame

// Esta función une dos DataFrames sumando los valores de la columna "count".
def combineDataFrames(df1: DataFrame, df2: DataFrame): DataFrame = {
  // Nos aseguramos de que ambas columnas de conteo tengan nombres consistentes
  val df1Renamed = df1.withColumnRenamed("count", "count_1")
  val df2Renamed = df2.withColumnRenamed("count", "count_2")

  // Combinamos los DataFrames sumando los conteos
  val combined = df1Renamed.join(df2Renamed, Seq("astrometric_n_good_obs_al"), "outer")
    .withColumn("count_total", coalesce($"count_1", lit(0)) + coalesce($"count_2", lit(0)))
    .drop("count_1").drop("count_2") // Eliminamos las columnas temporales

  // Nos aseguramos de que el DataFrame resultante tenga la columna "count" con el nombre adecuado
  combined.withColumnRenamed("count_total", "count")
}

// Procesar los archivos en lotes
for (i <- 0 until numBatches) {
  val start = i * batchSize
  val end = math.min(start + batchSize, filteredFileList.length)
  val batchFiles = filteredFileList.slice(start, end)

  // Leemos el lote actual
  val dfBatch = spark.read.option("header", "true").csv(batchFiles: _*)

  // Agrupamos el lote actual por "astrometric_n_good_obs_al" y contamos las ocurrencias
  val groupByGoodObs = dfBatch.groupBy("astrometric_n_good_obs_al").count()

  // Agregamos el resultado del lote actual al total
  if (groupByGoodObsTotal.isEmpty) {
    groupByGoodObsTotal = groupByGoodObs
  } else {
    // Realizamos la agregación acumulada entre los lotes
    groupByGoodObsTotal = combineDataFrames(groupByGoodObsTotal, groupByGoodObs)
  }
}

// Mostrar el agrupado total
groupByGoodObsTotal.show(1000, truncate=false)

// Ejercicio 4
var groupByRatioTotal: DataFrame = spark.emptyDataFrame

for (i <- 0 until numBatches) {
  val start = i * batchSize
  val end = math.min(start + batchSize, filteredFileList.length)
  val batchFiles = filteredFileList.slice(start, end)
  val dfBatch = spark.read.option("header", "true").csv(batchFiles: _*)
  val ratioDf = dfBatch.withColumn("ratio", (($"astrometric_n_good_obs_al" / $"astrometric_n_obs_al") * 100).cast("int"))
  val groupByRatio = ratioDf.groupBy("ratio").count()
  if (groupByRatioTotal.isEmpty) {
    groupByRatioTotal = groupByRatio
  } else {
    groupByRatioTotal = combineDataFrames(groupByRatioTotal, groupByRatio)
  }
}
groupByRatioTotal.show(100, truncate=false)


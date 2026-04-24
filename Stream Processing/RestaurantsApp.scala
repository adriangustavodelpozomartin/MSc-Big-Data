package edu.comillas.restaurants

import edu.comillas.restaurants.model.Restaurant
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.catalyst.ScalaReflection
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object RestaurantsApp extends App {

  // 1) Crear SparkSession
  implicit val spark: SparkSession = SparkSession.builder()
    .appName("RestaurantsApp")
    .master("local[*]")
    .getOrCreate()
  import spark.implicits._

  // 2) Inferir el esquema a partir de la case class
  val restaurantSchema: StructType =
    ScalaReflection.schemaFor[Restaurant].dataType.asInstanceOf[StructType]

  // 3) Leer del topic "restaurants" y deserializar a Dataset[Restaurant]
  val fromKafka = spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "master01.bigdata.alumnos.upcont.es:9092")
    .option("subscribe", "restaurants")
    .option("startingOffsets", "earliest")
    .option("maxOffsetsPerTrigger", 20)
    .load()
    .selectExpr("CAST(value AS STRING) AS json")
    .select(from_json($"json", restaurantSchema).as("data"))
    .select("data.*")
    .as[Restaurant]

  // 4) Agregado por type_of_food (solo rating > 4)
  val aggTypeOfFood = fromKafka
    .filter(r => r.rating.getOrElse(0.0) > 4.0)
    .groupBy($"type_of_food")
    .agg(
      round(avg($"rating"), 2).alias("avg_rating"),
      collect_set($"name").alias("restaurants")
    )

  // 5) Envío del resultado al topic "restaurants_mbdXXX" en formato JSON
  val toKafka = aggTypeOfFood
    .select(to_json(struct($"type_of_food", $"avg_rating", $"restaurants")).alias("value"))
    .writeStream
    .outputMode("update")
    .format("kafka")
    .option("kafka.bootstrap.servers", "master01.bigdata.alumnos.upcont.es:9092")
    .option("topic", "restaurants_mbd15_2025")
    .option("checkpointLocation", "/tmp/comillas/restaurants/kafka")
    .start()

  // Mantener la aplicación en ejecución
  toKafka.awaitTermination()
}

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp, from_unixtime, date_format, expr,  udf
from pyspark.sql.types import ArrayType,StructField, StructType, StringType, DoubleType,StructField
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("KafkaToCassandraStreaming") \ #Interactuar con Cassandra.
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,"
            "com.datastax.spark:spark-cassandra-connector_2.12:3.4.0") \
    .config("spark.cassandra.connection.host", "192.168.80.33") \ # Host de cassandra 
    .config("spark.cassandra.connection.port", "9042") \ #puerto de Cassandra
    .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \
    .config("spark.executor.memory", "8g") \
    .config("spark.executor.cores", "4") \
    .config("spark.executor.memoryOverhead", "1024") \
    .config("spark.driver.memory", "4g") \
    .config("spark.dynamicAllocation.enabled", "true") \
    .config("spark.dynamicAllocation.maxExecutors", "6") \
    .getOrCreate()

#Esquema para los datos de kafka.
schema = ArrayType(StructType([
    StructField("time", DoubleType(), True),
    StructField("host", StringType(), True),
    StructField("plugin", StringType(), True)
]))

# Esquemas para los archivos maestros
nodos_schema = StructType() \
    .add("serverName", StringType()) \
    .add("serverGroup", StringType())

turnos_schema = StructType() \
    .add("hora", StringType()) \
    .add("texto_dia_semana", StringType()) \
    .add("Turno", StringType())

nodos_df = spark.read.json("/user/mbd1/collectd/masterFiles/maestro-nodos.json", schema=nodos_schema)
turnos_df = spark.read.json("/user/mbd1/collectd/masterFiles/maestro-turnos.json", schema=turnos_schema)

# Leer datos en tiempo real desde Kafka
kafka_bootstrap_servers = "192.168.80.34:9092,192.168.80.35:9092,192.168.80.37:9092"

# Se configura la lectura de un stream desde el tópico collectd_json_2025, con la opción de empezar a leer desde el último offset (startingOffsets="latest").
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", "collectd_json_2025") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

json_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data"))

json_df = json_df.withColumn("data", F.explode(col("data"))) \
    .select(
        col("data.time").alias("time"),
        col("data.host").alias("host"),
        col("data.plugin").alias("plugin")
    )

json_df = json_df.withColumn("event_time", from_unixtime(col("time").cast("long")).cast("timestamp")) \
    .withColumn("hour", date_format(col("event_time"), "HH")) \
    .withColumn("day_english", date_format(col("event_time"), "EEEE")) \
    .withColumn("event_date", date_format(col("event_time"), "yyyy-MM-dd"))

day_mapping = {
    "Monday": "lunes", "Tuesday": "martes", "Wednesday": "miercoles",
    "Thursday": "jueves", "Friday": "viernes", "Saturday": "sabado", "Sunday": "domingo"
}

english_to_spanish_udf = udf(lambda day: day_mapping.get(day, None), StringType())
json_df = json_df.withColumn("day_spanish", english_to_spanish_udf(col("day_english")))

enriched_df = json_df.alias("r").join(nodos_df.alias("n"), col("r.host") == col("n.serverName"), "left") \
    .join(turnos_df.alias("t"), (col("r.hour") == col("t.hora")) & (col("r.day_spanish") == col("t.texto_dia_semana")), "left")

final_df = enriched_df.select(
    expr("uuid()").alias("id"),
    col("r.plugin").alias("plugin"),
    col("r.hour").alias("hour"),
    col("r.event_date").alias("event_date"),
    col("n.serverGroup").alias("servergroup"),
    col("t.Turno").alias("turno"),
    current_timestamp().alias("ingestion_time")
)

query = final_df.writeStream \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "collectd_keyspace") \
    .option("table", "collectd_streaming") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .outputMode("append") \
    .start()

query.awaitTermination()
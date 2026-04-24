import argparse
import subprocess
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_unixtime, col, date_format, udf, count, avg
from pyspark.sql.types import StringType
from pyspark.sql.window import Window

def main():
    # Definimos 4 argumentos obligatorios.
    parser = argparse.ArgumentParser(
        description="Job de Enriquecimiento de Collectd: Lee datos raw y maestros desde HDFS y almacena el resultado enriquecido en ORC particionado."
    )
    parser.add_argument(
        "raw_data_path",
        help="Ruta HDFS del archivo raw (ej. hdfs:///user/mbd1/collectd/raw/kafka_data.json)"
    )
    parser.add_argument(
        "maestro_nodos_path",
        help="Ruta HDFS del archivo maestro de nodos (ej. hdfs:///user/mbd1/collectd/masterFiles/maestro-nodos.json)"
    )
    parser.add_argument(
        "maestro_turnos_path",
        help="Ruta HDFS del archivo maestro de turnos (ej. hdfs:///user/mbd1/collectd/masterFiles/maestro-turnos.json)"
    )
    parser.add_argument(
        "output_path",
        help="Ruta HDFS de salida para los datos enriquecidos (ej. hdfs:///user/mbd1/collectd/enriched)"
    )

    args = parser.parse_args()
    #SparkConf es una clase que se utiliza para configurar la aplicación de Spark.
    conf = (
        SparkConf()
        .setAppName("HDFSEnrichmentBatch")
        .set("spark.executor.memory", "4g")
        .set("spark.executor.cores", "6")
        .set("spark.dynamicAllocation.maxExecutors", "6")
    )
    spark = SparkSession.builder.config(conf=conf).enableHiveSupport().getOrCreate()

    raw_data_path = args.raw_data_path
    maestro_nodos_path = args.maestro_nodos_path
    maestro_turnos_path = args.maestro_turnos_path
    output_path = args.output_path

    # Lectura de los datos raw y de los archivos maestros desde HDFS
    raw_df = spark.read.json(raw_data_path)
    nodos_df = spark.read.json(maestro_nodos_path)
    turnos_df = spark.read.json(maestro_turnos_path)

    # Conversion del campo 'time' a timestamp y extraccion de la fecha para particionar. Datos particionados por fecha.
    raw_df = raw_df.withColumn("event_time", from_unixtime(col("time").cast("long")).cast("timestamp"))
    raw_df = raw_df.withColumn("hour", date_format(col("event_time"), "HH"))
    raw_df = raw_df.withColumn("day_english", date_format(col("event_time"), "EEEE"))
    # Nueva columna para particionar (por ejemplo, "2025-02-10")
    raw_df = raw_df.withColumn("event_date", date_format(col("event_time"), "yyyy-MM-dd"))

    day_mapping = {
        "Monday": "lunes",
        "Tuesday": "martes",
        "Wednesday": "miercoles",
        "Thursday": "jueves",
        "Friday": "viernes",
        "Saturday": "sabado",
        "Sunday": "domingo"
    }
    def english_to_spanish(day):
        return day_mapping.get(day, None)

    english_to_spanish_udf = udf(english_to_spanish, StringType())
    raw_df = raw_df.withColumn("day_spanish", english_to_spanish_udf(col("day_english")))

    # Enriquecimiento 1: Unir con maestro-nodos para asignar el grupo del servidor
    enriched_df = raw_df.alias("r").join(
        nodos_df.alias("n"),
        col("r.host") == col("n.serverName"),
        "left"
    )

    # Enriquecimiento 2: Unir con maestro-turnos para asignar el turno
    enriched_df = enriched_df.join(
        turnos_df.alias("t"),
        (col("r.hour") == col("t.hora")) & (col("r.day_spanish") == col("t.texto_dia_semana")),
        "left"
    )

    final_df = enriched_df.select(
        col("r.plugin").alias("plugin"), #componente de collectd que recopila métricas.
        col("r.hour").alias("hour"),
        col("r.event_date").alias("event_date"),
        col("n.serverGroup").alias("serverGroup"),
        col("t.Turno").alias("turno")
    )

    # Enriquecimiento 3: agregado de numero de registros y media
    df_agg = final_df.groupBy("plugin", "serverGroup", "hour", "turno", "event_date") \
    .agg(count("*").alias("num_registros"))
    
    window_spec = Window.partitionBy("plugin", "serverGroup", "hour")

    final_enrich_df = df_agg.withColumn("media_registros", avg(col("num_registros")).over(window_spec))
    
    # Guardamos el DataFrame en HDFS en formato ORC sin compresion, particionando por event_date
    final_enrich_df.write.mode("overwrite") \
        .option("orc.compress", "NONE") \
        .partitionBy("event_date") \
        .orc(output_path)

    # Ejecutar MSCK REPAIR TABLE para actualizar las particiones de Hive
    spark.sql(f"MSCK REPAIR TABLE mbd01.collectd_enriched")
    print(f"Particiones actualizadas en mbd01.collectd_enriched")
    
    #Se elimina el archivo raw procesado, evitando reporcesarlo en futuras ejecucuines.
    subprocess.run(["hdfs", "dfs", "-rm", "-f", raw_data_path], check=True)
    print(f"Archivo eliminado de HDFS: {raw_data_path}")
    
if __name__ == "__main__":
    main()
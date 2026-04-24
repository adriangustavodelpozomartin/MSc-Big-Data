from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.ssh.operators.ssh import SSHOperator

default_args = {
    'owner': 'mbd1',
    'start_date': datetime(2025, 1, 1),
    'retries': 1, #Número de reintentos
    'retry_delay': timedelta(minutes=5), #Tiempo de espera entre reintentos
}

def read_kafka_and_write_hdfs(**context):
    from kafka import KafkaConsumer
    from hdfs import InsecureClient
    import json

    # Parámetros de Kafka
    kafka_bootstrap_servers = ["192.168.80.34:9092","192.168.80.35:9092","192.168.80.37:9092"]
    kafka_topic = "collectd_json_2025" #Tópico de Kafka del que vamos a leer mensajes

    # Crear consumidor de Kafka
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        auto_offset_reset="earliest", #Leer desde el inicio
        enable_auto_commit=False
    )

    # Asignar particiones y obtener los offsets finales
    # Se hace una asignación de particiones y se obtienen los offsets finales para saber cuándo se ha terminado de leer la cola.
    consumer.poll(timeout_ms=1000)
    partitions = consumer.assignment()
    if not partitions:
        print(f"No se han asignado particiones para el tópico {kafka_topic}.")
        consumer.close()
        return

    consumer.seek_to_beginning(*partitions)
    end_offsets = consumer.end_offsets(partitions)
    print("End Offsets:", end_offsets)

    # Configuración de HDFS

    hdfs_client = InsecureClient("http://master01.bigdata.alumnos.upcont.es:50070", user='mbd1') #url del namenode
    hdfs_path = '/user/mbd1/collectd/raw/kafka_data.json'

    # Crear archivo si no existe
    if not hdfs_client.status(hdfs_path, strict=False):
        hdfs_client.write(hdfs_path, data="", overwrite=False, append=False)

    # Buffer para escritura en lotes
    buffer_size = 50000 # Tamaño del buffer, para agrupar la escritura.
    message_buffer = []
    total_consumed = 0

    # Consumir solo hasta los offsets finales registrados.

    while True:
        records = consumer.poll(timeout_ms=2000, max_records=buffer_size)
        if not records:
            finished = all(consumer.position(part) >= end_offsets[part] for part in partitions)
            if finished:
                print(f"Se han alcanzado los offsets finales. Mensajes consumidos: {total_consumed}")
                break
        else:
            for tp, msgs in records.items():
                for msg in msgs:
                    try:
                        msg_str = msg.value.decode('utf-8')
                        parsed = json.loads(msg_str)

                        if isinstance(parsed, list):
                            for subobj in parsed:
                                message_buffer.append(json.dumps(subobj))
                        else:
                            message_buffer.append(json.dumps(parsed))

                        total_consumed += 1

                    except Exception as e:
                        print(f"Error procesando mensaje: {e}")

            # Si el buffer alcanza el tamaño deseado, escribir en HDFS
            if len(message_buffer) >= buffer_size:
                hdfs_client.write(hdfs_path, data="\n".join(message_buffer) + "\n", append=True)
                message_buffer = []  # Limpiar buffer

    # Escritura final del buffer restante
    if message_buffer:
        hdfs_client.write(hdfs_path, data="\n".join(message_buffer) + "\n", append=True)

    consumer.close()
    print(f"Proceso completado. Se almacenaron {total_consumed} mensajes en {hdfs_path}.")

# La tarea de Spark se ejecuta después de que se haya completado la tarea de lectura y escritura de Kafka a HDFS.
with DAG(
    dag_id='collectd_batch_pipeline', #DAG titulado collectd_batch_pipeline
    default_args=default_args,
    schedule_interval=None, # Se ejecuta on demand
    catchup=False, #No procesar retroactivamente
    description="DAG que ejecuta el procesamiento batch completo: desde Kafka a HDFS y luego el enriquecimiento vía spark-submit"
) as dag:

    # Tarea para leer Kafka y escribir en HDFS
    kafka_to_hdfs = PythonOperator(
        task_id='read_kafka_and_write_hdfs',
        python_callable=read_kafka_and_write_hdfs,
        provide_context=True
    )


    # Comando spark-submit para ejecutar el enriquecimiento en el nodo edge via SSH.
    # Se ejecuta un script de Spark (collectd_enrichment.py) que realiza el enriquecimiento de los datos.
    # Los archivos maestros son ficheros que contienen datos de referencia. 
    spark_cmd = """
    source /home/alumnos/mbd1/hibridas/setup_spark_env.sh && \
    nohup spark-submit \
            --master yarn \
            --conf spark.eventLog.enabled=true \
            --conf spark.eventLog.dir=hdfs:///user/mbd1/applicationHistory \
            /home/alumnos/mbd1/hibridas/airflow/dags/scripts/collectd_enrichment.py \
            /user/mbd1/collectd/raw/kafka_data.json \
            /user/mbd1/collectd/masterFiles/maestro-nodos.json \ #Contiene informacion sobre los nodos. Asocia cada servidor a un grupo específico. 
            /user/mbd1/collectd/masterFiles/maestro-turnos.json \ #Contiene información para asignar turnos o períodos basados en la hora.
            /user/mbd1/collectd/enriched \
            > /home/alumnos/mbd1/hibridas/enrichment_logs/spark_enrichment.log 2>&1 &
    """
    

    # Tarea de Spark para el enriquecimiento de datos
    spark_enrichment = SSHOperator(
        task_id='spark_submit_enrichment',
        ssh_conn_id='ssh_edge_node',
        command=spark_cmd,
        do_xcom_push=False
    )

    kafka_to_hdfs >> spark_enrichment

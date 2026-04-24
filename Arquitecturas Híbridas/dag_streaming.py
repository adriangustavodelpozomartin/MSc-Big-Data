from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "mbd1",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 23),
    "retries": 2, # 2 reintentos
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="collectd_streaming_pipeline",
    default_args=default_args,
    schedule_interval=None, # Se ejecuta on-demand
    catchup=False,
    description="DAG para ejecutar el procesamiento en streaming con Spark desde Kafka a Cassandra",
)


spark_streaming_cmd = """
source /home/alumnos/mbd1/hibridas/setup_spark_env.sh && \
nohup spark-submit \ #Permite que el proceso continue ejecutandose en sgundo plano
    --master yarn \
    --deploy-mode cluster \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.0 \ #Conector de cassandra.
    --conf spark.executor.memory=8g \
    --conf spark.executor.cores=4 \
    --conf spark.executor.memoryOverhead=1024 \
    --conf spark.driver.memory=4g \
    --conf spark.dynamicAllocation.enabled=true \
    --conf spark.dynamicAllocation.maxExecutors=6 \
    /home/alumnos/mbd1/hibridas/airflow/dags/scripts/collectd_streaming.py \
    > /home/alumnos/mbd1/hibridas/streaming_logs/spark_streaming.log 2>&1 &
"""
# El DAG utiliza este operador para conectarse (a través de SSH) a un nodo edge y ejecutar el comando anterior,
spark_streaming_task = SSHOperator(
    task_id="start_spark_streaming",
    ssh_conn_id="ssh_edge_node",
    command=spark_streaming_cmd,
    do_xcom_push=False,
    dag=dag,
)

spark_streaming_task


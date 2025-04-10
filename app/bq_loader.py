from google.cloud import bigquery
from dotenv import load_dotenv
import pandas as pd
import os
import logging

load_dotenv()

def upload_to_bigquery(df: pd.DataFrame):
    """
    Carga el DataFrame limpio a una tabla de BigQuery.
    Si la tabla no existe, se crea automáticamente.
    """
    try:
        project_id = os.getenv("PROJECT_ID")
        dataset_id = os.getenv("DATASET_ID")
        table_id = os.getenv("TABLE_ID")

        client = bigquery.Client()

        table_ref = f"{project_id}.{dataset_id}.{table_id}"

        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",  # o WRITE_TRUNCATE para sobrescribir
            autodetect=True
        )

        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Esperar a que finalice

        logging.info(f"Datos cargados a BigQuery: {table_ref}")
        print(f"Datos cargados a BigQuery: {table_ref}")

    except Exception as e:
        logging.error(f"Error al subir a BigQuery: {e}")
        print(f"Error al subir a BigQuery: {e}")

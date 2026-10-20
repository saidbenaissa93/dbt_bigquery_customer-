import json
import math
from google.cloud import bigquery
from kafka import KafkaConsumer

# Nettoyage des NaN pour compatibilité JSON / BigQuery
def sanitize_record(record):
    if isinstance(record, dict):
        return {k: sanitize_record(v) for k, v in record.items()}
    elif isinstance(record, list):
        return [sanitize_record(v) for v in record]
    elif isinstance(record, float) and math.isnan(record):
        return None
    return record

# 1. Initialisation du client BigQuery
client = bigquery.Client.from_service_account_json("gcp_key.json")
table_id = "project-gcp-510710.dbt_proj.retail_sales_bronze"

# 2. Configuration du Consumer Kafka
consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='bigquery-ingestion-group-v3',
    consumer_timeout_ms=5000,  # S'arrête automatiquement si aucun message ne vient après 5s
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer démarré ! Collecte des messages depuis Kafka...")

batch = []
for message in consumer:
    record = sanitize_record(message.value)
    batch.append(record)

print(f"Fin de la lecture. {len(batch)} messages récupérés de Kafka.")

if batch:
    print(f"Chargement de {len(batch)} lignes dans BigQuery via un Load Job (Free Tier)...")
    
    # Configuration du job de chargement par lot
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )
    
    # Lancement de l'insertion par lot
    job = client.load_table_from_json(batch, table_id, job_config=job_config)
    job.result()  # Attend la fin du traitement par GCP
    
    print(f"Succès ! {len(batch)} lignes ont été insérées dans {table_id}.")
else:
    print("Aucun nouveau message trouvé.")
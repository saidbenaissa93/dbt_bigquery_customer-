import time
import json
import pandas as pd
from kafka import KafkaProducer

# 1. Initialisation du Producer Kafka avec sérialisation JSON
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Chargement du fichier data.csv...")
# 2. Lecture du fichier CSV
df = pd.read_csv('data.csv', encoding='utf-8')

# Important : Remplacement des NaN / NaT par None pour générer des NULL valide en JSON
df = df.where(pd.notnull(df), None)

records = df.to_dict(orient='records')
total_records = len(records)
print(f"Lancement de l'envoi de {total_records} événements dans Kafka...")

start_time = time.time()

# 3. Envoi rapide des messages
for i, record in enumerate(records, 1):
    producer.send('test-topic', value=record)
    
    # Affichage du progrès tous les 2000 messages
    if i % 2000 == 0 or i == total_records:
        print(f"Progression : {i}/{total_records} messages envoyés...")

# Vider le buffer pour s'assurer que tous les messages sont transmis
producer.flush()

duration = round(time.time() - start_time, 2)
print(f"Terminé ! {total_records} messages envoyés avec succès en {duration} secondes.")
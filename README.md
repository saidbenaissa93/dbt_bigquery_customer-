# 🚀 Data Pipeline de Ventes (Kafka ➔ BigQuery ➔ dbt)

## 📌 But du Projet
Ce projet a pour objectif de construire un pipeline de données moderne (*Modern Data Stack*) complet. Il simule un environnement de production où des transactions de ventes sont ingérées en temps réel, stockées dans un Data Warehouse cloud, puis nettoyées, structurées et audités pour la Business Intelligence (Power BI).

**Objectifs clés :**
- **Ingestion & Streaming :** Capturer des messages JSON depuis un topic Kafka et les charger de manière fiable dans Google BigQuery.
- **Data Warehousing :** Structurer les données selon l'architecture Medallion (Bronze/Raw ➔ Silver/Staging ➔ Gold/Marts).
- **Transformation & Qualité :** Utiliser **dbt** pour transformer les données en SQL, valider leur qualité avec des tests automatisés, et documenter le lineage (DAG).
- **Fiabilité :** Garantir la non-perte de données grâce à la gestion synchrone des batchs (`job.result()`) et du commit manuel dans Kafka.

---

## 🏗️ Architecture du Pipeline

```text
┌────────────────┐     ┌───────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│  Source Ventes │ ──► │   Apache Kafka    │ ──► │   Google BigQuery   │ ──► │       dbt        │
│  (Transactions)│     │  (Stream/Topics)  │     │   (Layer Bronze)    │     │ (Staging & Marts)│
└────────────────┘     └───────────────────┘     └─────────────────────┘     └─────────┬────────┘
                                                                                       │
                                                                                       ▼
                                                                             ┌──────────────────┐
                                                                             │     Power BI     │
                                                                             │  (Dashboards)    │
                                                                             └──────────────────┘
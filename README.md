# 🚀 Data Pipeline de Ventes (Kafka ➔ BigQuery ➔ dbt ➔ Power BI)

## 📌 Présentation du Projet
Ce projet met en place un pipeline de données complet. Les transactions de ventes sont ingérées en temps réel via Apache Kafka, stockées dans Google BigQuery, puis nettoyées et structurées avec dbt avant d'être visualisées dans Power BI.

---

## 🛠️ Étapes de Réalisation
1. **Ingestion (Kafka & Python)** : Simulation et consommation des flux de transactions vers BigQuery (table Bronze).
2. **Transformations (dbt)** : Nettoyage (`stg_retail_sales`) et agrégation des métriques d'affaires (`fct_sales_summary`).
3. **Qualité & Documentation** : Tests automatisés d'unicité et de non-nullité, génération de la documentation et du DAG dbt.
4. **Visualisation (Power BI)** : Connexion à la table de faits BigQuery pour restituer les indicateurs clés.

---

## 📊 Dashboard Power BI

![Power BI Dashboard](images/dashboard.png)

* **Chiffre d'Affaires Total** : 8,23 M$
* **Profit Total** : 1,64 M$ (Marge de 20 %)
* **Panier Moyen** : 457,40 $
* **Analyse** : Dominance de la catégorie *Electronics* et forte rentabilité sur le segment *Consumer* (44,85 % du profit).

---

## 📂 Structure du Dépôt
* `consumer.py` & `producer.py` : Scripts d'ingestion Kafka.
* `exploration.py` & `data.csv` : Exploration et données brutes.
* `BI test projet.pbip` (et dossiers associés) : Fichiers source du projet Power BI.
* `dbt_project/` : Modèles SQL, tests et configuration dbt.
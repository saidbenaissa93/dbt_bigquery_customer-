import pandas as pd

# 1. Chargement du fichier
df = pd.read_csv('data.csv', encoding='utf-8')

print("=== 1. APERÇU GÉNÉRAL ===")
print(f"Nombre de lignes : {df.shape[0]}")
print(f"Nombre de colonnes : {df.shape[1]}\n")

# Afficher les 5 premières lignes
print("--- 5 Premières Lignes ---")
print(df.head())

print("\n=== 2. LISTE ET TYPES DES COLONNES ===")
# Utile pour repérer les types (int, float, object/string)
print(df.dtypes)

print("\n=== 3. VALEURS MANQUANTES (NULL / NaN) ===")
# Compter les valeurs nulles par colonne
null_counts = df.isnull().sum()
print(null_counts[null_counts > 0])  # Affiche uniquement les colonnes avec des manques

print("\n=== 4. DÉTECTION DES DOUBLONS ===")
# Vérifier la présence de lignes strictement identiques
duplicate_rows = df.duplicated().sum()
print(f"Nombre de lignes doublons : {duplicate_rows}")

# Si la colonne Transaction_ID existe, vérifier son unicité
if 'Transaction_ID' in df.columns:
    unique_tx = df['Transaction_ID'].nunique()
    print(f"Transactions uniques (Transaction_ID) : {unique_tx} / {len(df)}")

print("\n=== 5. STATISTIQUES DES COLONNES NUMÉRIQUES ===")
print(df.describe())
import requests
from train import load_data

# Chargement des données réelles avec le même traitement que dans train.py
DATA_PATH = "../data/air_quality_model.csv"
X, y = load_data(DATA_PATH)

# On prend une ligne réelle du dataset (ici la première)
sample = X.iloc[0].to_dict()

# Construction du JSON à envoyer à l'API
payload = {"features": sample}

print("Ligne de test utilisée :")
print(payload)

# Appel de l'API
url = "http://127.0.0.1:8000/predict"
response = requests.post(url, json=payload)

print("\nRéponse de l'API :")
print("Status code :", response.status_code)
print("Contenu :", response.json())


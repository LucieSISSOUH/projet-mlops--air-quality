# Image Python légère
FROM python:3.10-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copie des fichiers de l'API
COPY app.py /app/app.py
COPY model /app/model
COPY requirements.txt /app/requirements.txt

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Port exposé par l'API FastAPI
EXPOSE 8000

# Commande de lancement de l'API dans le conteneur
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

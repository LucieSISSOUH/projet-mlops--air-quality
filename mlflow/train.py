import argparse
import os
import sys

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

import mlflow
import mlflow.sklearn

# Nom de l'expérience dans MLflow
MLFLOW_EXP_NAME = "Air_Quality_RF_Binary"
RANDOM_STATE = 42


def load_data(csv_path: str):
    """Charge le CSV final et prépare X, y pour une classification binaire."""

    if not os.path.exists(csv_path):
        print(f"❌ Fichier introuvable : {csv_path}")
        sys.exit(1)

    df = pd.read_csv(csv_path)

    # Notre cible binaire : 0 / 1
    if "AQI_cat_simplified" not in df.columns:
        print("❌ La colonne 'AQI_cat_simplified' est absente du CSV.")
        sys.exit(1)

    y = df["AQI_cat_simplified"]

    # Colonnes à retirer des features
    drop_cols = [
        "AQI_cat_simplified",
        "AQI_cat",
        "Start_Date",
        "Unique ID",
        "Indicator ID",
        "Geo Join ID",
    ]
    drop_cols = [c for c in drop_cols if c in df.columns]

    X = df.drop(columns=drop_cols)

    # One-hot encoding pour les colonnes catégorielles
    cat_cols = X.select_dtypes(include="object").columns
    X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

    # Standardisation des colonnes numériques
    num_cols = X.select_dtypes(include=np.number).columns
    scaler = StandardScaler()
    X[num_cols] = scaler.fit_transform(X[num_cols])

    return X, y


def train_one_run(X, y, n_estimators, max_depth, run_name):
    """Une expérimentation MLflow : entrainement + logs"""

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred, average="binary")
    accuracy = model.score(X_test, y_test)

    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth if max_depth is not None else "None")
    mlflow.log_metric("f1_binary", f1)
    mlflow.log_metric("accuracy", accuracy)

    # Sauvegarde du modèle
    mlflow.sklearn.log_model(model, artifact_path="model")

    # Sauvegarde des noms de features (utile pour l'API ensuite)
    feature_names_path = "feature_names.txt"
    with open(feature_names_path, "w") as f:
        f.write(",".join(X_train.columns))
    mlflow.log_artifact(feature_names_path)

    print(f"{run_name} → F1 = {f1:.3f}, Acc = {accuracy:.3f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        type=str,
        default="../data/air_quality_model.csv",
        help="Chemin vers le CSV final.",
    )
    args = parser.parse_args()

    mlflow.set_experiment(MLFLOW_EXP_NAME)

    print(f"📂 Chargement des données : {args.data_path}")
    X, y = load_data(args.data_path)

    print("\n--- Lancement des runs MLflow (binaire) ---")

    with mlflow.start_run(run_name="Run-1-Base-100"):
        train_one_run(X, y, 100, None, "Run-1-Base-100")

    with mlflow.start_run(run_name="Run-2-Gros-500"):
        train_one_run(X, y, 500, None, "Run-2-Gros-500")

    with mlflow.start_run(run_name="Run-3-Petit-50"):
        train_one_run(X, y, 50, None, "Run-3-Petit-50")

    with mlflow.start_run(run_name="Run-4-Profondeur-10"):
        train_one_run(X, y, 300, 10, "Run-4-Profondeur-10")

    with mlflow.start_run(run_name="Run-5-Mix-150-15"):
        train_one_run(X, y, 150, 15, "Run-5-Mix-150-15")

    print("\n✅ Entraînement terminé. Consulte MLflow UI.")


if __name__ == "__main__":
    main()

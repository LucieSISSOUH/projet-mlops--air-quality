import os
import sys

import mlflow
from mlflow.tracking import MlflowClient

# Nom de l'expérience (doit être identique à celui utilisé dans train.py)
EXPERIMENT_NAME = "Air_Quality_RF_Binary"
METRIC_NAME = "f1_binary"

# Dossier où exporter le meilleur modèle pour l'API
EXPORT_DIR = os.path.join("..", "api", "model")


def get_best_run():
    """Retourne le meilleur run MLflow selon la métrique choisie."""
    client = MlflowClient()
    exp = client.get_experiment_by_name(EXPERIMENT_NAME)

    if exp is None:
        print(f"[ERREUR] L'expérience '{EXPERIMENT_NAME}' est introuvable.")
        sys.exit(1)

    # On trie les runs par la métrique décroissante
    runs = client.search_runs(
        experiment_ids=[exp.experiment_id],
        order_by=[f"metrics.{METRIC_NAME} DESC"],
        max_results=1
    )

    if not runs:
        print("[ERREUR] Aucun run trouvé.")
        sys.exit(1)

    best_run = runs[0]
    best_metric_value = best_run.data.metrics.get(METRIC_NAME, None)

    print(f"[OK] Meilleur run : {best_run.info.run_id} (f1 = {best_metric_value:.3f})")

    return best_run


def export_model_and_artifacts(best_run):
    """Télécharge le modèle MLflow + artefacts dans api/model/."""
    client = MlflowClient()

    # Création du dossier s'il n'existe pas
    os.makedirs(EXPORT_DIR, exist_ok=True)

    run_id = best_run.info.run_id

    print("[INFO] Téléchargement du modèle MLflow...")
    client.download_artifacts(run_id=run_id, path="model", dst_path=EXPORT_DIR)

    print("[INFO] Téléchargement du fichier des features si disponible...")
    try:
        client.download_artifacts(run_id=run_id, path="feature_names.txt", dst_path=EXPORT_DIR)
    except Exception:
        print("[AVERTISSEMENT] Le fichier feature_names.txt est absent.")

    # Infos utiles
    info_path = os.path.join(EXPORT_DIR, "best_run_info.txt")
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(f"run_id={run_id}\n")
        f.write(f"{METRIC_NAME}={best_run.data.metrics.get(METRIC_NAME, 'NA')}\n")
        f.write(f"params={best_run.data.params}\n")

    print(f"[OK] Modèle exporté dans : {os.path.abspath(EXPORT_DIR)}")


def main():
    print("[INFO] Sélection du meilleur modèle en cours...")
    best_run = get_best_run()
    export_model_and_artifacts(best_run)
    print("[INFO] Sélection terminée.")


if __name__ == "__main__":
    main()

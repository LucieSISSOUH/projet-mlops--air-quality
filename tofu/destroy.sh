#!/bin/bash

# ==========================================================
# Script de destruction de l'infrastructure OpenTofu
# Démolit toutes les ressources provisionnées sur AWS.
# ==========================================================

# 1. Définition des variables (optionnel, mais recommandé pour la clarté)

# Assurez-vous d'exporter vos identifiants AWS si vous ne les utilisez pas via un profil
# export AWS_ACCESS_KEY_ID="VOTRE_CLE_ACCES"
# export AWS_SECRET_ACCESS_KEY="VOTRE_CLE_SECRETE"

# Assurez-vous d'être dans le bon répertoire OpenTofu
cd "$(dirname "$0")"

# 2. Exécution de la commande de destruction
# On utilise l'option -auto-approve pour éviter la confirmation manuelle (non recommandé en prod !)

echo "Démarrage de la destruction des ressources AWS provisionnées par OpenTofu..."

# Remplacez './tofu' par le chemin absolu de votre exécutable OpenTofu si nécessaire, 
# comme vous l'avez fait pour le 'plan' et le 'apply'.

/usr/bin/env tofu destroy \
    -auto-approve \
    -var="ssh_public_key_path=/home/ubuntu/.ssh/myKeyML.pub" \
    -var="ssh_private_key_path=/home/ubuntu/.ssh/myKeyML.pem" 
    
echo "Destruction terminée."
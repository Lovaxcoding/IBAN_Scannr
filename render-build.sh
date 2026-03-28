#!/usr/bin/env bash
# Arrêter le script en cas d'erreur
set -o errexit

# Mettre à jour les paquets et installer Tesseract
# Note: On utilise apt-get avec les droits disponibles sur Render
apt-get update && apt-get install -y tesseract-ocr

# Installer les dépendances Python
pip install -r requirements.txt
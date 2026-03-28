#!/usr/bin/env bash
set -o errexit

apt-get update
# On installe Tesseract ET Poppler (pour les PDF)
apt-get install -y tesseract-ocr poppler-utils

pip install -r requirements.txt
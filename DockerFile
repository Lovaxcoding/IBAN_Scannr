# Image de base Python
FROM python:3.11-slim

# Installation des dépendances système pour l'OCR et les PDF
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Dossier de travail
WORKDIR /app

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Port par défaut de Render
ENV PORT=10000
EXPOSE 10000

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
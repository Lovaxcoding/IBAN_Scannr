from fastapi import FastAPI, UploadFile, File
import shutil
import os
import pytesseract
from scalar_fastapi import get_scalar_api_reference
from PIL import Image
from pdf2image import convert_from_path
from validation_iban import extract_and_validate_iban
from fastapi.middleware.cors import CORSMiddleware

# --- CONFIGURATION SPÉCIFIQUE POUR RENDER ---
# On force la détection du binaire Tesseract installé via apt-get
tesseract_bin = shutil.which("tesseract")
if not tesseract_bin:
    standard_path = "/usr/bin/tesseract"
    if os.path.exists(standard_path):
        tesseract_bin = standard_path

if tesseract_bin:
    pytesseract.pytesseract.tesseract_cmd = tesseract_bin
# --------------------------------------------

app = FastAPI(
    title="IBAN Scanner API",
    description="API de reconnaissance optique (OCR) pour la vérification d'IBAN via images.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post(
    "/scan-iban", 
    tags=["Analyse OCR"],
    summary="Scanner une image pour extraire un IBAN",
    description="Cette route reçoit une image ou un PDF, l'analyse via Tesseract et valide l'IBAN."
)
async def scan_iban(file: UploadFile = File(...)):
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Enregistrement du fichier
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    extracted_text = ""
    
    try:
        # 1. Extraction du texte selon le format
        if file.filename.lower().endswith(".pdf"):
            # Note : pdf2image nécessite 'poppler-utils' sur le système
            pages = convert_from_path(save_path, first_page=1, last_page=1)
            for page in pages:
                extracted_text += pytesseract.image_to_string(page)
        else:
            image = Image.open(save_path)
            extracted_text = pytesseract.image_to_string(image)

        # 2. Validation de l'IBAN
        result = extract_and_validate_iban(extracted_text)

        # 3. Nettoyage immédiat du fichier (Sécurité/RGPD)
        if os.path.exists(save_path):
            os.remove(save_path)

        return {
            "status": "success",
            "filename": file.filename,
            "is_iban": result["is_valid"],
            "data": {
                "iban": result["iban"],
                "country": result["country"]
            },
            "debug": extracted_text[:100] # On limite l'affichage pour la clarté
        }

    except Exception as e:
        # Nettoyage même en cas d'erreur
        if os.path.exists(save_path):
            os.remove(save_path)
        return {"status": "error", "message": f"Erreur lors de l'analyse : {str(e)}"}
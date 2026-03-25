from fastapi import FastAPI, UploadFile, File
import shutil
import os
from scalar_fastapi import get_scalar_api_reference
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from validation_iban import extract_and_validate_iban
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="IBAN Scanner API",
    description="API de reconnaissance optique (OCR) pour la vérification d'IBAN via images.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En développement, on autorise tout
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
    description="Cette route reçoit une image (JPG/PNG), l'enregistre temporairement et prépare l'analyse OCR."
)
async def scan_iban(file: UploadFile = File(...)):
    save_path = f"uploads/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    extracted_text = ""
    
    try:
        # 1. Extraction du texte (selon le format)
        if file.filename.lower().endswith(".pdf"):
            pages = convert_from_path(save_path, first_page=1, last_page=1)
            for page in pages:
                extracted_text += pytesseract.image_to_string(page)
        else:
            image = Image.open(save_path)
            extracted_text = pytesseract.image_to_string(image)

        # 2. Validation de l'IBAN (Commun à tous les formats)
        # On place l'appel ici pour que 'result' existe toujours !
        result = extract_and_validate_iban(extracted_text)

        # 3. Réponse finale
        return {
            "status": "success",
            "filename": file.filename,
            "message": "Analyse PDF/Image terminée",
            "is_iban": result["is_valid"],
            "data": {
                "iban": result["iban"],
                "country": result["country"]
            },
            "extracted_text_debug": extracted_text # Utile pour débugger
        }
    except Exception as e:
        return {"status": "error", "message": f"Erreur lors de l'analyse : {str(e)}"}
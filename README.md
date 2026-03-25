# IBAN_Scannr

**IBAN_Scannr** is an intelligent micro-service designed to automate the extraction and mathematical validation of bank account details (IBAN) from scanned documents (images and PDFs).

By combining the power of OCR (Tesseract) with rigorous Modulo 97 checksum validation, it transforms raw visual data into certified banking information.

## 🚀 Features
- **Multi-format Support:** Process `.png`, `.jpg`, `.jpeg`, and `.pdf` files.
- **AI-Powered OCR:** High-precision text extraction using Pytesseract.
- **Fintech Validation:** Real-time International Checksum verification.
- **Smart Cleaning:** Advanced Regex filtering to isolate the IBAN from textual noise (e.g., "BIC Code", "Account Holder").
- **Integration Ready:** REST API built with FastAPI, easily connectable to WordPress (Forminator), React, or Flutter.

## 🛠 Tech Stack
| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| API Framework | FastAPI |
| OCR Engine | Tesseract OCR |
| Validation | Schwifty (IBAN/BIC) |
| Image Processing | Pillow & PDF2Image |

## 🔧 Installation & Setup
1. **Prerequisites**
Ensure Tesseract is installed on your machine:
```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr

# macOS
brew install tesseract
```
2. **Dependency Installation**
```bash
pip install fastapi uvicorn pytesseract pillow pdf2image schwifty scalar-fastapi
```
3. **Run the Server**
```bash
uvicorn main:app --reload
```
The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000). Interactive documentation (Scalar) can be found at `/scalar`.

## 🧠 Technical Challenge: The "Sticky Character" Problem
A major hurdle in this project was handling "sticky characters" during OCR extraction. Often, the IBAN is immediately followed by labels like CODEBIC or SWIFT without spaces.

**Implemented Solution:** A dynamic validation loop that tests substrings of increasing lengths (from 15 to 34 characters). This identifies the exact sequence validated by the checksum algorithm, effectively ignoring adjacent textual noise.

## 🔌 WordPress Integration
This project has been successfully tested on WordPress using the Forminator plugin. A custom PHP hook (`forminator_custom_form_submit_errors`) intercepts the upload to validate the bank details in real-time before final submission.

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.

Developed with passion by Lovasoa Nantenaina 

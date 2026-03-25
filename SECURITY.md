# 🛡️ Security Policy

## Supported Versions

We are committed to ensuring the security of the IBAN_Scannr API. The following versions are currently receiving security updates:

| Version | Supported | Status |
|---------|------------|---------|
| 1.0.x   | :white_check_mark: | Current Stable Release |
| < 1.0 | :x: | Development/Beta Phases |

## Reporting a Vulnerability

Security is a top priority for this project. If you discover a security vulnerability, please follow the steps below:

1. **Do not open a public Issue:** To prevent exposing the vulnerability before it is fixed.
2. **Private Reporting:** Please send a detailed email to [your-email@example.com](mailto:your-email@example.com) describing the vulnerability, the steps to reproduce it, and the potential impact.
3. **Response Time:** You can expect an acknowledgment of your report within 48 hours.
4. **Resolution:** Once the vulnerability is validated, a fix will be deployed. Contributors may be credited in the release notes if they wish.

## 🔒 Implemented Security Measures

As part of this micro-service, the following measures have been implemented to protect sensitive banking data:

- **Ephemeral Processing:** Uploaded documents (Images/PDFs) are processed and should be purged immediately after analysis to prevent PII (Personally Identifiable Information) leaks.
- **Input Sanitization:** Strict Regex filtering is used during the OCR process to prevent malicious character injections or buffer overflows.
- **Dependency Monitoring:** We use tools to ensure that libraries like FastAPI, Pytesseract, and Schwifty are up to date and free of known CVEs.

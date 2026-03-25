import re
from schwifty import IBAN

import re
from schwifty import IBAN


def extract_and_validate_iban(text):
    clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
    print(clean_text)
    
    # On cherche :
# [A-Z]{2}\d{2} : 2 lettres + 2 chiffres (Le début standard)
# [A-Z0-9]{11,30} : La suite, mais on va la rendre moins gourmande
# (?![A-Z]) : "Stop si le caractère suivant est une lettre" (Lookahead)

    iban_pattern = r'[A-Z]{2}\d{2}[0-9A-Z]{11,30}?(?=[A-Z]{2,}|$)'
    
    matches = re.findall(iban_pattern, clean_text)
    print(f"DEBUG MATCHES FOUND: {matches}") # Ajoute cette ligne !
    
    for potential_iban in matches:
        # Nettoyage des lettres collées à la fin (ex: CODEBIC)
        clean_potential = re.sub(r'[A-Z]+$', '', potential_iban)
        
        for length in range(15, len(clean_potential) + 1):
            short_potential = clean_potential[:length]
            try:
                iban_obj = IBAN(short_potential)
                return {
                    "is_valid": True,
                    "iban": iban_obj.formatted,
                    "country": iban_obj.country_code
                }
            except Exception as e:
                # DEBUG : Décommente la ligne suivante pour voir l'erreur de Schwifty
                # print(f"Schwifty Error for {short_potential}: {e}")
                continue
                
    return {"is_valid": False, "iban": None, "country": None}

# Validation iban 
if __name__ == "__main__":
    test_text = "Voici mon RIB, mon IBAN est FR7630006000011234567890123 merci."
    print(extract_and_validate_iban(test_text))
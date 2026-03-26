/**
 * Validation IBAN via API FastAPI pour Forminator
 */
add_filter( 'forminator_custom_form_submit_errors', function( $submit_errors, $form_id, $field_data_array ) {
    
    // 1. On cible le formulaire ID 7
    if ( (int) $form_id !== 7 ) {
        return $submit_errors;
    }

    // 2. Identification du champ d'upload
    $file_field = 'upload-1'; 
    if ( empty( $_FILES[$file_field]['tmp_name'] ) ) {
        return $submit_errors; 
    }

    // 3. Configuration de l'appel à ton API Python
    // Note : Utilise l'URL Render 
    $api_url = 'https://iban-scannr.onrender.com/scan-iban'; 
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $api_url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 45); // L'OCR peut être lent sur de gros fichiers
    curl_setopt($ch, CURLOPT_POSTFIELDS, [
        'file' => new CURLFile(
            $_FILES[$file_field]['tmp_name'], 
            $_FILES[$file_field]['type'], 
            $_FILES[$file_field]['name']
        )
    ]);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    // 4. Analyse CRITIQUE du contenu de la réponse
    if ( $http_code === 200 ) {
        $result = json_decode($response, true);
        
        // on vérifie le contenu du JSON, pas juste le code 200
        if ( !isset($result['is_iban']) || $result['is_iban'] === false ) {
            $submit_errors[] = [ 
                $file_field => "Analyse terminée : Aucun IBAN valide n'a été détecté sur ce document." 
            ];
        }
    } else {
        // Si l'API est éteinte ou crash
        $submit_errors[] = [ 
            $file_field => "Le service d'IA (FastAPI) est actuellement injoignable. Code: " . $http_code
        ];
    }

    return $submit_errors;
}, 10, 3 );

add_filter( 'forminator_custom_form_submit_errors', function( $submit_errors, $form_id, $field_data_array ) {
    
    // 1. On cible uniquement le formulaire ID 7
    if ( (int) $form_id !== 7 ) {
        return $submit_errors;
    }

    // 2. Récupérer le nom du champ d'upload 
    $file_field = 'upload-1'; 
    if ( empty( $_FILES[$file_field]['tmp_name'] ) ) {
        return $submit_errors; 
    }

    // 3. Configuration de l'appel à ton Lab Python
    // Remplace 127.0.0.1 par l'IP du serveur si WordPress est distant
    $api_url = 'http://127.0.0.1:8000/scan-iban'; 
    
    $file_tmp  = $_FILES[$file_field]['tmp_name'];
    $file_type = $_FILES[$file_field]['type'];
    $file_name = $_FILES[$file_field]['name'];

    // 4. Envoi via CURL (Multipart/form-data)
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $api_url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30); // Laisse le temps à l'OCR de travailler
    curl_setopt($ch, CURLOPT_POSTFIELDS, [
        'file' => new CURLFile($file_tmp, $file_type, $file_name)
    ]);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    // 5. Analyse de la réponse de ton API
    if ( $http_code === 200 ) {
        $result = json_decode($response, true);
        
        // Si l'IBAN n'est pas trouvé ou invalide selon ton script Python
        if ( isset($result['is_iban']) && $result['is_iban'] === false ) {
            $submit_errors[] = [ 
                $file_field => "Erreur : L'IBAN sur ce document est invalide ou illisible. Veuillez fournir un RIB officiel." 
            ];
        }
    } else {
        // En cas de crash de l'API Python (optionnel)
        $submit_errors[] = [ $file_field => "Le service de vérification est temporairement indisponible." ];
    }

    return $submit_errors;
}, 10, 3 );
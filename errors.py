class JobHubError(Exception):
    MESSAGE_KEYS = {
        "adzuna": {
            "missing_credentials": "adzuna_missing_credentials",
            "timeout": "adzuna_timeout",
            "400": "adzuna_incorrect_parameters",
            "404": "adzuna_resource_not_found",
            "410": "adzuna_authorisation_failed",
            "429": "adzuna_rate_limit",
            "5xx": "adzuna_server_error",
            "default_status_code": "adzuna_request_failed",
            "api_repsonse_not_valid_list_of_jobs": "adzuna_invalid_job_list",
            "dict_format_necessary": "adzuna_dictionary_required",
            "valid_job_id_necessary": "adzuna_job_id_required",
            "request_failed_or_non_valid": "adzuna_request_failed_or_non_valid",
            "adzuna_non_valid_json": "adzuna_non_valid_json",
            "adzuna_field_not_string": "adzuna_field_not_string",
            "adzuna_required_field_is_empty": "adzuna_required_field_is_empty",
            "adzuna_required_field_missing": "adzuna_required_field_missing",
            "adzuna_field_not_dictionary": "adzuna_field_not_dictionary",
            "adzuna_field_salary_is_predicted_not_boolean": "adzuna_field_salary_is_predicted_not_boolean",
            "adzuna_field_not_number": "adzuna_field_not_number",

        },
        "json_config": {
            "json_config_non_valid_json": "json_config_non_valid_json",
            "json_config_read_failed": "json_config_read_failed",
            "json_config_invalid_country": "json_config_invalid_country",
            "json_config_missing_jobs": "json_config_missing_jobs",
            "json_config_missing_location": "json_config_missing_location",
            "json_config_invalid_text": "json_config_invalid_text",
            "json_config_not_object": "json_config_not_object",
            "json_config_unknown_fields": "json_config_unknown_fields",
            "json_config_invalid_integer": "json_config_invalid_integer",
            "json_config_invalid_boolean": "json_config_invalid_boolean",

        }
    }

    def __init__(self, *, source, code, **values):
        # Diese Angaben bleiben am Fehlerobjekt gespeichert.
        self.source = source
        self.code = str(code)
        self.values = values

        # Zuordnungen für die angegebene Quelle auswählen.
        keys = self.MESSAGE_KEYS.get(source, {})

        lookup_code = self.code

        # Alle HTTP-Serverfehler verwenden dieselbe Meldung.
        if self.code.isdigit() and 500 <= int(self.code) <= 599:
            lookup_code = "5xx"

        # Unbekannter Code: allgemeine Meldung der Quelle verwenden.
        # Unbekannte Quelle: allgemeine Fehlermeldung verwenden.
        self.message_key = keys.get(
            lookup_code,
            keys.get("default_status_code", "error_unknown"),
        )

        # Technische Beschreibung für die eingebaute Exception.
        # Hier wird noch nichts übersetzt.
        super().__init__(f"{self.source}: {self.code}")
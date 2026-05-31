INPUT_SCHEMA_ADD_CONTRACT_SIGNER = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract to add the signer to."},
        "name": {"type": "string", "description": "Signer's name."},
        "email": {"type": "string", "description": "Signer's email address."},
        "mobile": {"type": "string", "description": "Signer's mobile number (E.123 format, e.g. +12481234567). Non-US numbers must start with the country code."},
        "company_name": {"type": "string", "description": "Signer's company name."},
        "signing_order": {"type": "string", "description": "Order in which signers receive the contract; same number signers are notified together. By default, sequential."},
        "auto_sign": {"type": "string", "description": "Automatically signs document if 'yes'; only for your signature, not for other signers.", "enum": ["yes", "no"]},
        "signature_request_delivery_methods": {
            "type": "array",
            "description": "Methods for delivering the signature request. Empty list skips sending. Default calculated. Requires the relevant contact details.",
            "items": {
                "type": "string",
                "enum": ["email", "sms"],
            },
        },
        "signed_document_delivery_method": {
            "type": "string",
            "description": "Method to deliver signed document (email, sms). Usually required by law. Default calculated.",
            "enum": ["email", "sms"],
        },
        "multi_factor_authentications": {
            "type": "array",
            "description": "Authentication methods for the signer (6 digit email or SMS code, live photo ID check). Requires the relevant contact details.",
            "items": {
                "type": "string",
                "enum": ["sms_verification_code", "email_verification_code", "photo_id"],
            },
        },
        "redirect_url": {"type": "string", "description": "URL for signer redirection post-signing."},
    },
    "required": ["contract_id"],
}

INPUT_SCHEMA_UPDATE_CONTRACT_SIGNER = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract the signer belongs to."},
        "signer_id": {"type": "string", "description": "GUID of the signer to update."},
        "name": {"type": "string", "description": "Signer's name."},
        "email": {"type": "string", "description": "Signer's email address."},
        "mobile": {"type": "string", "description": "Signer's mobile number (E.123 format, e.g. +12481234567). Non-US numbers must start with the country code."},
        "company_name": {"type": "string", "description": "Signer's company name."},
        "signature_request_delivery_methods": {
            "type": "array",
            "description": "Methods for delivering the signature request. Empty list skips sending. Default calculated. Requires the relevant contact details.",
            "items": {
                "type": "string",
                "enum": ["email", "sms"],
            },
        },
        "signed_document_delivery_method": {
            "type": "string",
            "description": "Method to deliver signed document (email, sms). Usually required by law. Default calculated.",
            "enum": ["email", "sms"],
        },
        "multi_factor_authentications": {
            "type": "array",
            "description": "Authentication methods for the signer (6 digit email or SMS code, live photo ID check). Requires the relevant contact details.",
            "items": {
                "type": "string",
                "enum": ["sms_verification_code", "email_verification_code", "photo_id"],
            },
        },
        "redirect_url": {"type": "string", "description": "URL for signer redirection post-signing."},
    },
    "required": ["contract_id", "signer_id"],
}

INPUT_SCHEMA_RESEND_CONTRACT_SIGNER_REQUEST = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract the signer belongs to."},
        "signer_id": {"type": "string", "description": "GUID of the signer to send the sign request to."},
    },
    "required": ["contract_id", "signer_id"],
}

INPUT_SCHEMA_DELETE_CONTRACT_SIGNER = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract the signer belongs to."},
        "signer_id": {"type": "string", "description": "GUID of the signer to delete."},
    },
    "required": ["contract_id", "signer_id"],
}

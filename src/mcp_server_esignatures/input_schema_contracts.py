from .input_schema_document_elements import INPUT_SCHEMA_DOCUMENT_ELEMENTS_ITEMS

INPUT_SCHEMA_CREATE_CONTRACT = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string", "description": "GUID of a mobile-friendly contract template within eSignatures. The template provides content, title, and labels. Required unless document_elements is provided."},
        "title": {"type": "string", "description": "Sets the contract's title, which appears as the first line in contracts and PDF files, in email subjects, and overrides the template's title."},
        "locale": {"type": "string", "description": "Language for signer page and emails.", "enum": ["es", "hu", "da", "id", "gr", "ro", "sk", "pt", "hr", "sl", "de", "it", "pl", "rs", "sv", "en", "ja", "en-GB", "fr", "cz", "vi", "no", "zh-CN", "nl"]},
        "metadata": {"type": "string", "description": "Custom data for contract owners and webhook notifications; e.g. internal IDs."},
        "expires_in_hours": {"type": "string", "description": "Sets contract expiry time in hours; expired contracts can't be signed. Expiry period can be extended per contract in eSignatures."},
        "custom_webhook_url": {"type": "string", "description": "Overrides default webhook HTTPS URL for this contract, defined on the API page in eSignatures. Retries 6 times with 1 hour delays, timeout is 20 seconds."},
        "assigned_user_email": {"type": "string", "description": "Assigns an eSignatures user as contract owner with edit/view/send rights and notification settings. Contract owners get email notifications for signings and full contract completion if enabled on their Profile."},
        "labels": {"type": "array", "description": "Assigns labels to the contract, overriding template labels. Labels assist in organizing contracts without using folders.", "items": {"type": "string"}},
        "test": {"type": "string", "description": "Marks contract as 'demo' with no fees; adds DEMO stamp, disables reminders.", "enum":["yes", "no"]},
        "save_as_draft": {"type": "string", "description": "Saves contract as draft for further editing; draft can be edited and sent via UI. URL: https://esignatures.com/contracts/contract_id/edit, where contract_id is in the API response.", "enum":["yes", "no"]},
        "signers": {
           "type": "array",
           "description": "List of individuals required to sign the contract. Only include specific persons with their contact details; do not add generic signers.",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Signer's name."},
                    "email": {"type": "string", "description": "Signer's email address."},
                    "mobile": {"type": "string", "description": "Signer's mobile number (E.123 format)."},
                    "company_name": {"type": "string", "description": "Signer's company name."},
                    "signing_order": {"type": "string", "description": "Order in which signers receive the contract; same number signers are notified together. By default, sequential."},
                    "auto_sign": {"type": "string", "description": "Automatically signs document if 'yes'; only for your signature not for other signers."},
                    "signature_request_delivery_methods": {
                        "type": "array",
                        "description": "Methods for delivering signature request. Empty list skips sending. Default calculated. Requires contact details.",
                        "items": {
                            "type": "string",
                            "enum": ["email", "sms"]
                        }
                     },
                    "signed_document_delivery_method": {
                        "type": "string",
                        "description": "Method to deliver signed document (email, sms). Usually required by law. Default calculated.",
                        "enum": ["email", "sms"]
                     },
                    "multi_factor_authentications": {
                        "type": "array",
                        "description": "Authentication methods for signers (sms_verification_code, email_verification_code). Requires the relevant contact details.",
                        "items": {
                            "type": "string",
                            "enum": ["sms_verification_code", "email_verification_code"]
                        }
                     },
                    "redirect_url": {"type": "string", "description": "URL for signer redirection post-signing."},
                },
                "required": ["name"]
           }
        },
        "placeholder_fields": {
           "type": "array",
           "description": "Replaces text placeholders in templates when creating a contract. Example: {{interest_rate}}. Do not add placeholder values when creating a draft.",
            "items": {
                "type": "object",
                "properties": {
                    "api_key": {"type": "string", "description": "The template's placeholder key, e.g., for {{interest_rate}}, api_key is 'interest_rate'."},
                    "value": {"type": "string", "description": "Text that replaces the placeholder."},
                    "document_elements": {
                        "type": "array",
                        "description": "Allows insertion of custom elements like headers, text, images into placeholders.",
                        "items": INPUT_SCHEMA_DOCUMENT_ELEMENTS_ITEMS
                    }
                }
           }
        },
        "document_elements": {
            "type": "array",
            "description": "Customize document content with headers, text, images, etc. Owners can manually replace {{placeholder fields}} in the eSignatures editor, and signers can fill in Signer fields. Use placeholders for signer names unless names are already provided. The contract title is automatically added as the first line.",
            "items": INPUT_SCHEMA_DOCUMENT_ELEMENTS_ITEMS
        },
        "signer_fields": {
            "type": "array",
            "description": "Set default values for Signer fields.",
            "items": {
                "type": "object",
                "properties": {
                    "signer_field_id": {"type": "string", "description": "Signer field ID of the Signer field, defined in the template or document_elements."},
                    "default_value": {"type": "string", "description": "Default input value (use '1' for checkboxes and radio buttons, 'YYYY-mm-dd' for dates)."}
                },
                "required": ["signer_field_id"]
            }
        },
        "emails": {
            "type": "object",
            "description": "Customize email communications for signing and final documents.",
            "properties": {
                "signature_request_subject": {"type": "string", "description": "Email subject for signature request emails."},
                "signature_request_text": {"type": "string", "description": "Email body of signature request email; use __FULL_NAME__ for personalization. First line is bold and larger."},
                "final_contract_subject": {"type": "string", "description": "Email subject for the final contract email."},
                "final_contract_text": {"type": "string", "description": "Body of final contract email; use __FULL_NAME__ for personalization. First line is bold and larger."},
                "cc_email_addresses": {"type": "array", "description": "Email addresses CC'd when sending the signed contract PDF.", "items": {"type": "string"} },
                "reply_to": {"type": "string", "description": "Custom reply-to email address (defaults to support email if not set)."}
            },
        },
        "custom_branding": {
            "type": "object",
            "description": "Customize branding for documents and emails.",
            "properties": {
                "company_name": {"type": "string", "description": "Custom company name shown as the sender."},
                "logo_url": {"type": "string", "description": "URL for custom logo (PNG, recommended 400px size)."}
            },
        },
        "contract_source": {"type": "string", "enum": ["mcpserver"], "description": "Identifies the originating system. Currently only mcpserver supported for MCP requests."},
        "mcp_query": {"type": "string", "description": "The original text query that the user typed which triggered this MCP command execution. Used for logging and debugging purposes."}
    },
    "required": ["contract_source", "mcp_query"],
}

INPUT_SCHEMA_QUERY_CONTRACT = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract (draft contracts can't be queried, only sent contracts)."},
    },
    "required": ["contract_id"],
}

INPUT_SCHEMA_WITHDRAW_CONTRACT = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract to be withdrawn."},
    },
    "required": ["contract_id"],
}

INPUT_SCHEMA_DELETE_CONTRACT = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract to be deleted."},
    },
    "required": ["contract_id"],
}

INPUT_SCHEMA_LIST_RECENT_CONTRACTS = {
    "type": "object",
    "properties": {},
    "required": [],
}

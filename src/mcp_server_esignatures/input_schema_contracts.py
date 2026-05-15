from .input_schema_markdown import MARKDOWN_CONTENT_DESCRIPTION

INPUT_SCHEMA_CREATE_CONTRACT = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string", "description": "GUID of a contract template within eSignatures. The template provides content, title, and labels. Provide either template_id or markdown for the content, not both."},
        "markdown": {
            "type": "string",
            "description": "Ad-hoc contract body, used to create a contract WITHOUT a template. Provide either template_id or markdown, not both. " + MARKDOWN_CONTENT_DESCRIPTION,
        },
        "title": {"type": "string", "description": "Sets the contract's title, which appears as the first line in contracts and PDF files, in email subjects, and overrides the template's title. Recommended when using the `markdown` parameter, as there is no template title to fall back on."},
        "locale": {"type": "string", "description": "Language for signer page and emails.", "enum": ["cz", "da", "de", "el", "en", "en-GB", "es", "fi", "fr", "hr", "hu", "id", "it", "ja", "nl", "no", "pl", "pt", "ro", "rs", "sk", "sl", "sv", "vi", "zh-CN"]},
        "metadata": {"type": "string", "description": "Custom data for contract owners and webhook notifications; e.g. internal IDs."},
        "expires_in_hours": {"type": "string", "description": "Sets contract expiry time in hours; expired contracts can't be signed. Expiry period can be extended per contract in eSignatures."},
        "custom_webhook_url": {"type": "string", "description": "Overrides default webhook HTTPS URL for this contract, defined on the API page in eSignatures. Retries 6 times with 1 hour delays, timeout is 20 seconds."},
        "assigned_user_email": {"type": "string", "description": "Assigns an eSignatures user as contract owner with edit/view/send rights and notification settings. Contract owners get email notifications for signings and full contract completion if enabled on their Profile."},
        "labels": {"type": "array", "description": "Assigns labels to the contract, overriding template labels. Labels assist in organizing contracts without using folders.", "items": {"type": "string"}},
        "test": {"type": "string", "description": "Marks contract as 'demo' with no fees; adds DEMO stamp, disables reminders.", "enum": ["yes", "no"]},
        "save_as_draft": {"type": "string", "description": "Saves contract as draft for further editing; draft can be edited and sent via UI. URL: https://esignatures.com/contracts/contract_id/edit, where contract_id is in the API response.", "enum": ["yes", "no"]},
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
                            "enum": ["email", "sms"],
                        },
                    },
                    "signed_document_delivery_method": {
                        "type": "string",
                        "description": "Method to deliver signed document (email, sms). Usually required by law. Default calculated, empty list skips sending.",
                        "enum": ["email", "sms"],
                    },
                    "multi_factor_authentications": {
                        "type": "array",
                        "description": "Authentication methods for signers (6 digit email or SMS code, live photo ID check). Requires the relevant contact details.",
                        "items": {
                            "type": "string",
                            "enum": ["sms_verification_code", "email_verification_code", "photo_id"],
                        },
                    },
                    "redirect_url": {"type": "string", "description": "URL for signer redirection post-signing."},
                },
                "required": ["name"],
            },
        },
        "placeholder_fields": {
            "type": "array",
            "description": "Replaces text placeholders in the template when creating a contract. Example: {{interest_rate}}. Do not add placeholder values when creating a draft.",
            "items": {
                "type": "object",
                "properties": {
                    "placeholder_key": {"type": "string", "description": "The template's placeholder key, e.g., for {{interest_rate}}, placeholder_key is 'interest_rate'."},
                    "replace_with_text": {"type": "string", "description": "Plain text that replaces the placeholder."},
                    "replace_with_markdown": {
                        "type": "string",
                        "description": "Markdown content that replaces the placeholder. " + MARKDOWN_CONTENT_DESCRIPTION,
                    },
                    "replace_with_template": {"type": "string", "description": "GUID of another template; its full content replaces the placeholder."},
                },
                "required": ["placeholder_key"],
            },
        },
        "signer_fields": {
            "type": "array",
            "description": "Set default values for Signer fields defined in the template.",
            "items": {
                "type": "object",
                "properties": {
                    "signer_field_id": {"type": "string", "description": "Signer field ID of the given Signer field in the content."},
                    "default_value": {"type": "string", "description": "Default input value (use '1' for checkboxes and radio buttons, 'YYYY-mm-dd' for dates)."},
                },
                "required": ["signer_field_id"],
            },
        },
        "emails": {
            "type": "object",
            "description": "Customize email communications for signing and final documents.",
            "properties": {
                "signature_request_subject": {"type": "string", "description": "Email subject for signature request emails."},
                "signature_request_text": {"type": "string", "description": "Email body of signature request email; use __FULL_NAME__ for personalization. First line is bold and larger."},
                "final_contract_subject": {"type": "string", "description": "Email subject for the final contract email."},
                "final_contract_text": {"type": "string", "description": "Body of final contract email; use __FULL_NAME__ for personalization. First line is bold and larger."},
                "cc_email_addresses": {"type": "array", "description": "Email addresses CC'd when sending the signed contract PDF.", "items": {"type": "string"}},
                "reply_to": {"type": "string", "description": "Custom reply-to email address (defaults to support email if not set)."},
            },
        },
        "custom_branding": {
            "type": "object",
            "description": "Customize branding for documents and emails.",
            "properties": {
                "company_name": {"type": "string", "description": "Custom company name shown as the sender."},
                "logo_url": {"type": "string", "description": "URL for custom logo (PNG, recommended 400px size)."},
            },
        },
        "contract_source": {"type": "string", "enum": ["mcpserver"], "description": "Identifies the originating system. Currently only mcpserver supported for MCP requests."},
        "mcp_query": {"type": "string", "description": "The original text query that the user typed which triggered this MCP command execution. Used for logging and debugging purposes."},
    },
    "required": ["contract_source", "mcp_query"],
    "oneOf": [
        {"required": ["template_id"]},
        {"required": ["markdown"]},
    ],
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
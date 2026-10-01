from .input_schema_markdown import MARKDOWN_CONTENT_DESCRIPTION

_VERIFICATION_METHOD = {
    "type": "string",
    "description": "How signers are verified before signing: a 6 digit code sent via SMS or email.",
    "enum": ["sms_verification_code", "email_verification_code"],
}

INPUT_SCHEMA_CREATE_CONTRACT_LINK = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Title of the new Contract link; shown to signers and used for contracts signed via the link."},
        "template_id": {"type": "string", "description": "ID of a contract template within eSignatures.com that provides the content. Provide either template_id or markdown for the content, not both."},
        "markdown": {
            "type": "string",
            "description": "Ad-hoc content, used to create a Contract link WITHOUT a template. Provide either template_id or markdown, not both. " + MARKDOWN_CONTENT_DESCRIPTION,
        },
        "verification_method": _VERIFICATION_METHOD,
        "redirect_url": {"type": "string", "description": "URL the signer is redirected to after signing."},
        "thank_you_message": {"type": "string", "description": "Message shown to the signer after signing. Only shown when no redirect_url is set."},
        "cc_email_addresses": {"type": "array", "description": "Email addresses that receive a copy of each signed contract.", "items": {"type": "string"}},
        "second_signer_user_email": {"type": "string", "description": "Email address of a user in your eSignatures.com account who counter-signs each contract."},
        "second_signer_auto_sign": {"type": "string", "description": "When 'yes', the second signer's signature is applied automatically. Only applies when a second signer is set. Defaults to no.", "enum": ["yes", "no"]},
        "test": {"type": "string", "description": "When 'yes', contracts signed via this link are test contracts with no fees; adds DEMO stamp. Defaults to no.", "enum": ["yes", "no"]},
    },
    "oneOf": [
        {"required": ["template_id"]},
        {"required": ["markdown"]},
    ],
    "required": ["title", "verification_method"],
}

INPUT_SCHEMA_QUERY_CONTRACT_LINK = {
    "type": "object",
    "properties": {
        "contract_link_id": {"type": "string", "description": "ID of the Contract link."},
    },
    "required": ["contract_link_id"],
}

INPUT_SCHEMA_QUERY_CONTRACT_LINK_CONTENT = {
    "type": "object",
    "properties": {
        "contract_link_id": {"type": "string", "description": "ID of the Contract link whose Markdown content should be returned."},
    },
    "required": ["contract_link_id"],
}

INPUT_SCHEMA_UPDATE_CONTRACT_LINK = {
    "type": "object",
    "properties": {
        "contract_link_id": {"type": "string", "description": "ID of the Contract link to update. Only the parameters included are changed; omitted parameters are left unchanged."},
        "title": {"type": "string", "description": "Title of the Contract link."},
        "verification_method": _VERIFICATION_METHOD,
        "redirect_url": {"type": "string", "description": "URL the signer is redirected to after signing. Blank removes the redirect."},
        "thank_you_message": {"type": "string", "description": "Message shown to the signer after signing. Only shown when no redirect_url is set. Blank removes the message."},
        "cc_email_addresses": {"type": "array", "description": "Email addresses that receive a copy of each signed contract. Empty array clears the list.", "items": {"type": "string"}},
        "second_signer_user_email": {"type": "string", "description": "Email address of a user in your eSignatures.com account who counter-signs each contract. Blank removes the second signer."},
        "second_signer_auto_sign": {"type": "string", "description": "When 'yes', the second signer's signature is applied automatically. Only applies when a second signer is set.", "enum": ["yes", "no"]},
        "test": {"type": "string", "description": "When 'yes', contracts signed via this link are test contracts with no fees; adds DEMO stamp.", "enum": ["yes", "no"]},
    },
    "required": ["contract_link_id"],
}

INPUT_SCHEMA_UPDATE_CONTRACT_LINK_CONTENT = {
    "type": "object",
    "properties": {
        "contract_link_id": {"type": "string", "description": "ID of the Contract link whose content should be edited."},
        "dry_run": {
            "type": "string",
            "enum": ["yes", "no"],
            "description": "When 'yes', returns the content as it would appear after edits, without saving."
        },
        "edits": {
            "type": "array",
            "description": "List of Markdown edit operations applied to the Contract link content. Each edit finds existing content and replaces it with new Markdown.",
            "items": {
                "type": "object",
                "properties": {
                    "find_markdown": {"type": "string", "description": "Markdown content to find. By default this matches text literally, including line breaks, so all occurrences of the exact text you provide are replaced (e.g. every 'including weekends' becomes the replacement). As a special case, if the value is exactly a heading followed by a trailing newline (e.g. '## Payment Terms\n'), the match expands to that heading plus all content beneath it up to the next heading, replacing the whole section. Set to blank ('') to replace the entire content."},
                    "replace_with_markdown": {"type": "string", "description": "Markdown content to insert in place of the matched content. Leave blank to remove the matched content."},
                },
                "required": ["find_markdown", "replace_with_markdown"],
            },
        },
    },
    "required": ["contract_link_id", "edits"],
}

INPUT_SCHEMA_DELETE_CONTRACT_LINK = {
    "type": "object",
    "properties": {
        "contract_link_id": {"type": "string", "description": "ID of the Contract link to be deleted."},
    },
    "required": ["contract_link_id"],
}

INPUT_SCHEMA_LIST_CONTRACT_LINKS = {
    "type": "object",
    "properties": {},
}
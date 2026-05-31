from .input_schema_markdown import MARKDOWN_CONTENT_DESCRIPTION

INPUT_SCHEMA_QUERY_PLACEHOLDER_FIELDS = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract whose Placeholder field values should be returned."},
    },
    "required": ["contract_id"],
}

INPUT_SCHEMA_UPDATE_PLACEHOLDER_FIELDS = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract to update. The contract must be unsigned."},
        "placeholder_fields": {
            "type": "array",
            "description": "Placeholder fields to update on the contract. Only the fields included here are changed; omitted fields are left untouched. Each field can be replaced with plain text, Markdown content, or the full content of one of your templates.",
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
    },
    "required": ["contract_id", "placeholder_fields"],
}

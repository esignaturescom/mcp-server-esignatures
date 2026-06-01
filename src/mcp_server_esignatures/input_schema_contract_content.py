INPUT_SCHEMA_QUERY_CONTRACT_CONTENT = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract whose Markdown content should be returned."},
    },
    "required": ["contract_id"],
}

INPUT_SCHEMA_UPDATE_CONTRACT_CONTENT = {
    "type": "object",
    "properties": {
        "contract_id": {"type": "string", "description": "GUID of the contract whose content should be edited. The contract must be unsigned."},
        "edits": {
            "type": "array",
            "description": "List of Markdown edit operations applied to the contract content. Each edit finds existing content and replaces it with new Markdown.",
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
    "required": ["contract_id", "edits"],
}

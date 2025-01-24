from .input_schema_document_elements import INPUT_SCHEMA_DOCUMENT_ELEMENTS_ITEMS

INPUT_SCHEMA_CREATE_TEMPLATE = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Title for the new template; used for contracts based on this template."},
        "labels": {"type": "array", "description": "Assign labels for organizing templates and contracts; labels are inherited by contracts.", "items": {"type": "string"}},
        "document_elements": {
            "type": "array",
            "description": "Customize template content with headers, text, images. Owners can manually replace {{placeholder fields}} in the eSignatures contract editor, and signers can fill in Signer fields when signing the document. Use placeholders for signer names if needed, instead of Signer fields. Contract title auto-inserts as the first line.",
            "items": INPUT_SCHEMA_DOCUMENT_ELEMENTS_ITEMS
        }
    },
    "required": ["title", "document_elements"]
}

INPUT_SCHEMA_QUERY_TEMPLATE = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string", "description": "GUID of the template."},
    },
    "required": ["template_id"],
}

INPUT_SCHEMA_UPDATE_TEMPLATE = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "The new title of the template."},
        "labels": {"type": "array", "description": "List of labels to be assigned to the template.", "items": {"type": "string"}},
        "document_elements": {
            "type": "array",
            "description": "The content of the template like headers, text, and images for the document.",
            "items": INPUT_SCHEMA_DOCUMENT_ELEMENTS_ITEMS
        }
    }
}

INPUT_SCHEMA_DELETE_TEMPLATE = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string", "description": "GUID of the template to be deleted."},
    },
    "required": ["template_id"],
}

INPUT_SCHEMA_LIST_TEMPLATES = {
    "type": "object",
    "properties": {}
}

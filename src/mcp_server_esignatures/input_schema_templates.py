from .input_schema_markdown import MARKDOWN_CONTENT_DESCRIPTION

INPUT_SCHEMA_CREATE_TEMPLATE = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Title for the new template; used for contracts based on this template."},
        "labels": {"type": "array", "description": "Assign labels for organizing templates and contracts; labels are inherited by contracts.", "items": {"type": "string"}},
        "markdown": {
            "type": "string",
            "description": MARKDOWN_CONTENT_DESCRIPTION,
        },
    },
    "required": ["title", "markdown"],
}

INPUT_SCHEMA_QUERY_TEMPLATE = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string", "description": "GUID of the template."},
    },
    "required": ["template_id"],
}

INPUT_SCHEMA_QUERY_TEMPLATE_CONTENT = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string", "description": "GUID of the template whose Markdown content should be returned."},
    },
    "required": ["template_id"],
}

INPUT_SCHEMA_UPDATE_TEMPLATE = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string", "description": "GUID of the template to update."},
        "title": {"type": "string", "description": "The new title of the template."},
        "labels": {"type": "array", "description": "List of labels to be assigned to the template.", "items": {"type": "string"}},
    },
    "required": ["template_id"],
}

INPUT_SCHEMA_UPDATE_TEMPLATE_CONTENT = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string", "description": "GUID of the template whose content should be edited."},
        "edits": {
            "type": "array",
            "description": "List of Markdown edit operations applied to the template content. Each edit finds existing content and replaces it with new Markdown.",
            "items": {
                "type": "object",
                "properties": {
                    "find_markdown": {"type": "string", "description": "Markdown content to find and replace. Can be an exact snippet or a section heading (e.g. ## Payment Terms). When a heading is provided, the entire section is matched. Leave blank to replace the entire template content."},
                    "replace_with_markdown": {"type": "string", "description": "Markdown content to insert in place of the matched content. Leave blank to remove the matched content."},
                },
                "required": ["find_markdown", "replace_with_markdown"],
            },
        },
    },
    "required": ["template_id", "edits"],
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
    "properties": {},
}
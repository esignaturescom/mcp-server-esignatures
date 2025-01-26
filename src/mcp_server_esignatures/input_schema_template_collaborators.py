INPUT_SCHEMA_ADD_TEMPLATE_COLLABORATOR = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string"},
        "name": {"type": "string", "description": "Collaborator's name"},
        "email": {"type": "string", "description": "Collaborator's email; triggers an invitation email when provided"}
    },
    "required": ["template_id"]
}

INPUT_SCHEMA_REMOVE_TEMPLATE_COLLABORATOR = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string", "description": "Templates's GUID."},
        "template_collaborator_id": {"type": "string", "description": "Collaborator's GUID."}
    },
    "required": ["template_id", "template_collaborator_id"],
}

INPUT_SCHEMA_LIST_TEMPLATE_COLLABORATORS = {
    "type": "object",
    "properties": {
        "template_id": {"type": "string"}
    },
    "required": ["template_id"]
}

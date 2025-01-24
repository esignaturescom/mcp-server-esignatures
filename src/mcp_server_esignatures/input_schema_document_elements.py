INPUT_SCHEMA_DOCUMENT_ELEMENTS_ITEMS = {
    "type": "object",
    "oneOf": [
        {
            "properties": {
                "type": {
                    "type": "string",
                    "description": "Header lines. Do not add the title of the template/contract as the first line; it will already be included at the beginning of the contracts.",
                    "enum": ["text_header_one", "text_header_two", "text_header_three"]
                },
                "text": {"type": "string"},
                "text_alignment": {"type": "string", "enum": ["center", "right", "justified"], "default": "left"}
            },
            "required": ["type", "text"]
        },
        {
            "properties": {
                "type": {
                    "type": "string",
                    "description": "For paragraphs and non-list text content.",
                    "enum": ["text_normal"]
                },
                "text": {"type": "string"},
                "text_alignment": {"type": "string", "enum": ["center", "right", "justified"], "default": "left"},
                "text_styles": {
                    "type": "array",
                    "description": "An array defining text style ranges within the element. For Placeholder fields, ensure the moustache brackets around the placeholder also match the style. Example for '{{rate}} percent': [{offset:0, length:8, style:'bold'}]",
                    "items": {
                        "type": "object",
                        "properties": {
                            "offset": {"type": "integer", "description": "Start index of styled text (0-based)"},
                            "length": {"type": "integer", "description": "Number of characters in the styled range"},
                            "style": {"type": "string", "description": "Style to apply", "enum": ["bold", "italic", "underline"]}
                        }
                    }
                },
                "depth": {"type": "integer", "default": 0, "description":"Indentation level of text, defaults to 0."}
            },
            "required": ["type", "text"]
        },
        {
            "properties": {
                "type": {
                    "type": "string",
                    "description": "For list items. Use ordered_list_item for sequential/numbered lists, unordered_list_item for bullet points. Lists continue at the same indentation level until interrupted by another element type which is not a list or indented paragraph.",
                    "enum": ["ordered_list_item", "unordered_list_item"]
                },
                "text": {"type": "string"},
                "depth": {"type": "integer", "default": 0, "description":"Depth of list nesting, default 0. For ordered lists, numbering persists at the same or deeper indentation levels; paragraphs don't interrupt numbering."}
            },
            "required": ["type", "text"]
        },
        {
            "properties": {
                "type": {
                    "type": "string",
                    "description": "Signer fields allow input or selection by signers. Do not add any signer fields for collecting signatures, names, dates, company names or titles or anything similar at the end of documents. Radio buttons group automatically, do not insert any other elements (like text) between radio buttons that should be grouped together. Instead, place descriptive text before or after the complete radio button group.",
                    "enum": ["signer_field_text", "signer_field_text_area", "signer_field_date", "signer_field_dropdown", "signer_field_checkbox", "signer_field_radiobutton", "signer_field_file_upload"]
                },
                "text": {"type": "string"},
                "signer_field_assigned_to": {"type": "string", "description": "Specifies which signer(s) can interact with this field based on signing order. 'first_signer' means only the first signer to open and sign can fill the field; others with the same or later order cannot. The same rule applies for 'second_signer' and 'last_signer'. 'every_signer' shows the field to each signer, with separate values in the final PDF. Examples: 'Primary contact for property issues' (first signer) and 'My mobile number' (every signer).", "enum": ["first_signer", "second_signer", "last_signer", "every_signer"]},
                "signer_field_required": {"type": "string", "enum": ["yes", "no"]},
                "signer_field_dropdown_options": {"type": "string", "description": "Options for dropdown fields, separated by newline \n characters"},
                "signer_field_id": {"type": "string", "description": "Unique ID for the Signer field, used in Webhook notifications for value inclusion. If not specified, values are excluded from Webhook notifications and CSV exports."}
            },
            "required": ["type", "text", "signer_field_assigned_to"]
        },
        {
            "properties": {
                "type": {"type": "string", "enum": ["image"]},
                "image_base64": {"type": "string", "description": "The base64-encoded png or jpg image (max 0.5MB)."},
                "image_alignment": {"type": "string", "enum": ["center", "right"], "default": "left"},
                "image_height_rem": {"type": "number", "minimum": 2, "maximum": 38}
            },
            "required": ["type", "image_base64"]
        },
        {
            "properties": {
                "type": {"type": "string", "enum": ["table"]},
                "table_cells": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "styles": {"type": "array", "items": {"type": "string", "enum": ["bold", "italic"]}},
                                "alignment": {"type": "string", "enum": ["center", "right"], "default": "left"}
                            }
                        }
                    }
                }
            },
            "required": ["type", "table_cells"]
        },
        {
            "properties": {
                "type": {
                    "type": "string",
                    "description": "Nested template inclusion. Maximum depth: 1 level",
                    "enum": ["template"]
                },
                "template_id": {"type": "string", "description": "ID of the template to insert; Placeholder fields apply within this template too."}
            },
            "required": ["type", "template_id"]
        }
    ]
}

MARKDOWN_CONTENT_DESCRIPTION = """\
Document body in eSignatures.com Markdown. Use standard CommonMark for headers,
paragraphs, bold (**bold**), italic (*italic*), ordered/unordered lists,
tables, and images. Add Signer fields, line alignment, header counters, etc.
via the *extended syntax*: an optional JSON config in backticks appended to
the end of a markdown line.

Do NOT add Signer fields for the signature, signer name, signing date, or
signer company at the end of the document — those are inserted automatically.
Do NOT repeat the contract/template title as the first line — it is rendered
automatically.

Example:

  This agreement is between the rental provider/s and the renter/s.

  - The renter agrees to pay rent on the 1st of each month.
  - The provider agrees to maintain the property in good condition.

  ## Special conditions `{"header_counter": "yes"}`

  I agree to the above **terms and conditions**. `{"alignment": "center"}`

  Parent name `{"line_type": "text-input", "input_type": "only_first_signer", "input_required": "yes", "signer_field_id": "parent-name"}`

  Preferred device `{"line_type": "select-input", "input_type": "only_first_signer", "select_values": ["Desktop", "Tablet", "Mobile"]}`

  I accept the privacy policy `{"line_type": "checkbox", "input_type": "every_signer", "input_required": "yes"}`

  | Header 1 | Header 2 |
  | -------- | -------- |
  | cell 1   | cell 2   |

Extended-syntax config keys (all optional unless noted):

  - alignment: line alignment. Values: `center`, `right`, `justify`.
    Default `left`. Applicable to headers and paragraphs.
  - header_counter: `yes` prepends an auto-incremented counter to the header
    text. Applicable to headers.
  - line_type: turns the line into a Signer field. Required when adding a
    Signer field. Values: `text-input`, `text-area`, `date`, `select-input`,
    `checkbox`, `radiobutton`, `file-upload`.
  - input_type: which signer(s) may fill the Signer field. Required for
    Signer fields. Values: `only_first_signer`, `only_second_signer`,
    `only_last_signer`, `every_signer`. Use `only_first_signer` for a field
    that only the first signer in signing_order fills; `every_signer` shows
    the field to each signer with separate values recorded in the final PDF.
  - input_required: `yes` or `no`. Whether the signer must fill the field.
    Applicable to all Signer fields.
  - default_value: pre-filled value shown when the signer opens the document.
    Applicable to `text-input`, `select-input`, `checkbox` (use `1` to
    pre-tick), `radiobutton`. Use `YYYY-MM-DD` for dates.
  - placeholder_text: hint text shown in the field background guiding the
    signer on what to enter. Applicable to `text-input`.
  - select_values: list of dropdown options, e.g.
    ["Desktop", "Tablet", "Mobile"]. Applicable to `select-input`.
  - masked: `yes` or `no`. When `yes`, the value the signer enters is hidden
    from other signers and masked in the final PDF. Applicable to
    `text-input`.
  - signer_field_id: unique ID for the field. Surfaced in webhook payloads
    and used by the contract `signer_fields` API parameter to pre-fill the
    value. Applicable to all Signer fields.

Radio buttons within a single question group automatically; do not insert
other elements (text, headers) between radiobutton lines that belong to the
same group — place descriptive text before or after the full group instead.
"""
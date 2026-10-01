MARKDOWN_CONTENT_DESCRIPTION = r"""# Extended markdown syntax

## 1. Headings
- Standard Markdown headings: `#`, `##`, `###` and so on.
- `header_counter` prepends an auto-incrementing number to a heading. Append `{"header_counter": "yes"}` to the heading line to enable it.
- Do not use `header_counter` when the heading numbers are cross-referenced within the document (e.g. "as set out in clause 3.2"); keep the literal numbers in the heading text instead.

## 2. Indentation
- Use 4 spaces per level of nesting.
- Do not indent top-level paragraphs, top-level lists, or text under headings unless genuinely nested (continuations under a list item).

## 3. Ordered/numbered and unordered Lists
- Ensure all list and subsection numbering is consistent and sequential.
- Enumerated items (not headers) are standard Markdown lists: `-` for unordered, `1.` for ordered.
- Indent the lists as needed by 4 spaces per level, for both ordered and unordered lists. (e.g. indent the `1.1.1` -> `1. First line\n    1. Sub indented line\n        1. Sub sub indented line`)
- When a header line needs to be numbered never use a list item for that line.
- If a line must keep its own literal label or number (e.g. `(a)`, `5.2.`) instead of auto-numbering, write it as a paragraph with the label at the start, indented 4 spaces per nesting level. Do not combine a bullet marker with a literal label.

### How to ensure correct numbering
- Use `1.` for enumerated items as the digits are ignored - it doesn't matter if it's `1. ` or `2. `.
- Ordered list numbering continues **only** with:
    - a list item at the same level
    - a nested list item
    - a nested paragraph (indented with 4 spaces)
      Any other `line_type` or break in nesting restarts numbering from 1.

## 4. Tables
- Valid Markdown tables have a header row, a `---` separator row, and aligned pipes.
- Every table row must start with the pipe character `|`
- Tables are for displaying data. Do not place Signer fields inside table cells; present that content as headings/paragraphs (or label + field lines) instead.

## 5. Placeholder fields
- Placeholder fields are for values the **contract owner** provides during sending. They exist so the contract owner can reuse one template across many contracts, so anything the contract owner decides that changes from one contract to the next becomes a placeholder field.
- Mustache notated `{{field_name}}` are for values the **contract owner** customizes before sending - e.g. company/party names, fees, rates, dates set by the owner, and similar deal terms.
- Snake_case is preferred, e.g. `{{company_name}}`, `{{service_start_date}}`, `{{total_fee}}`.
- Reuse the same key when the very same information needs to be filled in at multiple spots in the document.

## 6. Extended Markdown syntax (follow exactly)
The extended syntax is a JSON object in backticks appended to the very end of a Markdown line.
Important: This JSON object must only appear at the very end of the line. It must never be placed anywhere else within a line.

This is a centered heading `{"alignment": "center", "header_counter": "yes"}`
Parent name `{"line_type": "text-input", "input_type": "only_first_signer", "input_required": "yes", "signer_field_id": "parent_name"}`
Preferred device `{"line_type": "select-input", "input_type": "only_first_signer", "select_values": "Desktop\nTablet\nMobile", "signer_field_id": "preferred_device"}`
I accept the privacy policy `{"line_type": "checkbox", "input_type": "every_signer", "input_required": "yes", "signer_field_id": "privacy_policy_accepted"}`

Parameter reference:

| Parameter | Description                                                                                                                                            | Used with |
| --- |--------------------------------------------------------------------------------------------------------------------------------------------------------| --- |
| line_type | Type of Signer field. Required for Signer fields. Options: `text-input`, `text-area`, `date`, `select-input`, `checkbox`, `radiobutton`, `file-upload` | Signer fields |
| input_type | Which signer(s) fill the field. Options: `only_first_signer`, `only_second_signer`, `only_last_signer`, `every_signer` | All Signer fields |
| input_required | Whether the field is mandatory. Options: `yes`, `no` | All Signer fields |
| signer_field_id | Unique snake_case ID, used in webhooks, integrations, and the `signer_fields` API parameter | All Signer fields |
| default_value | Pre-filled value when the signer opens the document | text-input, select-input, checkbox, radiobutton |
| placeholder_text | Hint text shown inside the field guiding the signer | text-input |
| masked | Hides the value from other signers and masks it in the final PDF. Options: `yes`, `no` | text-input |
| select_values | String containing dropdown options separated by newlines `\n`, e.g. `Desktop\nTablet\nMobile`                                                          | select-input |
| alignment | `center`, `right`, or `justify` (default is left) | Headers and paragraphs |
| header_counter | Prepends an auto-incrementing number to the header. Value: `yes` | Headers |

### Extended markdown rules
- Only append the JSON config when defining a Signer field or special formatting (alignment / header_counter). Plain content lines get no config.
- Only a single JSON config can be used in a markdown line.
- The label text always goes before the JSON config on the same line.
- Every config must be valid JSON: double-quoted keys and string values, no trailing commas, only the keys listed above.
- The JSON config in backticks must be the very last thing on the line, with nothing after the closing backtick — not a space, punctuation, or any other character. Any trailing character breaks the JSON syntax.

## 7. Extended Markdown syntax for Signer fields
- Signer fields are for values the **signers** provide during signing.
- The Signer field markdown line must have the label at the beginning, and the JSON syntax at the end of the line.
- A markdown line can only have a single Signer field. Do not include multiple Signer fields in a single markdown line.
- Choose `line_type` by the data being collected: short text → `text-input`; multi-line answers, descriptions, comments → `text-area`; dates → `date`; a single confirmation → `checkbox`; mutually exclusive options → `radiobutton` (or `select-input` for a dropdown of values); document attachments → `file-upload`.
- Do not use plain underscores (`_____`) or manual lines anywhere; every fill-in becomes a Signer field or a Placeholder field.
- When a signer must confirm, acknowledge, or initial a specific section, convert it to a mandatory checkbox with text similar to: "I hereby acknowledge that I've read and understood the above content."
- Default `input_type` to `every_signer` unless context clearly indicates a specific party (e.g. fields in a section addressed to one party → `only_first_signer` / `only_second_signer`; when party order is unclear for the receiving party, prefer `every_signer`).
- `input_required`: `yes` for fields necessary to the agreement; `no` for clearly optional ones.
- `signer_field_id`: a stable, unique snake_case identifier derived from the label (e.g. `client_full_name`, `start_date`). Never duplicate IDs.
- Use `masked`:`yes` for confidential values (e.g. ID numbers, bank details).
- Use `placeholder_text` to hint about the expected value.
- A question with a fixed set of answers (Yes/No, Agree/Disagree, True/False, or any short closed list) should either be a radiobutton list or a select-input (dropdown) — never a text-input with the options written into the label.

### Signer fields vs Placeholder fields
- Rule of thumb: if the value defines the deal and must be known before the contract is sent (including the name of the signer), it is a `{{placeholder}}`; if it is personal to a signer and provided at signing time, it is a Signer field.

### Radiobuttons
- Group radiobuttons by keeping all options on directly consecutive Markdown lines. Never insert any blank lines, paragraphs, headings, or other content between radiobutton lines in the same group.
- Output one line per radiobutton option.
- Use the `"default_value":"yes"` to set that radiobutton line selected by default, within its radiobutton group - only when needed.
- Set the `input_required` and other fields for the first radiobutton line only (all others in the same group will automatically have the same parameters applied).
- If added, the `signer_field_id` must be unique for each radiobutton line. That helps with identifying which radiobutton was chosen in Webhooks and other data pipelines.
- In some cases Yes/No options are better to be represented with radiobuttons, in some cases they are better with a single Dropdown. Make a consistent decision on that for each individual document.

### Worked examples

INPUT (form blank in body):
This Agreement is made between ______________ ("Provider") and ______________ ("Customer").
OUTPUT:
This Agreement is made between {{provider_name}} ("Provider") and {{customer_name}} ("Customer").

INPUT (signer-supplied detail):
Emergency contact phone: _________________
BAD OUTPUT label is not tied to the field:
Emergency contact phone
`{"line_type":"text-input","input_type":"only_first_signer","input_required":"yes","signer_field_id":"emergency_contact_phone"}`

INPUT (signer-supplied detail):
Emergency contact phone: _________________
OUTPUT:
Emergency contact phone`{"line_type":"text-input","input_type":"only_first_signer","input_required":"yes","signer_field_id":"emergency_contact_phone"}`

INPUT (signer-supplied multi line):
Details:\n_________________\n_________________
OUTPUT:
Details`{"line_type":"text-area","input_type":"every_signer","input_required":"no","signer_field_id":"details"}`

INPUT (acknowledgment/initials line):
Initials: ____ (Section 8: Limitation of Liability)
OUTPUT:
I hereby acknowledge that I've read and understood the above content.`{"line_type":"checkbox","input_type":"every_signer","input_required":"yes","signer_field_id":"limitation_of_liability_acknowledged"}`

INPUT (choice):
Preferred contact method:  ☐ Email   ☐ SMS   ☐ Mail
OUTPUT with select-input:
Preferred contact method`{"line_type":"select-input","input_type":"every_signer","select_values":"Email\nSMS\nMail","signer_field_id":"preferred_contact_method"}`

INPUT (choice):
Preferred contact method:  ☐ Email   ☐ SMS   ☐ Mail
OUTPUT with radiobutton:
Preferred contact method
Email`{"line_type":"radiobutton","input_type":"every_signer","signer_field_id":"preferred_contact_method_email"}`
SMS`{"line_type":"radiobutton","input_type":"every_signer","signer_field_id":"preferred_contact_method_sms"}`
Mail`{"line_type":"radiobutton","input_type":"every_signer","signer_field_id":"preferred_contact_method_mail"}`

INPUT (choice):
Preferred contact method:  ☐ Email   ☐ SMS   ☐ Mail
BAD OUTPUT extra lines break the radiobutton grouping:
Preferred contact method
Email`{"line_type":"radiobutton","input_type":"every_signer","signer_field_id":"preferred_contact_method_email"}`

SMS`{"line_type":"radiobutton","input_type":"every_signer","signer_field_id":"preferred_contact_method_sms"}`

Mail`{"line_type":"radiobutton","input_type":"every_signer","signer_field_id":"preferred_contact_method_mail"}`


INPUT (signature block at the end):
Signature: ______________    Date: ___________
Printed name: ______________
OUTPUT: nothing — omit the block; the platform renders the signature section.
"""
# mcp-server-esignatures MCP server

MCP server for eSignatures (https://esignatures.com)

## Tools


| Tool                             | Category      | Description                                      |
|----------------------------------|---------------|--------------------------------------------------|
| `create_contract`                | Contracts     | Draft for review or send contract                |
| `query_contract`                 | Contracts     | Retrieve contract info                           |
| `withdraw_contract`              | Contracts     | Withdraw an unsigned contract                    |
| `delete_contract`                | Contracts     | Delete a draft or test contract                  |
| `list_recent_contracts`          | Contracts     | List the recent contracts                        |
|                                  |               |                                                  |
| `add_contract_signer`            | Signers       | Add a signer to an existing contract             |
| `update_contract_signer`         | Signers       | Update an existing signer's contact details      |
| `resend_contract_signer_request` | Signers       | Send or resend the sign request to a signer      |
| `delete_contract_signer`         | Signers       | Remove a signer from a contract                  |
|                                  |               |                                                  |
| `create_template`                | Templates     | Create a new contract template (Markdown body)   |
| `update_template`                | Templates     | Update an existing template's title/labels       |
| `update_template_content`        | Templates     | Edit a template's Markdown body via find/replace |
| `query_template`                 | Templates     | Retrieve template metadata                       |
| `query_template_content`         | Templates     | Retrieve a template's Markdown body              |
| `delete_template`                | Templates     | Delete a template                                |
| `list_templates`                 | Templates     | List all your templates                          |
|                                  |               |                                                  |
| `add_template_collaborator`      | Collaborators | Invite someone to edit a template                |
| `remove_template_collaborator`   | Collaborators | Revoke template editing rights                   |
| `list_template_collaborators`    | Collaborators | View who can edit a template                     |


## Examples

#### Creating a draft contract

`Create a draft NDA for a publisher, ready for me to review and send. Signer: John Doe, ACME Corp, john@acme.com.`

#### Sending a contract from a template

`Send an NDA based on my template to John Doe from ACME Corp at john@acme.com. Set the term to 2 years.`

#### Creating a new contract

`Create a contractor agreement for a graphic designer, including payment terms of net 14 days. Prepare it as a draft for review. Signer: John Doe, ACME Corp, john@acme.com.`

#### Adding a signer to a contract
`Add Jane Smith from ACME Corp (jane@acme.com) as a signer on the NDA contract, then send her the signature request.`

#### Editing an existing template

`Update my NDA template to include a 12-month non-solicitation clause.`

#### Reviewing templates

`Review my templates and suggest improvements. Do not apply any changes until I approve them one by one.`

#### Finding the right template

`Find the best template for onboarding a contractor and prepare a draft contract for John Doe.`

#### Managing contracts

`Show me the recent contracts that are waiting for signatures.`

#### Updating signer details

`Update the signer email on the NDA contract for John Doe to john.doe@acme.com.`

#### Inviting template collaborators

`Invite John Doe to edit the NDA template. His email is john@acme.com.`


## Install

### Create an eSignatures account

Create an eSignatures account at https://esignatures.com for free, to test the Agent AI by creating templates and sending test contracts.

### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

##### Development/Unpublished Servers Configuration
```
"mcpServers": {
  "mcp-server-esignatures": {
    "command": "uv",
    "env": {
      "ESIGNATURES_SECRET_TOKEN": "your-esignatures-api-secret-token"
    },
    "args": [
      "--directory",
      "/your-local-directories/mcp-server-esignatures",
      "run",
      "mcp-server-esignatures"
    ]
  }
}
```

#### Published Servers Configuration
```
"mcpServers": {
  "mcp-server-esignatures": {
    "command": "uvx",
    "args": [
      "mcp-server-esignatures"
    ],
    "env": {
      "ESIGNATURES_SECRET_TOKEN": "your-esignatures-api-secret-token"
    }
  }
}
```

### Authentication

To use this server, you need to set the `ESIGNATURES_SECRET_TOKEN` environment variable with your eSignatures API secret token.

## eSignatures API Documentation

For a detailed guide on API endpoints, parameters, and responses, see [eSignatures API](https://esignatures.com/docs/api).

## eSignatures Support

For support, please navigate to [Support](https://esignatures.com/support) or contact [support@esignatures.com](mailto:support@esignatures.com).

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and make changes as you see fit. Here are some guidelines:

- **Bug Reports**: Please open an issue to report any bugs you encounter.
- **Feature Requests**: Suggest new features by opening an issue with the "enhancement" label.
- **Pull Requests**: Ensure your pull request follows the existing code style.
- **Documentation**: Help improve or translate documentation. Any form of documentation enhancement is appreciated.

For major changes, please open an issue first to discuss what you would like to change. We're looking forward to your contributions!
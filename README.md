[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/esignaturescom-mcp-server-esignatures-badge.png)](https://mseep.ai/app/esignaturescom-mcp-server-esignatures)

# mcp-server-esignatures MCP server

MCP server for eSignatures (https://esignatures.com)

<a href="https://glama.ai/mcp/servers/0ev38n83u4"><img width="380" height="200" src="https://glama.ai/mcp/servers/0ev38n83u4/badge" alt="Server for eSignatures MCP server" /></a>

## Tools


| Tool                           | Category      | Description                        |
|--------------------------------|---------------|------------------------------------|
| `create_contract`              | Contracts     | Draft for review or send contract  |
| `query_contract`               | Contracts     | Retrieve contract info             |
| `withdraw_contract`            | Contracts     | Withdraw an unsigned contract      |
| `delete_contract`              | Contracts     | Delete a draft or test contract    |
| `list_recent_contracts`        | Contracts     | List the recent contracts          |
|                                |               |                                    |
| `create_template`              | Templates     | Create a new contract template     |
| `update_template`              | Templates     | Update an existing template        |
| `query_template`               | Templates     | Retrieve template content and info |
| `delete_template`              | Templates     | Delete a template                  |
| `list_templates`               | Templates     | List all your templates            |
|                                |               |                                    |
| `add_template_collaborator`    | Collaborators | Invite someone to edit a template  |
| `remove_template_collaborator` | Collaborators | Revoke template editing rights     |
| `list_template_collaborators`  | Collaborators | View who can edit a template       |


## Examples

#### Creating a Draft Contract

`Generate a draft NDA contract for a publisher, which I can review and send. Signer: John Doe, ACME Corp, john@acme.com`

#### Sending a Contract

`Send an NDA based on my template to John Doe, ACME Corp, john@acme.com. Set the term to 2 years.`

#### Updating templates

`Review my templates for legal compliance, and ask me about updating each one individually`

#### Inviting template collaborators

`Invite John Doe to edit the NDA template, email: john@acme.com`


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

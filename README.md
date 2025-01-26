# mcp-server-esignatures MCP server
[![smithery badge](https://smithery.ai/badge/@esignaturescom/mcp-server-esignatures)](https://smithery.ai/server/@esignaturescom/mcp-server-esignatures)

MCP server for eSignatures (https://esignatures.com)

## Tools

These tools are designed to make managing contracts and templates straightforward, ensuring that everything from creation to finalization is smooth and customizable to your needs.

### For Contract Management:

- **Create Contract**: Create a draft contract for review, or send it instantly. You can choose templates or dynamic content, customize emails, set expiration dates, and more.
- **Query Contract**: Look up any contract by its unique ID to check its status or details.
- **Withdraw Contract**: If you've sent out a contract but haven't received signatures yet, you can pull it back with this tool.
- **Delete Contract**: Remove a contract from the system when it's no longer needed.
- **List Recent Contracts**: Get an overview of the recent contracts you've created or managed.

### For Template Management:

- **Create Template**: Create reusable contract templates with Placeholder fields for dynamic content. This makes setting up new contracts much faster.
- **Query Template**: Fetch details of any template you've made, handy for updates or reference.
- **Update Template**: Modify an existing template if you need to change future contracts based on it.
- **Delete Template**: Delete templates that are no longer in use or relevant.
- **List Templates**: List the templates you have in eSignatures.
- **Add/Remove/List Collaborators**: Invite persons to edit a template.

## Examples of Usage

#### Example 1: Creating a Draft Contract

Command: `Generate a draft contract so I can review and send it, using the NDA template, signer: John Doe, ACME Corp, john@acme.com`

#### Example 2: Sending a Contract

Command: `Send an NDA based on my template to John Doe, ACME Corp, john@acme.com`

#### Example 3: Updating templates

Command: `Review my templates for legal compliance, and ask me about updating each one individually`

#### Example 4: Inviting template collaborators

Command: `Invite John Doe to edit the NDA template, email: john@acme.com`


## Install

### Installing via Smithery

To install mcp-server-esignatures for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@esignaturescom/mcp-server-esignatures):

```bash
npx -y @smithery/cli install @esignaturescom/mcp-server-esignatures --client claude
```

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

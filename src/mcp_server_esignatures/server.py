from os import getenv

import asyncio
import httpx

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from .input_schema_contracts import INPUT_SCHEMA_CREATE_CONTRACT, INPUT_SCHEMA_QUERY_CONTRACT, INPUT_SCHEMA_WITHDRAW_CONTRACT, INPUT_SCHEMA_DELETE_CONTRACT, INPUT_SCHEMA_LIST_RECENT_CONTRACTS
from .input_schema_templates import (
    INPUT_SCHEMA_CREATE_TEMPLATE,
    INPUT_SCHEMA_QUERY_TEMPLATE,
    INPUT_SCHEMA_QUERY_TEMPLATE_CONTENT,
    INPUT_SCHEMA_UPDATE_TEMPLATE,
    INPUT_SCHEMA_UPDATE_TEMPLATE_CONTENT,
    INPUT_SCHEMA_DELETE_TEMPLATE,
    INPUT_SCHEMA_LIST_TEMPLATES,
)
from .input_schema_template_collaborators import INPUT_SCHEMA_ADD_TEMPLATE_COLLABORATOR, INPUT_SCHEMA_REMOVE_TEMPLATE_COLLABORATOR, INPUT_SCHEMA_LIST_TEMPLATE_COLLABORATORS

ESIGNATURES_SECRET_TOKEN = getenv("ESIGNATURES_SECRET_TOKEN")
ESIGNATURES_API_BASE = "https://esignatures.com"

async def serve() -> Server:
    secret_token = ESIGNATURES_SECRET_TOKEN
    server = Server("mcp-server-esignatures")
    httpxClient = httpx.AsyncClient(base_url=ESIGNATURES_API_BASE)

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="create_contract",
                description="Creates a new contract, either from a template (via template_id) or from ad-hoc content (via the markdown parameter, with no template needed). Exactly one of template_id or markdown must be provided. The contract can be a draft which the user can customize/send, or the contract can be sent instantly. So called 'signature fields' like Name/Date/signature-line must be left out, they are all handled automatically. Contract owners can customize template content by replacing {{placeholder fields}} inside the content (via placeholder_fields), and the signers can fill in Signer fields when they sign the contract.",
                inputSchema=INPUT_SCHEMA_CREATE_CONTRACT
            ),
            types.Tool(
                name="query_contract",
                description="Responds with the contract details, contract_id, status, final PDF url if present, title, labels, metadata, expiry time if present, and signer details with all signer events (signer events are included only for recent contracts, with rate limiting).",
                inputSchema=INPUT_SCHEMA_QUERY_CONTRACT
            ),
            types.Tool(
                name="withdraw_contract",
                description="Withdraws a sent contract.",
                inputSchema=INPUT_SCHEMA_WITHDRAW_CONTRACT
            ),
            types.Tool(
                name="delete_contract",
                description="Deletes a contract. The contract can only be deleted if it's a test contract or a draft contract.",
                inputSchema=INPUT_SCHEMA_DELETE_CONTRACT
            ),
            types.Tool(
                name="list_recent_contracts",
                description="Returns the the details of the latest 100 contracts.",
                inputSchema=INPUT_SCHEMA_LIST_RECENT_CONTRACTS
            ),

            types.Tool(
                name="create_template",
                description="Creates a reusable contract template for contracts to be based on. The body is provided as Markdown; Signer fields, alignment, and header counters are expressed with the extended-syntax JSON config in backticks at the end of a line.",
                inputSchema=INPUT_SCHEMA_CREATE_TEMPLATE
            ),
            types.Tool(
                name="update_template",
                description="Updates a template's title and/or labels. Use update_template_content to edit the template body.",
                inputSchema=INPUT_SCHEMA_UPDATE_TEMPLATE
            ),
            types.Tool(
                name="update_template_content",
                description="Edits a template's Markdown content by applying an ordered list of find/replace operations. Each `edits` entry replaces the first match of `find_markdown` (a Markdown snippet or just a header line like '## Section') with `replace_with_markdown`; set `replace_with_markdown` to an empty string to delete the matched content.",
                inputSchema=INPUT_SCHEMA_UPDATE_TEMPLATE_CONTENT
            ),
            types.Tool(
                name="query_template",
                description="Responds with the template metadata: template_id, title, labels, created_at, list of Placeholder fields and Signer field IDs in the template. Use query_template_content to fetch the Markdown body.",
                inputSchema=INPUT_SCHEMA_QUERY_TEMPLATE
            ),
            types.Tool(
                name="query_template_content",
                description="Returns the Markdown content (body) of a template.",
                inputSchema=INPUT_SCHEMA_QUERY_TEMPLATE_CONTENT
            ),
            types.Tool(
                name="delete_template",
                description="Deletes a contract template.",
                inputSchema=INPUT_SCHEMA_DELETE_TEMPLATE
            ),
            types.Tool(
                name="list_templates",
                description="Lists the templates.",
                inputSchema=INPUT_SCHEMA_LIST_TEMPLATES
            ),

            types.Tool(
                name="add_template_collaborator",
                description="Creates a HTTPS link for editing a contract template; sends an invitation email if an email is provided..",
                inputSchema=INPUT_SCHEMA_ADD_TEMPLATE_COLLABORATOR
            ),
            types.Tool(
                name="remove_template_collaborator",
                description="Removes the template collaborator",
                inputSchema=INPUT_SCHEMA_REMOVE_TEMPLATE_COLLABORATOR
            ),
            types.Tool(
                name="list_template_collaborators",
                description="Returns the list of template collaborators, including their GUID, name, email, and the HTTPS link for editing the template",
                inputSchema=INPUT_SCHEMA_LIST_TEMPLATE_COLLABORATORS
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "create_contract":
            response = await httpxClient.post(f"/api/contracts?token={secret_token}&source=mcpserver", json=arguments)
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "query_contract":
            response = await httpxClient.get(f"/api/contracts/{arguments.get('contract_id')}?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "withdraw_contract":
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/withdraw?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "delete_contract":
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/delete?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "list_recent_contracts":
            response = await httpxClient.get(f"/api/contracts/recent?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]

        if name == "create_template":
            response = await httpxClient.post(f"/api/templates?token={secret_token}", json=arguments)
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "query_template":
            response = await httpxClient.get(f"/api/templates/{arguments.get('template_id')}?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "query_template_content":
            response = await httpxClient.get(f"/api/templates/{arguments.get('template_id')}/content?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "update_template":
            payload = {k: v for k, v in arguments.items() if k != "template_id"}
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}?token={secret_token}", json=payload)
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "update_template_content":
            payload = {k: v for k, v in arguments.items() if k != "template_id"}
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}/content?token={secret_token}", json=payload)
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "delete_template":
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}/delete?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "list_templates":
            response = await httpxClient.get(f"/api/templates?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]

        if name == "add_template_collaborator":
            payload = {k: v for k, v in arguments.items() if k != "template_id"}
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}/collaborators?token={secret_token}", json=payload)
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "remove_template_collaborator":
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}/collaborators/{arguments.get('template_collaborator_id')}/remove?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "list_template_collaborators":
            response = await httpxClient.get(f"/api/templates/{arguments.get('template_id')}/collaborators?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]

        raise ValueError(f"Unknown tool: {name}")

    return server

def main():
    async def _run():
        # Run the server using stdin/stdout streams
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            server = await serve()
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-server-esignatures",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(_run())
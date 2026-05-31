from importlib.metadata import version
from os import getenv

import asyncio
import httpx

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from .input_schema_contracts import INPUT_SCHEMA_CREATE_CONTRACT, INPUT_SCHEMA_QUERY_CONTRACT, INPUT_SCHEMA_WITHDRAW_CONTRACT, INPUT_SCHEMA_DELETE_CONTRACT, INPUT_SCHEMA_LIST_RECENT_CONTRACTS
from .input_schema_signers import (INPUT_SCHEMA_ADD_CONTRACT_SIGNER, INPUT_SCHEMA_UPDATE_CONTRACT_SIGNER, INPUT_SCHEMA_RESEND_CONTRACT_SIGNER_REQUEST, INPUT_SCHEMA_DELETE_CONTRACT_SIGNER)
from .input_schema_templates import (INPUT_SCHEMA_CREATE_TEMPLATE, INPUT_SCHEMA_QUERY_TEMPLATE, INPUT_SCHEMA_QUERY_TEMPLATE_CONTENT, INPUT_SCHEMA_UPDATE_TEMPLATE, INPUT_SCHEMA_UPDATE_TEMPLATE_CONTENT, INPUT_SCHEMA_DELETE_TEMPLATE, INPUT_SCHEMA_LIST_TEMPLATES)
from .input_schema_template_collaborators import INPUT_SCHEMA_ADD_TEMPLATE_COLLABORATOR, INPUT_SCHEMA_REMOVE_TEMPLATE_COLLABORATOR, INPUT_SCHEMA_LIST_TEMPLATE_COLLABORATORS

ESIGNATURES_SECRET_TOKEN = getenv("ESIGNATURES_SECRET_TOKEN")
ESIGNATURES_API_BASE = "https://esignatures.com"
SERVER_VERSION = version("mcp-server-esignatures")

async def serve() -> Server:
    secret_token = ESIGNATURES_SECRET_TOKEN
    if not secret_token: raise RuntimeError("ESIGNATURES_SECRET_TOKEN is not set. Set it to your eSignatures API secret token before starting the server.")
    server = Server("mcp-server-esignatures")
    httpxClient = httpx.AsyncClient(base_url=ESIGNATURES_API_BASE, auth=httpx.BasicAuth(secret_token or "", ""))

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
                description="Returns the details of the latest 100 contracts.",
                inputSchema=INPUT_SCHEMA_LIST_RECENT_CONTRACTS
            ),

            types.Tool(
                name="add_contract_signer",
                description="Adds a signer to an existing contract. Note: adding a signer does NOT automatically send the contract to them; use resend_contract_signer_request to send it.",
                inputSchema=INPUT_SCHEMA_ADD_CONTRACT_SIGNER
            ),
            types.Tool(
                name="update_contract_signer",
                description="Updates the contact details of an existing signer on a contract. Note: the contract is NOT automatically re-sent when the signer is updated.",
                inputSchema=INPUT_SCHEMA_UPDATE_CONTRACT_SIGNER
            ),
            types.Tool(
                name="resend_contract_signer_request",
                description="Sends (or resends) the signature request to a specific signer on a contract.",
                inputSchema=INPUT_SCHEMA_RESEND_CONTRACT_SIGNER_REQUEST
            ),
            types.Tool(
                name="delete_contract_signer",
                description="Removes a signer from a contract.",
                inputSchema=INPUT_SCHEMA_DELETE_CONTRACT_SIGNER
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
                description="Creates a HTTPS link for editing a contract template; sends an invitation email if an email is provided.",
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
        arguments = arguments or {}

        if name == "create_contract":
            response = await httpxClient.post("/api/contracts?contract_source=mcpserver", json=arguments)
        elif name == "query_contract":
            response = await httpxClient.get(f"/api/contracts/{arguments.get('contract_id')}")
        elif name == "withdraw_contract":
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/withdraw")
        elif name == "delete_contract":
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/delete")
        elif name == "list_recent_contracts":
            response = await httpxClient.get("/api/contracts/recent")

        elif name == "add_contract_signer":
            payload = {k: v for k, v in arguments.items() if k != "contract_id"}
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/signers", json=payload)
        elif name == "update_contract_signer":
            payload = {k: v for k, v in arguments.items() if k not in ("contract_id", "signer_id")}
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/signers/{arguments.get('signer_id')}", json=payload)
        elif name == "resend_contract_signer_request":
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/signers/{arguments.get('signer_id')}/send_contract")
        elif name == "delete_contract_signer":
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/signers/{arguments.get('signer_id')}/delete")

        elif name == "create_template":
            response = await httpxClient.post("/api/templates", json=arguments)
        elif name == "query_template":
            response = await httpxClient.get(f"/api/templates/{arguments.get('template_id')}")
        elif name == "query_template_content":
            response = await httpxClient.get(f"/api/templates/{arguments.get('template_id')}/content")
        elif name == "update_template":
            payload = {k: v for k, v in arguments.items() if k != "template_id"}
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}", json=payload)
        elif name == "update_template_content":
            payload = {k: v for k, v in arguments.items() if k != "template_id"}
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}/content", json=payload)
        elif name == "delete_template":
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}/delete")
        elif name == "list_templates":
            response = await httpxClient.get("/api/templates")

        elif name == "add_template_collaborator":
            payload = {k: v for k, v in arguments.items() if k != "template_id"}
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}/collaborators", json=payload)
        elif name == "remove_template_collaborator":
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}/collaborators/{arguments.get('template_collaborator_id')}/remove")
        elif name == "list_template_collaborators":
            response = await httpxClient.get(f"/api/templates/{arguments.get('template_id')}/collaborators")

        else:
            raise ValueError(f"Unknown tool: {name}")

        try:
            body = response.json()
        except ValueError:
            body = response.text

        return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {body}")]

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
                    server_version=SERVER_VERSION,
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(_run())
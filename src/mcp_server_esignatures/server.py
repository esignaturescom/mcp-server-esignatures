from importlib.metadata import version
from os import getenv

import asyncio
import httpx

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from .input_schema_contracts import INPUT_SCHEMA_CREATE_CONTRACT, INPUT_SCHEMA_QUERY_CONTRACT, INPUT_SCHEMA_SEND_DRAFT_CONTRACT, INPUT_SCHEMA_WITHDRAW_CONTRACT, INPUT_SCHEMA_DELETE_CONTRACT, INPUT_SCHEMA_LIST_RECENT_CONTRACTS
from .input_schema_signers import (INPUT_SCHEMA_ADD_CONTRACT_SIGNER, INPUT_SCHEMA_UPDATE_CONTRACT_SIGNER, INPUT_SCHEMA_RESEND_CONTRACT_SIGNER_REQUEST, INPUT_SCHEMA_DELETE_CONTRACT_SIGNER)
from .input_schema_placeholder_fields import (INPUT_SCHEMA_QUERY_PLACEHOLDER_FIELDS, INPUT_SCHEMA_UPDATE_PLACEHOLDER_FIELDS)
from .input_schema_contract_content import (INPUT_SCHEMA_QUERY_CONTRACT_CONTENT, INPUT_SCHEMA_UPDATE_CONTRACT_CONTENT)
from .input_schema_templates import (INPUT_SCHEMA_CREATE_TEMPLATE, INPUT_SCHEMA_QUERY_TEMPLATE, INPUT_SCHEMA_QUERY_TEMPLATE_CONTENT, INPUT_SCHEMA_UPDATE_TEMPLATE, INPUT_SCHEMA_UPDATE_TEMPLATE_CONTENT, INPUT_SCHEMA_DELETE_TEMPLATE, INPUT_SCHEMA_LIST_TEMPLATES)
from .input_schema_template_collaborators import INPUT_SCHEMA_ADD_TEMPLATE_COLLABORATOR, INPUT_SCHEMA_REMOVE_TEMPLATE_COLLABORATOR, INPUT_SCHEMA_LIST_TEMPLATE_COLLABORATORS
from .input_schema_contract_links import (INPUT_SCHEMA_CREATE_CONTRACT_LINK, INPUT_SCHEMA_QUERY_CONTRACT_LINK, INPUT_SCHEMA_QUERY_CONTRACT_LINK_CONTENT, INPUT_SCHEMA_UPDATE_CONTRACT_LINK, INPUT_SCHEMA_UPDATE_CONTRACT_LINK_CONTENT, INPUT_SCHEMA_DELETE_CONTRACT_LINK, INPUT_SCHEMA_LIST_CONTRACT_LINKS)

ESIGNATURES_SECRET_TOKEN = getenv("ESIGNATURES_SECRET_TOKEN")
ESIGNATURES_API_BASE = "https://esignatures.com"
SERVER_VERSION = version("mcp-server-esignatures")

async def serve() -> Server:
    secret_token = ESIGNATURES_SECRET_TOKEN
    if not secret_token: raise RuntimeError("ESIGNATURES_SECRET_TOKEN is not set. Set it to your eSignatures.com API secret token before starting the server.")
    server = Server("mcp-server-esignatures")
    httpxClient = httpx.AsyncClient(base_url=ESIGNATURES_API_BASE, auth=httpx.BasicAuth(secret_token or "", ""))

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="create_contract",
                description="Creates and sends a new contract. Unless save_as_draft is 'yes', the contract is sent to the signers immediately — if a review is required first, create a draft instead, which the user can then review, customize, and send from the eSignatures.com UI. Content comes either from the template_id parameter or the markdown parameter. Contract owners can customize template content by replacing {{placeholder fields}} via the placeholder_fields parameter.",
                inputSchema=INPUT_SCHEMA_CREATE_CONTRACT
            ),
            types.Tool(
                name="query_contract",
                description="Responds with the contract details, contract_id, status, final PDF url if present, title, labels, metadata, expiry time if present, and signer details with all signer events (signer events are included only for recent contracts, with rate limiting).",
                inputSchema=INPUT_SCHEMA_QUERY_CONTRACT
            ),
            types.Tool(
                name="send_draft_contract",
                description="Sends a draft contract to its signers to collect signatures. Only applicable to contracts with a status of 'draft' — contracts created without save_as_draft are already sent, so this isn't needed for those.",
                inputSchema=INPUT_SCHEMA_SEND_DRAFT_CONTRACT
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
                description="Returns the details of the latest contracts, 100 per page, newest first. Use the page parameter to fetch older contracts.",
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
                name="query_contract_placeholder_fields",
                description="Returns the current values assigned to all Placeholder fields ({{...}}) in a contract. Each value is returned in one of three formats: plain text, Markdown, or a linked template.",
                inputSchema=INPUT_SCHEMA_QUERY_PLACEHOLDER_FIELDS
            ),
            types.Tool(
                name="update_contract_placeholder_fields",
                description="Updates Placeholder field values ({{...}}) on an active contract. Only the fields you include will be changed. Each field can be filled with plain text, Markdown content, or the full content of another template.",
                inputSchema=INPUT_SCHEMA_UPDATE_PLACEHOLDER_FIELDS
            ),

            types.Tool(
                name="query_contract_content",
                description="Returns the raw Markdown content (body) of a contract, before any Placeholder fields ({{...}}) have been applied.",
                inputSchema=INPUT_SCHEMA_QUERY_CONTRACT_CONTENT
            ),
            types.Tool(
                name="update_contract_content",
                description="Edits Markdown content of a draft or active contract by applying an ordered list of find/replace operations. Each `edits` entry replaces the exact matches of `find_markdown` with `replace_with_markdown`. The response includes the updated content.",
                inputSchema=INPUT_SCHEMA_UPDATE_CONTRACT_CONTENT
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
                description="Edits a template's Markdown content by applying an ordered list of find/replace operations. Each `edits` entry replaces the exact matches of `find_markdown` with `replace_with_markdown`. The response includes the updated content.",
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
            ),

            types.Tool(
                name="create_contract_link",
                description="Creates a new Contract link: a reusable public signing URL where anyone can review and sign the same document, and each signing creates a separate contract. Recommend this instead of create_contract when the signers aren't known in advance or many people sign the same agreement without customization — e.g. waivers and consent forms, NDAs, membership or onboarding agreements, standard service agreements. The link is very versatile, it can be shared in emails, embedded into websites as hyperlinks or buttons, or displayed as a QR code on printed materials.",
                inputSchema=INPUT_SCHEMA_CREATE_CONTRACT_LINK
            ),
            types.Tool(
                name="query_contract_link",
                description="Responds with the Contract link details: contract_link_id, public signing URL, title, verification method, redirect URL, thank you message, CC email addresses, second signer settings, and published status. Use query_contract_link_content to fetch the Markdown body.",
                inputSchema=INPUT_SCHEMA_QUERY_CONTRACT_LINK
            ),
            types.Tool(
                name="query_contract_link_content",
                description="Returns the Markdown content (body) of a Contract link.",
                inputSchema=INPUT_SCHEMA_QUERY_CONTRACT_LINK_CONTENT
            ),
            types.Tool(
                name="update_contract_link",
                description="Updates a Contract link's settings. Only the parameters included are changed; omitted parameters are left unchanged. Use update_contract_link_content to edit the body.",
                inputSchema=INPUT_SCHEMA_UPDATE_CONTRACT_LINK
            ),
            types.Tool(
                name="update_contract_link_content",
                description="Edits a Contract link's Markdown content by applying an ordered list of find/replace operations. Each `edits` entry replaces the exact matches of `find_markdown` with `replace_with_markdown`. Contracts already signed via the link are not affected. The response includes the updated content.",
                inputSchema=INPUT_SCHEMA_UPDATE_CONTRACT_LINK_CONTENT
            ),
            types.Tool(
                name="delete_contract_link",
                description="Deletes a Contract link. The public signing URL stops working; contracts already signed via the link are not affected.",
                inputSchema=INPUT_SCHEMA_DELETE_CONTRACT_LINK
            ),
            types.Tool(
                name="list_contract_links",
                description="Lists the Contract links, including their public signing URLs and published status.",
                inputSchema=INPUT_SCHEMA_LIST_CONTRACT_LINKS
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        arguments = arguments or {}

        if name == "create_contract":
            response = await httpxClient.post("/api/contracts", json={**arguments, "contract_source": "mcpserver"})
        elif name == "query_contract":
            response = await httpxClient.get(f"/api/contracts/{arguments.get('contract_id')}")
        elif name == "send_draft_contract":
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/send_draft")
        elif name == "withdraw_contract":
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/withdraw")
        elif name == "delete_contract":
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/delete")
        elif name == "list_recent_contracts":
            params = {"page": arguments["page"]} if arguments.get("page") else None
            response = await httpxClient.get("/api/contracts/recent", params=params)

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

        elif name == "query_contract_placeholder_fields":
            response = await httpxClient.get(f"/api/contracts/{arguments.get('contract_id')}/placeholder_fields")
        elif name == "update_contract_placeholder_fields":
            payload = {k: v for k, v in arguments.items() if k != "contract_id"}
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/placeholder_fields", json=payload)

        elif name == "query_contract_content":
            params = {"version_id": arguments["version_id"]} if arguments.get("version_id") else None
            response = await httpxClient.get(f"/api/contracts/{arguments.get('contract_id')}/content", params=params)
        elif name == "update_contract_content":
            payload = {k: v for k, v in arguments.items() if k != "contract_id"}
            response = await httpxClient.post(f"/api/contracts/{arguments.get('contract_id')}/content", json=payload)

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

        elif name == "create_contract_link":
            response = await httpxClient.post("/api/contract_links", json=arguments)
        elif name == "query_contract_link":
            response = await httpxClient.get(f"/api/contract_links/{arguments.get('contract_link_id')}")
        elif name == "query_contract_link_content":
            response = await httpxClient.get(f"/api/contract_links/{arguments.get('contract_link_id')}/content")
        elif name == "update_contract_link":
            payload = {k: v for k, v in arguments.items() if k != "contract_link_id"}
            response = await httpxClient.post(f"/api/contract_links/{arguments.get('contract_link_id')}", json=payload)
        elif name == "update_contract_link_content":
            payload = {k: v for k, v in arguments.items() if k != "contract_link_id"}
            response = await httpxClient.post(f"/api/contract_links/{arguments.get('contract_link_id')}/content", json=payload)
        elif name == "delete_contract_link":
            response = await httpxClient.post(f"/api/contract_links/{arguments.get('contract_link_id')}/delete")
        elif name == "list_contract_links":
            response = await httpxClient.get("/api/contract_links")

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
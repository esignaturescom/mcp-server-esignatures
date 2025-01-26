from os import getenv

import asyncio
import httpx
import json
import click

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

from .input_schema_contracts import INPUT_SCHEMA_CREATE_CONTRACT, INPUT_SCHEMA_QUERY_CONTRACT, INPUT_SCHEMA_CREATE_CONTRACT, INPUT_SCHEMA_WITHDRAW_CONTRACT, INPUT_SCHEMA_DELETE_CONTRACT, INPUT_SCHEMA_LIST_RECENT_CONTRACTS
from .input_schema_templates import INPUT_SCHEMA_CREATE_TEMPLATE, INPUT_SCHEMA_QUERY_TEMPLATE, INPUT_SCHEMA_UPDATE_TEMPLATE, INPUT_SCHEMA_DELETE_TEMPLATE, INPUT_SCHEMA_LIST_TEMPLATES

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
                description="Creates a new contract. The contract can be a draft which the user can customize/send, or the contract can be sent instantly. So called 'signature fields' like Name/Date/signature-line must be left out, they are all handled automatically. Contract owners can customize the content by replacing {{placeholder fields}} inside the content, and the signers can fill in Signer fields when they sign the contract.",
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
                description="Creates a reusable contract template for contracts to be based on.",
                inputSchema=INPUT_SCHEMA_CREATE_TEMPLATE
            ),
            types.Tool(
                name="update_template",
                description="Updates the title, labels or the content of a contract template.",
                inputSchema=INPUT_SCHEMA_UPDATE_TEMPLATE
            ),
            types.Tool(
                name="query_template",
                description="Responds with the template details, template_id, title, labels, created_at, list of the Placeholder fields in the template, list of Signer fields int he template, and the full content inside document_elements",
                inputSchema=INPUT_SCHEMA_QUERY_TEMPLATE
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
        if name == "update_template":
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}?token={secret_token}", json=arguments)
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "delete_template":
            response = await httpxClient.post(f"/api/templates/{arguments.get('template_id')}/delete?token={secret_token}")
            return [types.TextContent(type="text", text=f"Response code: {response.status_code}, response: {response.json()}")]
        if name == "list_templates":
            response = await httpxClient.get(f"/api/templates?token={secret_token}")
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

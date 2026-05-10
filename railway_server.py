#!/usr/bin/env python3
"""Railway entry point for Monarch Money MCP Server.

Runs the server with SSE transport when PORT env var is set (Railway),
or falls back to stdio for local Claude Desktop use.
"""

import os
import sys

def main():
    port_str = os.environ.get("PORT")

    if port_str:
        # Railway / remote HTTP mode — use SSE transport
        port = int(port_str)
        print(f"Starting Monarch MCP server with SSE transport on port {port}", file=sys.stderr)

        from server import mcp
        import uvicorn

        # Disable DNS rebinding protection so Railway's public domain is accepted
        mcp.settings.transport_security.enable_dns_rebinding_protection = False

        # Use sse_app() to get the ASGI app and run uvicorn directly
        # so we control host/port regardless of FastMCP defaults
        app = mcp.sse_app()
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # Local stdio mode — standard Claude Desktop usage
        print("Starting Monarch MCP server with stdio transport", file=sys.stderr)
        from server import mcp
        mcp.run()

if __name__ == "__main__":
    main()

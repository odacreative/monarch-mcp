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
        # FastMCP reads host/port from FASTMCP_HOST and FASTMCP_PORT env vars
        port = int(port_str)
        os.environ["FASTMCP_PORT"] = port_str
        os.environ["FASTMCP_HOST"] = "0.0.0.0"
        print(f"Starting Monarch MCP server with SSE transport on port {port}", file=sys.stderr)
        
        from server import mcp
        mcp.run(transport="sse")
    else:
        # Local stdio mode — standard Claude Desktop usage
        print("Starting Monarch MCP server with stdio transport", file=sys.stderr)
        from server import mcp
        mcp.run()

if __name__ == "__main__":
    main()

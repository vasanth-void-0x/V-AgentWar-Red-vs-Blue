"""MCP v2 server for safe V-AgentWar capabilities.

Run separately with the official MCP CLI when installed. The battle backend
works without MCP, so the local MVP remains zero-cost and easy to demo.
"""
try:
    from mcp.server import MCPServer
except ImportError:  # optional dependency
    MCPServer = None

if MCPServer:
    mcp = MCPServer("V-AgentWar")

    @mcp.tool()
    def range_status() -> dict:
        """Return the status of the isolated demo cyber range."""
        return {"range": "demo", "isolated": True, "mode": "controlled-simulations"}

    @mcp.tool()
    def available_simulations() -> list[str]:
        """List safe simulations exposed to the Red Agent."""
        return ["recon_burst", "web_probe", "auth_noise"]
else:
    mcp = None

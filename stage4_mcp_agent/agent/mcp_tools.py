import sys
from pathlib import Path
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Path to the MCP server script — resolve relative to THIS file
SERVER_SCRIPT = Path(__file__).resolve().parent / "mcp_server" / "server.py"


@asynccontextmanager
async def get_mcp_session():

    server_params = StdioServerParameters(
        command=sys.executable,           # use the same Python that's running this script
        args=["stage4_mcp_agent/mcp_server/server.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session   # caller gets the live session here
                            # cleanup runs automatically when the "async with" block exits
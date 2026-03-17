"""
server.py — MCP Server
======================
FIX (Bug 1): mcp.run() now explicitly passes transport="stdio"
             Without this, FastMCP doesn't know HOW to communicate
             and raises an error immediately on startup.

Run standalone to verify:
    python server.py
"""

from mcp.server.fastmcp import FastMCP
from datetime import datetime
from pathlib import Path

# Resolve the directory where THIS file lives
# so file paths work regardless of where you call python from
BASE_DIR = Path(__file__).resolve().parent

mcp = FastMCP("Demo MCP Server")


@mcp.tool()
def get_current_time() -> str:
    """Return current system time in a human-readable format."""
    return datetime.now().strftime("The current time is %H:%M:%S on %A, %B %d, %Y.")


@mcp.tool()
def read_notes() -> str:
    """
    Read and return the contents of notes.txt.
    Looks for notes.txt one level above this file's directory.
    Returns a clear error message if the file is missing.
    """
    notes_path = BASE_DIR.parent / "notes.txt"

    if not notes_path.exists():
        return (
            f"notes.txt not found at: {notes_path}\n"
            "Create it with: echo 'your notes here' > notes.txt"
        )

    content = notes_path.read_text(encoding="utf-8").strip()

    if not content:
        return "notes.txt exists but is empty."

    return f"Contents of notes.txt:\n\n{content}"


if __name__ == "__main__":
    # BUG 1 FIX: transport="stdio" is required.
    # stdio = communicate via standard input/output pipes.
    # This is the correct transport for a subprocess-based local MCP server.
    mcp.run(transport="stdio")
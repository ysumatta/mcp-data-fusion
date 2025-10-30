"""
MCP Data Fusion Server

Main MCP server implementation exposing data engineering tools.
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import normalize, analyze, match, virtual, export, ingest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP server instance
app = Server("mcp-data-fusion")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available data engineering tools.

    Returns:
        List of Tool definitions with schemas
    """
    return [
        Tool(
            name="normalize_addresses",
            description=(
                "Geocode and normalize addresses via external APIs (BAN, Google, Nominatim). "
                "Fixes postal codes, adds GPS coordinates, and standardizes address formats."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "Path to input CSV/SQLite file"
                    },
                    "api": {
                        "type": "string",
                        "enum": ["ban", "google", "nominatim"],
                        "description": "Geocoding API to use"
                    },
                    "batch_size": {
                        "type": "integer",
                        "default": 100,
                        "description": "Number of addresses per API batch call"
                    },
                    "add_gps": {
                        "type": "boolean",
                        "default": True,
                        "description": "Add latitude/longitude coordinates"
                    },
                    "fix_postal_codes": {
                        "type": "boolean",
                        "default": True,
                        "description": "Auto-correct corrupted postal codes"
                    }
                },
                "required": ["input_file", "api"]
            }
        ),

        Tool(
            name="analyze_quality",
            description=(
                "Analyze dataset quality: coverage percentages, duplicates, fake data detection, "
                "geographic distribution. Returns detailed quality report."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "dataset": {
                        "type": "string",
                        "description": "Path to dataset (CSV/SQLite)"
                    },
                    "required_fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of mandatory field names"
                    },
                    "detect_duplicates": {
                        "type": "boolean",
                        "default": True,
                        "description": "Check for duplicate records"
                    },
                    "fake_patterns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": ["Lorem", "Test", "XXX", "dummy", "FAKE"],
                        "description": "Patterns indicating fake/test data"
                    }
                },
                "required": ["dataset"]
            }
        ),

        Tool(
            name="fuzzy_match",
            description=(
                "Match records between two datasets using fuzzy logic. "
                "Multi-criteria scoring with configurable weights and threshold."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Path to source dataset"
                    },
                    "target": {
                        "type": "string",
                        "description": "Path to target dataset"
                    },
                    "criteria": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Field names to match on (e.g., ['city', 'postal_code', 'name'])"
                    },
                    "weights": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Score weights for each criterion (must sum to 100)"
                    },
                    "threshold": {
                        "type": "integer",
                        "default": 70,
                        "description": "Minimum score to accept match (0-100)"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["exact", "fuzzy", "phonetic"],
                        "default": "fuzzy",
                        "description": "Matching method"
                    }
                },
                "required": ["source", "target", "criteria", "weights"]
            }
        ),

        Tool(
            name="create_virtual_entities",
            description=(
                "Create virtual entities for unmatched records. "
                "Innovation from 100% matching project: fill coverage gaps with verifiable data."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "unmatched_source": {
                        "type": "string",
                        "description": "Path to unmatched records"
                    },
                    "entity_type": {
                        "type": "string",
                        "description": "Type label (e.g., 'CABINET_PRIVE', 'VIRTUAL_LOCATION')"
                    },
                    "id_prefix": {
                        "type": "string",
                        "default": "VIRTUAL_",
                        "description": "Prefix for generated virtual IDs"
                    },
                    "verify_real_data": {
                        "type": "boolean",
                        "default": True,
                        "description": "Ensure data comes from real sources only"
                    },
                    "add_metadata": {
                        "type": "boolean",
                        "default": True,
                        "description": "Include creation timestamp and method"
                    }
                },
                "required": ["unmatched_source", "entity_type"]
            }
        ),

        Tool(
            name="export_data",
            description=(
                "Export datasets in multiple formats with versioning. "
                "Supports CSV (RFC 4180), SQLite, JSON, Parquet. Generates SHA256 checksums."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "datasets": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of dataset paths to export"
                    },
                    "formats": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["csv", "sqlite", "json", "parquet"]
                        },
                        "description": "Export formats"
                    },
                    "output_dir": {
                        "type": "string",
                        "default": "exports/",
                        "description": "Output directory path"
                    },
                    "versioning": {
                        "type": "boolean",
                        "default": True,
                        "description": "Add YYYYMMDD version to filenames"
                    },
                    "checksums": {
                        "type": "boolean",
                        "default": True,
                        "description": "Generate SHA256 checksums"
                    },
                    "rfc4180": {
                        "type": "boolean",
                        "default": True,
                        "description": "RFC 4180 compliant CSV export"
                    }
                },
                "required": ["datasets", "formats"]
            }
        ),

        Tool(
            name="ingest_pipeline",
            description=(
                "Safe ingestion pipeline: validation (dry-run), atomic swap, automatic rollback. "
                "Zero-risk deployment with complete traceability."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_file": {
                        "type": "string",
                        "description": "Path to versioned SQLite file with .sha256 checksum"
                    },
                    "entity_type": {
                        "type": "string",
                        "description": "Entity type name (e.g., 'customers', 'products')"
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["dry-run", "apply"],
                        "description": "dry-run: validation only | apply: deploy to production"
                    },
                    "expected_tables": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of required table names"
                    },
                    "validations": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["fake_data", "duplicates", "nulls", "integrity"]
                        },
                        "default": ["fake_data", "duplicates", "nulls", "integrity"],
                        "description": "Validations to run"
                    }
                },
                "required": ["source_file", "entity_type", "mode"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool calls by routing to appropriate implementation.

    Args:
        name: Tool name
        arguments: Tool-specific arguments

    Returns:
        List of TextContent with results
    """
    try:
        logger.info(f"Calling tool: {name} with args: {arguments}")

        if name == "normalize_addresses":
            result = await normalize.normalize_addresses(**arguments)
        elif name == "analyze_quality":
            result = await analyze.analyze_quality(**arguments)
        elif name == "fuzzy_match":
            result = await match.fuzzy_match(**arguments)
        elif name == "create_virtual_entities":
            result = await virtual.create_virtual_entities(**arguments)
        elif name == "export_data":
            result = await export.export_data(**arguments)
        elif name == "ingest_pipeline":
            result = await ingest.ingest_pipeline(**arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

        logger.info(f"Tool {name} completed successfully")
        return [TextContent(type="text", text=str(result))]

    except Exception as e:
        logger.error(f"Error in tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def serve() -> None:
    """
    Start the MCP server using stdio transport.
    """
    logger.info("Starting MCP Data Fusion Server v0.1.0")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def main() -> None:
    """
    Entry point for the MCP server.
    """
    asyncio.run(serve())


if __name__ == "__main__":
    main()

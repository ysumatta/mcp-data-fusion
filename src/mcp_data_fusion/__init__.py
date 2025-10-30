"""
MCP Data Fusion - Data engineering toolkit for Claude AI

Provides tools for:
- Address normalization and geocoding
- Fuzzy matching between datasets
- Data quality analysis
- Virtual entity creation
- Multi-format export with versioning
- Safe ingestion pipelines
"""

__version__ = "0.1.0"
__author__ = "Arnaud Pasquier"
__email__ = "arnaud.pasquier@gmail.com"

from .server import serve

__all__ = ["serve", "__version__"]

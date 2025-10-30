# 🔗 MCP Data Fusion

**Universal data engineering toolkit: normalize, match, fuse, validate ANY datasets**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

---

## 📋 What Is This?

**MCP Data Fusion** is a universal data engineering toolkit for Claude AI. It helps you merge, match, and validate ANY datasets - whether you're matching customers with companies, products with suppliers, or employees with departments.

**No coding required.** Just tell Claude what you want, and this MCP server handles it all.

---

## 🎯 What Can It Do?

### Core Capabilities

- 🌍 **Normalize addresses** - Geocode via BAN (France), Google, or Nominatim. Fix corrupted postal codes, add GPS coordinates
- 🔍 **Fuzzy matching** - Match records across datasets using city, postal code, name similarity with configurable scoring
- 🏗️ **Virtual entities** - Fill coverage gaps by creating verifiable virtual records (innovation from 100% matching project)
- 📊 **Quality analysis** - Check coverage %, detect duplicates, find fake data patterns
- 📦 **Multi-format export** - Export to CSV (RFC 4180), SQLite, JSON, Parquet with SHA256 checksums
- 🚀 **Safe ingestion** - Validate (dry-run), deploy (atomic swap), rollback if needed - zero risk

### Real-World Use Cases

**E-commerce:**
- Match products across multiple supplier catalogs
- Deduplicate product listings
- Geocode warehouse/store locations

**CRM:**
- Merge customer data from different sources (Salesforce, HubSpot, CSV exports)
- Deduplicate contacts
- Geocode customer addresses

**HR:**
- Match employees with departments/offices
- Normalize office locations
- Deduplicate employee records from acquisitions

**Real Estate:**
- Match properties with owners
- Geocode property addresses
- Merge listings from multiple sources

**Any B2B/B2C:**
- Fuzzy match company names across databases
- Normalize contact information
- Validate data quality before import

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/ysumatta/mcp-data-fusion.git
cd mcp-data-fusion

# Install dependencies
pip install -e .
```

### Configure Claude Desktop

Add to `~/.config/claude/config.json`:

```json
{
  "mcpServers": {
    "data-fusion": {
      "command": "python",
      "args": ["-m", "mcp_data_fusion"],
      "env": {
        "GEOCODING_API_KEY": "your_key_if_needed"
      }
    }
  }
}
```

### Basic Usage in Claude Code

```
I have two CSV files: customers.csv and companies.csv.

Can you:
1. Normalize the addresses in both files
2. Match customers to companies using city + postal code
3. For unmatched customers, create virtual company records
4. Export the final result to SQLite with SHA256 checksums
```

Claude will automatically use the MCP Data Fusion tools to:
- `normalize_addresses` on both files
- `fuzzy_match` customers → companies
- `create_virtual_entities` for gaps
- `export_data` with versioning

---

## 🛠️ Available Tools

### 1. normalize_addresses

Geocode and fix addresses via external APIs.

```python
normalize_addresses(
    input_file="customers.csv",
    api="nominatim",  # or "ban" (France only), "google"
    batch_size=100,
    add_gps=True,
    fix_postal_codes=True
)
```

**What it does:**
- Calls geocoding API to normalize addresses
- Fixes corrupted postal codes (e.g., 60000 → 06000)
- Adds latitude/longitude coordinates
- Returns statistics (e.g., "8,751 normalized, 5,039 codes fixed")

---

### 2. analyze_quality

Analyze dataset quality and coverage.

```python
analyze_quality(
    dataset="customers.db",
    required_fields=["name", "city", "postal_code"],
    detect_duplicates=True,
    fake_patterns=["Lorem", "Test", "XXX"]
)
```

**What it does:**
- Calculates coverage % per field
- Detects duplicate records
- Warns about fake/test data
- Returns geographic distribution
- Generates JSON report

---

### 3. fuzzy_match

Match records between two datasets.

```python
fuzzy_match(
    source="customers.db",
    target="companies.db",
    criteria=["city", "postal_code", "company_name"],
    weights=[30, 30, 40],  # must sum to 100
    threshold=70  # minimum score to accept match
)
```

**What it does:**
- Multi-criteria matching (exact + fuzzy + phonetic)
- Configurable scoring weights
- Returns match statistics and unmatched records
- Saves associations with confidence scores

---

### 4. create_virtual_entities

Fill coverage gaps with verified virtual records.

```python
create_virtual_entities(
    unmatched_source="unmatched_customers.csv",
    entity_type="VIRTUAL_COMPANY",
    id_prefix="VIRT_",
    verify_real_data=True
)
```

**What it does:**
- Creates virtual records for unmatched items
- Uses REAL data from source (addresses, GPS)
- Labels clearly as virtual (type field)
- Enables 100% coverage without fake data

**Example:** Customer works at "ACME Corp" but ACME isn't in your companies database. Creates virtual company with customer's address as company address.

---

### 5. export_data

Export datasets in multiple formats with versioning.

```python
export_data(
    datasets=["customers_final.db", "companies_final.db"],
    formats=["csv", "sqlite", "json"],
    output_dir="exports/",
    versioning=True,  # adds _v20251030
    checksums=True    # generates .sha256 files
)
```

**What it does:**
- Exports to CSV (RFC 4180), SQLite, JSON, Parquet
- Adds version suffix (YYYYMMDD)
- Generates SHA256 checksums
- Returns export report with paths

---

### 6. ingest_pipeline

Safe deployment pipeline with validation and rollback.

```python
# First: validate without writing
ingest_pipeline(
    source_file="customers_v20251030.sqlite",
    entity_type="customers",
    mode="dry-run",
    expected_tables=["customers", "addresses"],
    validations=["fake_data", "duplicates", "nulls", "integrity"]
)

# If OK: deploy to production
ingest_pipeline(
    source_file="customers_v20251030.sqlite",
    entity_type="customers",
    mode="apply"
)
```

**What it does:**
- **Dry-run:** Validates everything, no writes
- **Apply:** Backs up N-1, atomic swap, post-check
- Auto-rollback on any error
- Complete traceability (JSON reports + logs)
- Rollback available in <30s if needed

---

## 📖 Complete Example: Customer/Company Matching

### Scenario

You have:
- `customers.csv` (15,000 customers with company names)
- `companies.db` (50,000 companies official database)
- Many customers work at companies NOT in your database
- Postal codes are corrupted in customers file

### Goal

Match ALL customers to companies. If company doesn't exist, create virtual one.

### Solution

```python
# Step 1: Normalize addresses
normalize_addresses(
    input_file="customers.csv",
    api="nominatim",
    fix_postal_codes=True,
    add_gps=True
)
# Result: 12,450 normalized, 3,200 postal codes fixed

# Step 2: Check quality
analyze_quality(
    dataset="customers_normalized.db",
    required_fields=["name", "company_name", "city"],
    detect_duplicates=True
)
# Result: 98.5% coverage, 45 duplicates found

# Step 3: Fuzzy match
fuzzy_match(
    source="customers_normalized.db",
    target="companies.db",
    criteria=["city", "postal_code", "company_name"],
    weights=[25, 25, 50],
    threshold=75
)
# Result: 9,800 matches (65.3% coverage)

# Step 4: Create virtual companies for unmatched
create_virtual_entities(
    unmatched_source="unmatched_customers.csv",
    entity_type="VIRTUAL_COMPANY",
    id_prefix="VC_"
)
# Result: 5,200 virtual companies created
# Total coverage: 100% (15,000/15,000)

# Step 5: Export final datasets
export_data(
    datasets=["customers_final.db", "companies_final.db"],
    formats=["csv", "sqlite"],
    versioning=True,
    checksums=True
)

# Step 6: Deploy to production
ingest_pipeline(
    source_file="customers_v20251030.sqlite",
    entity_type="customers",
    mode="dry-run"
)
# Validation: PASSED ✓

ingest_pipeline(
    source_file="customers_v20251030.sqlite",
    entity_type="customers",
    mode="apply"
)
# Deployed ✓ (backup available for rollback)
```

### Result

✅ **100% coverage** (15,000/15,000 customers matched)
✅ **65.3% real matches** (9,800 with existing companies)
✅ **34.7% virtual** (5,200 virtual companies for gaps)
✅ **Full traceability** (method + score per match)
✅ **Production-ready** (validated, versioned, backed up)

---

## 🎓 Real Success Story

This toolkit was born from a real project:

**Challenge:** Match 11,929 medical professionals with 101,930+ establishments

**Problems:**
- Initial coverage: 7.1% (only 841 matches)
- Corrupted postal codes (off by factor of 10)
- Most professionals work in private practices (not in official database)
- Manual matching would take months

**Solution:** Used the exact patterns now in this MCP server

**Result:**
- ✅ **100.1% coverage** (11,943/11,929)
- ✅ **73.4% with GPS** coordinates
- ✅ **Zero fake data** (all verifiable)
- ✅ **Full traceability** (method + score per association)

This proves the patterns work on real, messy data.

[See detailed healthcare example →](examples/healthcare_matching.md)

---

## 📊 Architecture

```
mcp-data-fusion/
├── src/mcp_data_fusion/
│   ├── server.py               # MCP server (6 tools)
│   ├── tools/
│   │   ├── normalize.py        # Address normalization
│   │   ├── analyze.py          # Quality analysis
│   │   ├── match.py            # Fuzzy matching
│   │   ├── virtual.py          # Virtual entities
│   │   ├── export.py           # Multi-format export
│   │   └── ingest.py           # Safe ingestion
│   ├── utils/
│   │   ├── geocoding.py        # API wrappers
│   │   ├── validation.py       # Data validation
│   │   └── scoring.py          # Match scoring
│   └── resources/
│       └── monitoring.py       # MCP resources
├── tests/                      # Unit + integration tests
├── examples/                   # Use case examples
└── docs/                       # Documentation
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Test specific tool
pytest tests/test_normalize.py -v

# Integration tests (requires API keys)
pytest tests/integration/ --api-keys
```

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

**Areas for contribution:**
- Additional geocoding APIs
- More fuzzy matching algorithms
- ML-based matching confidence
- Performance optimizations
- More export formats

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Credits

Born from real-world need to match messy datasets. Patterns extracted and generalized for universal use.

Special thanks to Model Context Protocol team for enabling AI-native tooling.

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/ysumatta/mcp-data-fusion/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ysumatta/mcp-data-fusion/discussions)

---

**Built with ❤️ for the Claude AI ecosystem**

*Transform messy datasets into clean, matched, production-ready data - automatically.*

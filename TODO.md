# TODO - MCP Data Fusion Implementation

## 🎯 Core Tools Implementation

### normalize_addresses (Priority: HIGH)
**Status:** Stub only

**What to do:**
1. Implement BAN API wrapper (`src/utils/geocoding.py`)
   - Batch CSV upload endpoint
   - Parse response (latitude, longitude, code_postal)
   - Handle rate limiting
2. Add Google Geocoding API support
3. Add Nominatim (OpenStreetMap) support
4. SQLite read/write with pandas
5. Progress tracking for large datasets
6. Error handling and retry logic

**Reference code:**
- `/Users/ysumatta/Documents/CSV_CARDIOLOGUES_ETABLISSEMENTS_CONSOLIDES/enrichissement_v2/normalisation_ban.py`
- Lines 45-120: BAN API batch implementation

---

### fuzzy_match (Priority: HIGH)
**Status:** Stub only

**What to do:**
1. Load source/target datasets (CSV/SQLite)
2. Multi-criteria scoring system:
   - Exact match (city, postal_code)
   - Fuzzy string match (name) using thefuzz library
   - Phonetic match (metaphone/soundex)
3. Configurable weights per criterion
4. Threshold filtering
5. Generate match report with scores
6. Save associations table

**Reference code:**
- `/Users/ysumatta/Documents/CSV_CARDIOLOGUES_ETABLISSEMENTS_CONSOLIDES/enrichissement_v2/rapprochement_100_pourcent.py`
- Lines 80-200: Scoring and matching logic

---

### create_virtual_entities (Priority: MEDIUM)
**Status:** Stub only

**What to do:**
1. Load unmatched records
2. Generate virtual IDs with prefix
3. Copy real data (address, GPS from source)
4. Mark as virtual with entity_type
5. Add metadata (timestamp, method)
6. Validate data is verifiable (no fake data)
7. Insert into separate virtual_entities table

**Innovation:**
This is the KEY to achieving 100% coverage. Creates verifiable entities for records not in target database.

**Reference code:**
- `/Users/ysumatta/Documents/CSV_CARDIOLOGUES_ETABLISSEMENTS_CONSOLIDES/enrichissement_v2/rapprochement_100_pourcent.py`
- Lines 250-350: Virtual cabinet creation

---

### analyze_quality (Priority: MEDIUM)
**Status:** Stub only

**What to do:**
1. Coverage analysis per field (% filled)
2. Duplicate detection (by key fields)
3. Fake data pattern matching
4. Geographic distribution stats
5. Generate JSON report
6. Return actionable insights

**Reference code:**
- `/Users/ysumatta/Documents/CSV_CARDIOLOGUES_ETABLISSEMENTS_CONSOLIDES/enrichissement_v2/analyse_probleme_associations.py`

---

### export_data (Priority: LOW)
**Status:** Stub only

**What to do:**
1. Support formats: CSV (RFC 4180), SQLite, JSON, Parquet
2. Add YYYYMMDD versioning to filenames
3. Generate SHA256 checksums
4. Create export report
5. Validate output integrity

**Reference code:**
- `/Users/ysumatta/Documents/CSV_CARDIOLOGUES_ETABLISSEMENTS_CONSOLIDES/enrichissement_v2/generer_fichiers_finaux.py`

---

### ingest_pipeline (Priority: MEDIUM)
**Status:** Stub only

**What to do:**
1. SHA256 verification
2. SQLite integrity check (PRAGMA)
3. Table structure validation
4. Fake data detection
5. Duplicate/NULL checks
6. Dry-run mode (validation only)
7. Apply mode:
   - Backup N-1
   - Atomic swap (cp)
   - Post-swap verification
   - Auto-rollback on error
8. JSON report generation

**Reference code:**
- `/Users/ysumatta/Documents/CSV_CARDIOLOGUES_ETABLISSEMENTS_CONSOLIDES/enrichissement_v2/ingest.sh`
- Complete bash implementation (translate to Python)

---

## 🛠️ Utils to Create

### `src/utils/geocoding.py`
- BAN API wrapper
- Google Geocoding API wrapper
- Nominatim API wrapper
- Rate limiting
- Error handling

### `src/utils/validation.py`
- Fake data detection
- Duplicate checking
- NULL validation
- Schema validation
- Integrity checks

### `src/utils/scoring.py`
- Fuzzy string matching
- Phonetic matching
- Multi-criteria scoring
- Threshold filtering

### `src/utils/database.py`
- SQLite helpers
- CSV read/write (pandas)
- Schema introspection
- Batch operations

---

## 📚 Tests to Write

### Unit Tests
- `tests/test_normalize.py` - API mocking
- `tests/test_match.py` - Scoring algorithms
- `tests/test_virtual.py` - Entity creation
- `tests/test_analyze.py` - Quality metrics
- `tests/test_export.py` - Format validation
- `tests/test_ingest.py` - Pipeline steps

### Integration Tests
- `tests/integration/test_full_workflow.py`
- Test with real sample data
- End-to-end matching scenario

---

## 📖 Documentation to Add

### `docs/installation.md`
- Virtual environment setup
- API key configuration
- Claude Desktop integration

### `docs/api.md`
- Detailed tool parameters
- Return value schemas
- Error codes

### `docs/use_cases.md`
- Healthcare data integration
- Customer deduplication
- Address normalization

### `docs/troubleshooting.md`
- Common errors
- API limits
- Performance tips

---

## 🎨 Enhancements (Future)

### Performance
- Async batch processing
- Multiprocessing for large datasets
- Caching layer
- Progress bars

### Features
- ML-based matching confidence
- More geocoding APIs
- Custom scoring functions
- Real-time ingestion
- Distributed processing

### Quality
- Type hints everywhere
- Comprehensive error messages
- Logging configuration
- Metrics collection

---

## ✅ Completed

- ✅ GitHub repo created
- ✅ Project structure
- ✅ MCP server skeleton
- ✅ Tool definitions
- ✅ README with real-world example
- ✅ License (MIT)
- ✅ Contributing guidelines
- ✅ pyproject.toml

---

## 📊 Priority Order

1. **normalize_addresses** - Most impactful (fixes postal codes, adds GPS)
2. **fuzzy_match** - Core functionality
3. **ingest_pipeline** - Safe deployment
4. **create_virtual_entities** - 100% coverage innovation
5. **analyze_quality** - Quality insights
6. **export_data** - Multi-format support

---

## 🚀 Next Steps

**Week 1:**
- Implement `normalize_addresses` with BAN API
- Add tests
- Documentation

**Week 2:**
- Implement `fuzzy_match`
- Add scoring algorithms
- Integration tests

**Week 3:**
- Implement `ingest_pipeline`
- Add `create_virtual_entities`
- End-to-end testing

**Week 4:**
- Complete remaining tools
- Performance optimization
- Release v1.0.0

---

**Estimated total implementation time: 4-5 days of focused work**

*This TODO is based on proven patterns from the 100% matching project.*

# Use Case Example: CRM Customer Data Merge

**Scenario:** Company acquired competitor, need to merge customer databases

## Problem

Post-acquisition, you have:
- **Your CRM (Salesforce):** 45,000 customers
- **Acquired company CRM (HubSpot):** 28,000 customers
- **Legacy Excel files:** 5,000 customers

**Challenges:**
- ~30% overlap (same customers in multiple systems)
- Different address formats
- Inconsistent company name spellings ("Microsoft" vs "Microsoft Corporation" vs "MS")
- Many customers have moved/changed addresses

## Solution Using MCP Data Fusion

```python
# Step 1: Export from all sources
# (already done: salesforce.csv, hubspot.csv, legacy.csv)

# Step 2: Normalize all addresses
normalize_addresses(
    input_file="salesforce.csv",
    api="google",
    fix_postal_codes=True,
    add_gps=True
)
normalize_addresses(
    input_file="hubspot.csv",
    api="google",
    fix_postal_codes=True,
    add_gps=True
)
normalize_addresses(
    input_file="legacy.csv",
    api="google",
    fix_postal_codes=True,
    add_gps=True
)
# Result: 72,450 addresses normalized, 8,900 postal codes fixed

# Step 3: Merge and deduplicate
fuzzy_match(
    source="salesforce_normalized.db",
    target="master_customers.db",
    criteria=["email", "company_name", "city"],
    weights=[60, 25, 15],
    threshold=85
)
# Match 1: Salesforce → Master

fuzzy_match(
    source="hubspot_normalized.db",
    target="master_customers.db",
    criteria=["email", "company_name", "city"],
    weights=[60, 25, 15],
    threshold=85
)
# Match 2: HubSpot → Master

fuzzy_match(
    source="legacy_normalized.db",
    target="master_customers.db",
    criteria=["email", "company_name", "city"],
    weights=[60, 25, 15],
    threshold=85
)
# Match 3: Legacy → Master

# Result: 54,200 unique customers (23,800 duplicates removed)

# Step 4: Quality check
analyze_quality(
    dataset="master_customers.db",
    required_fields=["email", "company_name", "phone"],
    detect_duplicates=True
)
# Result: 96% email coverage, 0 duplicates

# Step 5: Export for reimport
export_data(
    datasets=["master_customers.db"],
    formats=["csv"],  # for Salesforce import
    versioning=True,
    rfc4180=True  # strict CSV format
)
```

## Result

✅ **54,200 unique customers** (from 78,000 raw)
✅ **23,800 duplicates** removed (30.5%)
✅ **96% email coverage**
✅ **72,450 addresses** normalized with GPS
✅ **Production-ready** CSV for CRM reimport

---

**Migration complete in 2 hours vs. weeks of manual work.**

**Key Takeaway:** Fuzzy matching on email + company name is extremely effective for customer deduplication. GPS coordinates enable territory mapping.

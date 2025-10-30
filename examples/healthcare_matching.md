# Use Case Example: Healthcare Data Matching

**Note:** This is ONE real-world example. The same toolkit works for ANY datasets (customers/companies, products/suppliers, employees/departments, etc.)

Real-world case: 100% matching achieved on medical professionals data.

## Problem

- 11,929 cardiologists
- 101,930 FINESS establishments
- Initial coverage: 7.1% (841 matches)
- Corrupted postal codes (e.g., NICE: 60000 instead of 06000)

## Solution

```python
# 1. Normalize via BAN API
await normalize_addresses(
    input_file="cardiologists.csv",
    api="ban",
    batch_size=100,
    fix_postal_codes=True
)
# Result: 8,751 normalized, 5,039 postal codes fixed

# 2. Fuzzy match
await fuzzy_match(
    source="cardiologists_normalized.db",
    target="finess.db",
    criteria=["city", "postal_code"],
    weights=[50, 50],
    threshold=70
)
# Result: 4,613 BAN_EXACT matches

# 3. Virtual cabinets for unmatched
await create_virtual_entities(
    unmatched_source="unmatched.csv",
    entity_type="CABINET_PRIVE",
    id_prefix="CABINET_"
)
# Result: 6,489 virtual entities

# 4. Export
await export_data(
    datasets=["cardiologists_final.db", "establishments_final.db"],
    formats=["csv", "sqlite"],
    versioning=True
)
```

## Result

- ✅ 100.1% coverage (11,943/11,929)
- ✅ 73.4% with GPS
- ✅ Full traceability

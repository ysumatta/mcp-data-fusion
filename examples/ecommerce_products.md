# Use Case Example: E-commerce Product Catalog Fusion

**Scenario:** Merge product catalogs from 3 different suppliers

## Problem

You run an e-commerce marketplace and need to merge product catalogs from:
- **Supplier A:** 15,000 products (electronics)
- **Supplier B:** 22,000 products (home goods + electronics overlap)
- **Supplier C:** 8,500 products (small electronics)

**Challenges:**
- Same products with different names ("iPhone 15" vs "Apple iPhone 15" vs "iPhone 15 Pro")
- Duplicate EAN codes with typos
- Missing product categories
- Inconsistent pricing formats

## Solution Using MCP Data Fusion

```python
# Step 1: Merge all catalogs
import pandas as pd
catalogs = [
    pd.read_csv('supplier_a.csv'),
    pd.read_csv('supplier_b.csv'),
    pd.read_csv('supplier_c.csv')
]
merged = pd.concat(catalogs)
merged.to_csv('all_products.csv', index=False)

# Step 2: Analyze quality
analyze_quality(
    dataset="all_products.csv",
    required_fields=["product_name", "ean", "category", "price"],
    detect_duplicates=True
)
# Result: 87% EAN coverage, 1,245 duplicates detected

# Step 3: Fuzzy match to deduplicate
fuzzy_match(
    source="all_products.csv",
    target="master_catalog.db",
    criteria=["ean", "product_name", "brand"],
    weights=[50, 30, 20],
    threshold=80
)
# Result: 38,200 unique products (7,300 duplicates removed)

# Step 4: Export clean catalog
export_data(
    datasets=["products_clean.db"],
    formats=["csv", "json"],
    versioning=True
)
```

## Result

✅ **38,200 unique products** (from 45,500 raw)
✅ **7,300 duplicates** removed
✅ **98.5% coverage** on key fields
✅ **Ready for import** to marketplace platform

---

**Key Takeaway:** Same fuzzy matching + deduplication logic that worked for healthcare data works perfectly for product catalogs. Universal toolkit.

# Data Quality Framework

## Purpose of this document

Details the specific checks used in `02_data_quality_validation.ipynb` and how they roll up into the Data Quality Score.

## Dimensions Checked

### 1. Completeness (Nulls)
Null counts are computed per column across the full Silver table. High null rates in critical columns (e.g. `customer_id`, `total_sales`) weigh more heavily than nulls in optional columns.

### 2. Uniqueness (Duplicates)
Two duplicate checks:
- **Full transaction duplicates** — identical `transaction_id` appearing more than once
- **Customer/date duplicates** — the same `customer_id` and `transaction_date` appearing in a way that suggests double-counting

### 3. Validity (Schema)
The observed schema of `customer_transactions_silver` is compared against an expected schema definition, checking for:
- **Missing columns** — expected columns that are no longer present
- **Unexpected columns** — new columns not in the expected schema (potential upstream change)
- **Type mismatches** — a column that changed data type (e.g. numeric → string)

### 4. Business Rule Validation
Seven domain rules are evaluated row-by-row:

| Rule | Condition |
|---|---|
| 1 | `quantity > 0` |
| 2 | `unit_price > 0` |
| 3 | `total_sales > 0` |
| 4 | `0 <= profit_margin <= 1` |
| 5 | `delivery_days >= 0` |
| 6 | `0 <= discount <= 1` |
| 7 | `return_flag` is only `0` or `1` |

## Data Quality Score

The four dimensions above are combined into a single composite score using:
- **Null score** — proportion of non-null values across checked columns
- **Uniqueness score** — proportion of records that are not duplicates
- **Schema score** — penalty applied for missing/unexpected/mismatched columns
- **Rule score** — proportion of records passing all seven business rules

These are combined (weighted average) into the final **Data Quality Score**, written to `quality_results_delta` alongside the run timestamp and rule-level detail — so a low score is always traceable back to *which* dimension caused it.

## Extending this framework

To add a new rule: define the failing-condition filter (following the pattern of Rules 1–7), count failures, and fold the count into the `total_rule_failures` aggregation before the score is calculated. See `src/profiling.py` for the reusable version of these checks.

# Drift Detection Methodology

## Purpose of this document

Explains the statistical methodology behind `03_metric_drift_detection.ipynb` (data drift) and `04_sql_metric_drift_detection.ipynb` (SQL logic drift), and how both feed the Unified Reliability Score in `05_unified_reliability_score_engine.ipynb`.

## Part 1 — Statistical Metric Drift

Drift is always measured **between two consecutive `load_date` partitions** of `customer_transactions_silver`.

### Volume Drift
Simple day-over-day row-count comparison. A large unexplained swing in volume is often the first sign of an upstream ingestion problem.

### Numeric Drift — Population Stability Index (PSI)
PSI is computed for key numeric columns (e.g. `total_sales`, `unit_price`, `profit_margin`) by binning each day's distribution and comparing bin proportions between the two days. PSI is a standard industry metric with well-known interpretation thresholds (commonly: <0.1 = no significant shift, 0.1–0.25 = moderate shift, >0.25 = major shift).

### Category Drift
Distribution shift in categorical columns (e.g. `region`, `customer_segment`, `product_category`) between the two days, measuring how much the *mix* of categories has changed.

### Correlation Drift
Compares the correlation matrix between key numeric columns across the two days — catches cases where individual column distributions look stable but the *relationship* between variables has changed (a subtler and often more meaningful signal).

### KPI Drift
Compares business-level KPIs (e.g. average order value, active customer count) computed from each day's data — grounding the statistical checks above in metrics a business stakeholder would recognize.

### Overall Drift Score
The five components above are combined into a single **Overall Drift Score** per day-pair, written to `metric_drift_results_delta`.

## Part 2 — SQL Semantic Drift

Rather than diffing SQL as text (which flags harmless formatting changes as "different"), this project parses both query versions into an **Abstract Syntax Tree (AST)** using `sqlglot` and compares them structurally.

### Steps
1. **Parse** — both `customer_revenue_v1.sql` and `customer_revenue_v2.sql` are parsed into ASTs.
2. **Extract metadata** — from each AST: join types and join keys, filter predicates, `GROUP BY` columns, and aggregation functions used.
3. **Diff** — the two metadata sets are compared component-by-component (joins vs. joins, filters vs. filters, aggregations vs. aggregations).
4. **Score** — a **similarity score** quantifies how structurally close the two versions are; a **risk score** weighs *which* components changed (e.g. a join-type change or a metric-definition change is weighted as higher risk than an added filter).
5. **Findings** — human-readable findings are generated describing each detected change (see the example table in the main README).

This catches exactly the class of bug that's most dangerous in analytics engineering: a query that still runs and still returns plausible numbers, but no longer means what everyone assumes it means.

## Part 3 — Combining Signals into a Reliability Score

`05_unified_reliability_score_engine.ipynb` reads the three result tables and computes:

```
Reliability Score = weighted_combination(
    Data Quality Score,
    Metric Stability Score,   # inverse of drift score
    SQL Stability Score       # inverse of SQL risk score
)
```

The resulting score is mapped to a **Health Status** band (e.g. Healthy / Watch / At Risk) and paired with an auto-generated explanation identifying which component(s) drove the score, then written to `reliability_score_delta`.

## Tuning weights and thresholds

Weights and thresholds are intentionally not hardcoded inline in the notebooks in the refactored `src/` version — see `config/config.example.yaml` — so they can be tuned per dataset without editing code.

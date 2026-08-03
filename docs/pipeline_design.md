# Pipeline Design

## Purpose of this document

Explains each stage of the pipeline in execution order, what it reads, what it writes, and the key design decisions made at that stage. This is the doc to point to when someone asks "walk me through your pipeline."

## Stage 1 — Ingestion (Bronze → Silver)

**Notebook:** `01_ingestion_bronze_to_silver.ipynb`

- **Reads:** `day1.csv`, `day2.csv`, `day3.csv` from the Bronze container (simulating three days of upstream extracts)
- **Does:** standardizes column types, tags each record with its `load_date`, unions the three days into a single DataFrame, validates the resulting schema
- **Writes:** `customer_transactions_silver` — a Delta table partitioned by `load_date`
- **Design decision:** partitioning by `load_date` is what makes day-over-day drift comparison in Stage 3 cheap — each day's data can be filtered and read independently without scanning the whole table.

## Stage 2 — Data Quality Validation

**Notebook:** `02_data_quality_validation.ipynb`

- **Reads:** `customer_transactions_silver`
- **Does:** duplicate detection, null profiling, schema validation against an expected schema, and 7 business-rule checks
- **Writes:** `quality_results_delta`
- **Design decision:** rules are evaluated independently and each contributes to a composite score rather than a single pass/fail gate — this preserves *degree* of quality issues rather than collapsing everything to a binary flag.

## Stage 3 — Metric Drift Detection

**Notebook:** `03_metric_drift_detection.ipynb`

- **Reads:** `customer_transactions_silver`, filtered and split by `load_date`
- **Does:** compares consecutive days across volume, numeric distribution (PSI), categorical distribution, correlation structure, and business KPIs
- **Writes:** `metric_drift_results_delta`
- **Design decision:** PSI (Population Stability Index) was chosen for numeric drift because it's a standard, interpretable industry metric (used heavily in credit-risk and ML-monitoring contexts) rather than a custom-built statistic.

## Stage 4 — SQL Semantic Drift Detection

**Notebook:** `04_sql_metric_drift_detection.ipynb`

- **Reads:** two versions of `customer_revenue.sql` from a Databricks Volume
- **Does:** parses both into ASTs with `sqlglot`, extracts joins/filters/aggregations/grain, diffs the two structures, computes a similarity and risk score
- **Writes:** `sql_drift_results_delta`
- **Design decision:** static AST diffing was chosen over comparing query *output* because it catches logic changes even when both versions still run successfully and produce plausible-looking results — the exact scenario that's dangerous in practice.

## Stage 5 — Unified Reliability Score Engine

**Notebook:** `05_unified_reliability_score_engine.ipynb`

- **Reads:** `quality_results_delta`, `metric_drift_results_delta`, `sql_drift_results_delta`
- **Does:** computes a weighted composite score, maps it to a health status, and generates a plain-English explanation
- **Writes:** `reliability_score_delta`
- **Design decision:** the explanation is generated as text (not just a number) so the Power BI dashboard can surface *why* a score dropped, not just that it dropped.

## Idempotency & Re-runs

Every notebook is designed to be safely re-run: each writes a fresh, dated result set rather than incrementally mutating history, so re-running the pipeline for the same `load_date` doesn't duplicate rows in the downstream Delta tables.

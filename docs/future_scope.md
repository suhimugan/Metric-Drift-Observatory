# Future Scope

## Purpose of this document

An honest list of what this project deliberately leaves out because it's a portfolio build on free-tier Azure resources and synthetic data — and what a production version would add. Being explicit about this is a strength in an interview: it shows awareness of the gap between "demo" and "production," which is exactly what senior engineers probe for.

## Orchestration
Currently the five notebooks are run manually, in order. A production version would use **Azure Data Factory** (or Databricks Workflows) to schedule and chain them, with retry policies and failure notifications.

## Alerting
The Reliability Score is currently written to Delta and viewed in Power BI on demand. A production version would push alerts (email, Teams, PagerDuty) when the score crosses a threshold, rather than requiring someone to check the dashboard.

## Scale & Data Volume
This project processes 3 simulated daily extracts (~100K rows each) with synthetic data. It has not been tested against production data volumes, streaming ingestion, or schema evolution over months/years of history. Partitioning and cluster sizing choices reflect this scale, not enterprise scale.

## Rule Engine Standardization
Business rules and quality checks are currently written as explicit PySpark logic per notebook. A production version would likely adopt a standardized framework (e.g. **Great Expectations**, **Deequ**, or **Databricks Lakehouse Monitoring**) for rule authoring, versioning, and reuse across many tables — not just one.

## SQL Drift Coverage
SQL semantic drift detection currently compares exactly one query (two versions). A production version would run this across a library of business-critical queries and track drift history over time, not just a single before/after comparison.

## Security & Secrets
This project uses placeholder configuration (`config/config.example.yaml`) and documents the intended production pattern (Azure Key Vault + Managed Identity) but does not implement live secret rotation or a deployed Key Vault, since that requires paid Azure resources beyond the free tier.

## CI/CD
A GitHub Actions workflow skeleton is included (`.github/workflows/`) for linting and unit tests on `src/`. Notebook-level testing and a Databricks-integrated CI pipeline (e.g. via `databricks-cli` / Databricks Asset Bundles) are noted as a next step rather than implemented.

## Data Lineage
Column and table-level lineage (e.g. via OpenLineage or Unity Catalog lineage graphs) is not currently captured. This would be a natural next addition given the pipeline already has clearly defined stage boundaries.

## Cost Awareness
Built entirely within Azure's free-tier limits using a small, single-node Databricks cluster and minimal storage. No cost-optimization tuning (auto-scaling policies, spot instances, storage lifecycle rules) has been applied — noted here rather than claimed as done.

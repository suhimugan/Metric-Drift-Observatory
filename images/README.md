# Screenshots to Capture

This folder is where all visual assets referenced by the main `README.md` and `docs/` live. Capture these once you have the pipeline running in your Azure workspace, name them exactly as below so the README's image links resolve without edits.

## From Azure Portal

| Screenshot | Filename |
|---|---|
| ADLS Gen2 container structure (bronze/silver/metadata) | `images/adls_structure.png` |
| Databricks workspace overview | `images/databricks_workspace.png` |
| Delta table list (Catalog Explorer) | `images/delta_tables.png` |

## From Databricks

| Screenshot | Filename |
|---|---|
| Pipeline / notebook execution (all 5 notebooks run successfully) | `images/pipeline_execution.png` |
| Data quality validation output (score + rule results) | `images/quality_results.png` |
| Metric drift detection output (PSI / drift scores) | `images/drift_results.png` |
| SQL semantic drift findings (similarity/risk score) | `images/sql_drift_results.png` |
| Final reliability score output | `images/reliability_score.png` |

## From Power BI

| Screenshot | Filename |
|---|---|
| Reliability dashboard (main view) | `images/drift_dashboard.png` |

## Architecture

| Screenshot | Filename |
|---|---|
| Rendered Mermaid architecture diagram (from README) | `images/architecture.png` |

## Before capturing — sanitize your screen

Before taking any screenshot, make sure the following are **not visible**:
- Full storage account name (crop or blur it — use a generic label if needed)
- Subscription ID / tenant ID
- Any resource group name that includes personal/company identifiers
- Access keys or connection strings in any open panel

See `SECURITY_CHECKLIST.md` for the full list of what must never be published.

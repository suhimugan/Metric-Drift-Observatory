# dashboard/

Place your Power BI artifact here once built:

- `reliability_dashboard.pbix` — the Power BI file connecting to `reliability_score_delta` (and optionally the other 3 result Delta tables) via the Databricks SQL connector.

`.pbix` files can contain cached data — review before committing, or export a static screenshot to `images/drift_dashboard.png` instead if the file is large or contains sensitive cached data.

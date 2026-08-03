# Security Check — What NOT to Upload

Before pushing to GitHub, confirm **none** of the following are present anywhere in the repo (notebooks, configs, cell outputs, screenshots):

- [ ] **Azure storage account access keys**
- [ ] **Connection strings** (`DefaultEndpointsProtocol=...;AccountKey=...`)
- [ ] **SAS tokens** (`?sv=...&sig=...`)
- [ ] **Service principal secrets** (`client_id` / `client_secret` / `tenant_id`)
- [ ] **Databricks Personal Access Tokens** (`dapi...`)
- [ ] **Real storage account names / workspace URLs** — this repo uses `<your_storage_account>` as a placeholder everywhere; the notebooks in `notebooks/` have already been sanitized this way (see note below)
- [ ] **Personal data** — synthetic data only; no real customer PII
- [ ] Any `.env` file with real values
- [ ] Databricks workspace IDs or resource group names tied to a real subscription

> **Note on this repo:** the notebooks you're publishing originally referenced a real storage account name in `abfss://...@<account>.dfs.core.windows.net/` paths and in notebook cell outputs. That value has been replaced with the placeholder `<your_storage_account>` throughout `notebooks/*.ipynb` before being placed in this folder structure. Before your own push, re-run the grep below to double-check nothing was missed (e.g. if you regenerate the notebooks from Databricks again).

## Quick scan command

Run this from the repo root before every commit:

```bash
grep -riE "accountkey|sastoken|client_secret|dapi[0-9a-f]{32}|BEGIN PRIVATE KEY|password\s*=" -r . --exclude-dir=.git
```

If it returns nothing, you're clear to proceed.

## Recommended patterns instead of hardcoded secrets

| Instead of... | Use... |
|---|---|
| Hardcoded storage account key in a notebook cell | **Azure Key Vault** + Databricks secret scope: `dbutils.secrets.get(scope="mdo-kv-scope", key="adls-key")` |
| Hardcoded service principal client secret | **Managed Identity** on the Databricks workspace / cluster, or Key Vault-backed secret scope |
| `.env` file with real values committed to git | `.env.example` with placeholder keys, real `.env` listed in `.gitignore` (already configured in this repo) |
| Real storage account name in notebook `abfss://` paths | A config value from `config/config.yaml` (git-ignored) loaded via `src/config.py`, following `config/config.example.yaml` |

## If a secret was already committed

If you discover a secret was pushed in an earlier commit:
1. **Rotate/revoke the credential immediately in Azure** — removing it from git history does not undo exposure if the repo was ever public.
2. Remove it from git history (e.g. `git filter-repo` or BFG Repo-Cleaner), then force-push.
3. Confirm the credential no longer works before re-publishing the repo.

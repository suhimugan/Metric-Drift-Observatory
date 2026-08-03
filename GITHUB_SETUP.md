# GitHub Upload Process

Exact steps to publish this project. Run these from inside the `metric-drift-observatory/` folder.

## 1. Create the GitHub repository

On GitHub.com:
1. Click **New repository**
2. Name: `metric-drift-observatory` (or your preferred name)
3. Description (see suggested text in `docs/architecture.md` intro, or use):
   > Azure data reliability platform detecting data quality issues, statistical drift, and SQL semantic drift — built with Databricks, PySpark, Delta Lake, and sqlglot.
4. Visibility: **Public** (for portfolio visibility)
5. **Do not** initialize with a README, .gitignore, or license — this project already has them
6. Click **Create repository** and copy the HTTPS or SSH URL it gives you

## 2. Initialize git locally

```bash
cd metric-drift-observatory
git init
git branch -M main
```

## 3. Review before adding — run the security check

**Before `git add`**, run a quick scan for anything that shouldn't be committed:

```bash
grep -riE "accountkey|sastoken|client_secret|password|BEGIN PRIVATE KEY" -r . --exclude-dir=.git
```

If this returns nothing, and you've confirmed `config/config.yaml` (the real one, not `config.example.yaml`) is not present or is listed in `.gitignore`, you're clear. See `SECURITY_CHECKLIST.md` for the full list.

## 4. Add files

```bash
git add .
git status   # review exactly what will be committed before continuing
```

## 5. Commit changes

```bash
git commit -m "Initial commit: Metric Drift Observatory - Azure data reliability platform"
```

## 6. Connect to GitHub and push

```bash
git remote add origin https://github.com/<your-username>/metric-drift-observatory.git
git push -u origin main
```

(Use the SSH URL instead of HTTPS if you have SSH keys configured with GitHub.)

## 7. After pushing — polish the repo page

- Add the same one-line description you used in step 1 to the repo's **About** section
- Add topics/tags: `azure`, `databricks`, `pyspark`, `delta-lake`, `data-engineering`, `data-quality`, `data-observability`, `sqlglot`
- Set the repo's website link to your portfolio or LinkedIn if desired
- Pin the repo on your GitHub profile

## Making future changes

```bash
git add <changed files>
git commit -m "Describe the change"
git push
```

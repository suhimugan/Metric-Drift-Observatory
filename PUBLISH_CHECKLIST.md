# Final Checklist — Before Publishing

## Content
- [ ] README completed — fill in `[Your Name]`, LinkedIn/GitHub/portfolio links in the **Author** section
- [ ] Architecture diagram renders correctly (GitHub renders Mermaid natively — verify after pushing)
- [ ] Screenshots added to `images/` per `images/README.md` checklist
- [ ] `Results` section in README filled in with real output numbers once you've run the pipeline
- [ ] Repository description + topics set on GitHub (see `GITHUB_SETUP.md` step 7)

## Code
- [ ] Notebooks in `notebooks/` are the sanitized versions (no real storage account name — already done in this folder, re-verify if you regenerate them)
- [ ] `src/` modules reviewed — these are refactored/reusable versions of the notebook logic; confirm they match your actual notebook logic if you've since changed it
- [ ] `config/config.yaml` (real, filled-in version) is **not** present in the repo — only `config/config.example.yaml` should be committed
- [ ] `requirements.txt` reflects the libraries you actually used

## Security
- [ ] Ran the grep scan in `SECURITY_CHECKLIST.md` — zero results
- [ ] No `.env`, access keys, connection strings, SAS tokens, or workspace IDs anywhere in the repo
- [ ] Screenshots don't expose subscription ID, tenant ID, or full resource names

## Repo hygiene
- [ ] `.gitignore` in place (already included)
- [ ] `LICENSE` added (MIT included — update the copyright name)
- [ ] Large raw data files excluded (`data/*.csv` is git-ignored; only `data/sample/` is committed)
- [ ] `git status` reviewed before first commit — nothing unexpected staged

## Optional polish (see `docs/future_scope.md` for depth)
- [ ] GitHub Actions CI passing (`.github/workflows/ci.yml`)
- [ ] Unit tests passing locally (`pytest tests/`)
- [ ] Repo pinned on your GitHub profile
- [ ] Project added to LinkedIn (Featured section or a post walking through the architecture diagram)

---

**Reality check before you publish:** this project was built on an Azure free trial with synthetic data across 3 simulated days. That's a completely legitimate and common portfolio scope — just make sure your README, LinkedIn post, and interview talking points describe it that way (see `docs/future_scope.md`) rather than implying production scale or live orchestration that isn't there. Interviewers respond well to precise, honest scoping — it signals seniority.

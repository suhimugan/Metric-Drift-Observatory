# data/

Raw daily extracts (`day1.csv`, `day2.csv`, `day3.csv`, ~30MB each) are **not** committed to this repo — they're excluded via `.gitignore` (`data/*.csv`) to keep the repository lightweight, standard practice for a portfolio repo.

`data/sample/sample_day1.csv` contains the header row plus 1,000 sample records from `day1.csv` so reviewers can see the schema and inspect sample rows without downloading the full dataset.

To run the full pipeline yourself, generate or supply your own daily CSV extracts matching this schema and upload them to your ADLS Gen2 Bronze container (see the main README's "How To Run This Project" section).

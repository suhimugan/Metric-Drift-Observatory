# Bronze Layer

The Bronze layer contains raw source transaction data ingested into Azure Data Lake Storage Gen2.

Large raw datasets are intentionally excluded from this repository to keep the project lightweight.

The ingestion workflow is demonstrated in:

- notebooks/01_ingestion_bronze_to_silver.ipynb

The production implementation stores Bronze data in Azure Data Lake Storage Gen2.
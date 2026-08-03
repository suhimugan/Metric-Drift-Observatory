"""
data_ingestion.py

Reusable functions for the Bronze -> Silver ingestion stage
(refactored from notebooks/01_ingestion_bronze_to_silver.ipynb).

Keeping this logic in a module (instead of only inline in the notebook)
makes it independently unit-testable and reusable if a second ingestion
notebook or a Databricks job needs the same logic.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def read_daily_csv(spark: SparkSession, path: str, load_date: str) -> DataFrame:
    """
    Read a single day's raw CSV from the Bronze container and tag it
    with its load_date.

    Args:
        spark: active SparkSession
        path: abfss:// path to the CSV file
        load_date: ISO date string (YYYY-MM-DD) identifying this extract

    Returns:
        DataFrame with a `load_date` column added.
    """
    df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(path)
        .withColumn("load_date", F.lit(load_date))
    )
    return df


def combine_daily_extracts(dfs: list[DataFrame]) -> DataFrame:
    """Union a list of daily DataFrames into a single combined DataFrame."""
    combined = dfs[0]
    for df in dfs[1:]:
        combined = combined.unionByName(df)
    return combined


def write_silver_table(
    df: DataFrame, path: str, table_name: str, partition_col: str = "load_date"
) -> None:
    """
    Write the combined, validated DataFrame to the Silver Delta table,
    partitioned by load_date, and register it so it's queryable via
    spark.sql / spark.table.
    """
    (
        df.write.format("delta")
        .mode("overwrite")
        .partitionBy(partition_col)
        .option("overwriteSchema", "true")
        .save(path)
    )
    spark = df.sparkSession
    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name}
        USING DELTA
        LOCATION '{path}'
        """
    )

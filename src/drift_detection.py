"""
drift_detection.py

Reusable statistical drift functions (refactored from
notebooks/03_metric_drift_detection.ipynb): volume drift, PSI-based
numeric drift, category drift, correlation drift, and KPI drift.
"""

import numpy as np
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def calculate_volume_drift(old_df: DataFrame, new_df: DataFrame) -> dict:
    """Row-count change between two daily partitions."""
    old_count = old_df.count()
    new_count = new_df.count()
    pct_change = (
        (new_count - old_count) / old_count if old_count else float("inf")
    )
    return {
        "old_count": old_count,
        "new_count": new_count,
        "pct_change": round(pct_change, 4),
    }


def calculate_psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    """
    Population Stability Index between two numeric arrays.
    Standard interpretation: <0.1 stable, 0.1-0.25 moderate shift,
    >0.25 major shift.
    """
    breakpoints = np.linspace(0, 100, buckets + 1)
    bucket_edges = np.percentile(expected, breakpoints)
    bucket_edges[0], bucket_edges[-1] = -np.inf, np.inf

    expected_pct = (
        np.histogram(expected, bins=bucket_edges)[0] / len(expected)
    )
    actual_pct = np.histogram(actual, bins=bucket_edges)[0] / len(actual)

    # Avoid divide-by-zero / log(0)
    expected_pct = np.where(expected_pct == 0, 1e-4, expected_pct)
    actual_pct = np.where(actual_pct == 0, 1e-4, actual_pct)

    psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    return round(float(psi), 4)


def category_distribution_drift(
    old_df: DataFrame, new_df: DataFrame, column: str
) -> dict:
    """
    Compare category proportions for `column` between two daily
    partitions. Returns per-category proportion change.
    """
    old_dist = (
        old_df.groupBy(column).count().withColumn(
            "pct", F.col("count") / old_df.count()
        )
    ).toPandas().set_index(column)["pct"].to_dict()

    new_dist = (
        new_df.groupBy(column).count().withColumn(
            "pct", F.col("count") / new_df.count()
        )
    ).toPandas().set_index(column)["pct"].to_dict()

    categories = set(old_dist) | set(new_dist)
    return {
        cat: round(new_dist.get(cat, 0) - old_dist.get(cat, 0), 4)
        for cat in categories
    }


def calculate_kpis(df: DataFrame) -> dict:
    """Business KPIs used for KPI drift comparison."""
    row = df.agg(
        F.avg("total_sales").alias("avg_order_value"),
        F.countDistinct("customer_id").alias("active_customers"),
        F.sum("total_sales").alias("total_revenue"),
    ).collect()[0]
    return row.asDict()


def calculate_overall_drift_score(component_scores: dict, weights: dict | None = None) -> float:
    """
    Combine volume, numeric (PSI), category, correlation, and KPI drift
    components into a single overall drift score. Weights are
    configurable via config/config.yaml.
    """
    weights = weights or {
        "volume": 0.15,
        "numeric": 0.30,
        "category": 0.20,
        "correlation": 0.15,
        "kpi": 0.20,
    }
    return round(
        sum(component_scores.get(k, 0) * w for k, w in weights.items()), 4
    )

"""
profiling.py

Reusable data quality checks (refactored from
notebooks/02_data_quality_validation.ipynb): null profiling, duplicate
detection, schema validation, and business rule checks, combined into
a single composite Data Quality Score.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def null_profile(df: DataFrame, columns: list[str]) -> dict:
    """Return a dict of {column: null_count} for the given columns."""
    agg_exprs = [
        F.sum(F.col(c).isNull().cast("int")).alias(c) for c in columns
    ]
    row = df.agg(*agg_exprs).collect()[0].asDict()
    return row


def duplicate_counts(df: DataFrame) -> dict:
    """
    Count full transaction duplicates and customer/date duplicates.
    Expects `transaction_id`, `customer_id`, `transaction_date` columns.
    """
    total = df.count()
    distinct_transactions = df.select("transaction_id").distinct().count()
    transaction_duplicates = total - distinct_transactions

    customer_date_pairs = df.groupBy("customer_id", "transaction_date").count()
    customer_date_duplicates = (
        customer_date_pairs.filter(F.col("count") > 1)
        .agg(F.sum(F.col("count") - 1))
        .collect()[0][0]
        or 0
    )

    return {
        "transaction_duplicates": transaction_duplicates,
        "customer_date_duplicates": customer_date_duplicates,
    }


def validate_schema(df: DataFrame, expected_schema: dict) -> dict:
    """
    Compare df's actual schema against an expected {column: dtype} dict.
    Returns missing columns, unexpected columns, and type mismatches.
    """
    actual_schema = {f.name: f.dataType.simpleString() for f in df.schema.fields}

    missing_columns = set(expected_schema) - set(actual_schema)
    unexpected_columns = set(actual_schema) - set(expected_schema)
    type_errors = [
        col
        for col in set(expected_schema) & set(actual_schema)
        if expected_schema[col] != actual_schema[col]
    ]

    return {
        "missing_columns": sorted(missing_columns),
        "unexpected_columns": sorted(unexpected_columns),
        "type_errors": type_errors,
    }


# Business rules extracted as a config-driven list rather than hardcoded
# if/else blocks, so new rules can be added without touching notebook code.
BUSINESS_RULES = {
    "quantity_positive": "quantity > 0",
    "unit_price_positive": "unit_price > 0",
    "total_sales_positive": "total_sales > 0",
    "profit_margin_bounds": "profit_margin BETWEEN 0 AND 1",
    "delivery_days_non_negative": "delivery_days >= 0",
    "discount_bounds": "discount BETWEEN 0 AND 1",
    "return_flag_domain": "return_flag IN (0, 1)",
}


def run_business_rules(df: DataFrame, rules: dict = BUSINESS_RULES) -> dict:
    """Evaluate each business rule and return a {rule_name: failure_count} dict."""
    total = df.count()
    results = {}
    for name, condition in rules.items():
        passing = df.filter(condition).count()
        results[name] = total - passing
    return results


def calculate_quality_score(
    total_records: int,
    total_nulls: int,
    duplicate_count: int,
    schema_errors: int,
    rule_failures: int,
    weights: dict | None = None,
) -> float:
    """
    Combine null rate, duplicate rate, schema errors, and rule failures
    into a single 0-1 Data Quality Score. Weights are configurable via
    config/config.yaml rather than hardcoded.
    """
    weights = weights or {
        "completeness": 0.3,
        "uniqueness": 0.3,
        "schema": 0.2,
        "rules": 0.2,
    }

    completeness_score = 1 - (total_nulls / max(total_records, 1))
    uniqueness_score = 1 - (duplicate_count / max(total_records, 1))
    schema_score = 1 - min(schema_errors / 10, 1)  # capped penalty
    rule_score = 1 - (rule_failures / max(total_records, 1))

    return round(
        completeness_score * weights["completeness"]
        + uniqueness_score * weights["uniqueness"]
        + schema_score * weights["schema"]
        + rule_score * weights["rules"],
        4,
    )

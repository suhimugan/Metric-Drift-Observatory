"""
test_profiling.py

Minimal unit test skeleton for src/profiling.py. Run with:
    pytest tests/

Note: full tests require a local SparkSession (pyspark installed) —
these focus on the pure-Python scoring logic that doesn't need Spark,
plus a template for the Spark-dependent tests.
"""

from src.profiling import calculate_quality_score, BUSINESS_RULES


def test_calculate_quality_score_perfect_data():
    score = calculate_quality_score(
        total_records=1000,
        total_nulls=0,
        duplicate_count=0,
        schema_errors=0,
        rule_failures=0,
    )
    assert score == 1.0


def test_calculate_quality_score_penalizes_nulls():
    clean = calculate_quality_score(1000, 0, 0, 0, 0)
    with_nulls = calculate_quality_score(1000, 200, 0, 0, 0)
    assert with_nulls < clean


def test_business_rules_defined():
    # Guard against accidentally deleting a rule during refactors
    expected_rules = {
        "quantity_positive",
        "unit_price_positive",
        "total_sales_positive",
        "profit_margin_bounds",
        "delivery_days_non_negative",
        "discount_bounds",
        "return_flag_domain",
    }
    assert expected_rules.issubset(BUSINESS_RULES.keys())


# --- Spark-dependent test template -----------------------------------
# Uncomment and adapt once a local SparkSession fixture is set up
# (e.g. via a conftest.py `spark` fixture using pyspark.sql.SparkSession
# .builder.master("local[1]").getOrCreate()).
#
# def test_null_profile(spark):
#     df = spark.createDataFrame([(1, None), (2, "x")], ["id", "val"])
#     result = null_profile(df, ["id", "val"])
#     assert result["val"] == 1

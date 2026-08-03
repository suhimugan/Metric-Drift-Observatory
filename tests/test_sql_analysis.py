"""
test_sql_analysis.py

Unit tests for src/sql_analysis.py using the two real SQL versions
shipped in sql/. These don't require Spark, only sqlglot.
"""

import sqlglot

from src.sql_analysis import (
    extract_sql_metadata,
    compare_component,
    calculate_similarity,
    calculate_sql_risk,
)

with open("sql/customer_revenue_v1.sql") as f:
    SQL_V1 = f.read()

with open("sql/customer_revenue_v2.sql") as f:
    SQL_V2 = f.read()


def test_parses_both_versions():
    ast_v1 = sqlglot.parse_one(SQL_V1)
    ast_v2 = sqlglot.parse_one(SQL_V2)
    assert ast_v1 is not None
    assert ast_v2 is not None


def test_metadata_extraction_detects_join_change():
    ast_v1 = sqlglot.parse_one(SQL_V1)
    ast_v2 = sqlglot.parse_one(SQL_V2)
    meta1 = extract_sql_metadata(ast_v1)
    meta2 = extract_sql_metadata(ast_v2)

    join_diff = compare_component(meta1["joins"], meta2["joins"])
    # v1 -> v2 changes the customers join from INNER to LEFT
    assert join_diff["added"] or join_diff["removed"]


def test_similarity_score_between_zero_and_one():
    ast_v1 = sqlglot.parse_one(SQL_V1)
    ast_v2 = sqlglot.parse_one(SQL_V2)
    meta1 = extract_sql_metadata(ast_v1)
    meta2 = extract_sql_metadata(ast_v2)

    score = calculate_similarity(meta1, meta2)
    assert 0.0 <= score <= 1.0


def test_risk_score_flags_findings():
    ast_v1 = sqlglot.parse_one(SQL_V1)
    ast_v2 = sqlglot.parse_one(SQL_V2)
    meta1 = extract_sql_metadata(ast_v1)
    meta2 = extract_sql_metadata(ast_v2)

    diff = {
        key: compare_component(meta1[key], meta2[key]) for key in meta1
    }
    findings, risk_score = calculate_sql_risk(diff)
    assert isinstance(findings, list)
    assert 0.0 <= risk_score <= 1.0

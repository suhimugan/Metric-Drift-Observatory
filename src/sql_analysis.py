"""
sql_analysis.py

Reusable SQL semantic drift functions (refactored from
notebooks/04_sql_metric_drift_detection.ipynb) using sqlglot to parse
and diff two versions of a query.
"""

import sqlglot
from sqlglot import exp


def read_sql_file(path: str) -> str:
    """Read a .sql file (works for both local paths and Databricks Volumes)."""
    with open(path, "r") as f:
        return f.read()


def extract_sql_metadata(ast: exp.Expression) -> dict:
    """
    Extract structural metadata from a parsed SQL AST: joins, filter
    predicates, group-by columns, and aggregation functions.
    """
    joins = [
        {
            "type": j.args.get("kind", "INNER"),
            "table": j.this.sql() if j.this else None,
        }
        for j in ast.find_all(exp.Join)
    ]

    filters = [w.this.sql() for w in ast.find_all(exp.Where)]

    group_by_cols = [
        g.sql() for g in ast.find_all(exp.Group) for g in g.expressions
    ]

    aggregations = sorted(
        {f.sql_name().upper() for f in ast.find_all(exp.AggFunc)}
    )

    return {
        "joins": joins,
        "filters": filters,
        "group_by": group_by_cols,
        "aggregations": aggregations,
    }


def compare_component(old: list, new: list) -> dict:
    """Generic diff between two lists of AST-extracted components."""
    old_set, new_set = set(map(str, old)), set(map(str, new))
    return {
        "added": sorted(new_set - old_set),
        "removed": sorted(old_set - new_set),
        "unchanged": sorted(old_set & new_set),
    }


def calculate_similarity(metadata1: dict, metadata2: dict) -> float:
    """
    Jaccard-style similarity across all extracted SQL components,
    0 (completely different) to 1 (structurally identical).
    """
    total_overlap, total_union = 0, 0
    for key in metadata1:
        a, b = set(map(str, metadata1[key])), set(map(str, metadata2[key]))
        total_overlap += len(a & b)
        total_union += len(a | b) or 1
    return round(total_overlap / total_union, 4) if total_union else 1.0


# Higher-risk component changes are weighted more heavily than lower-risk ones.
RISK_WEIGHTS = {
    "joins": 0.35,
    "aggregations": 0.30,
    "filters": 0.20,
    "group_by": 0.15,
}


def calculate_sql_risk(diff: dict) -> tuple[list[str], float]:
    """
    Convert a component-level diff into human-readable findings and a
    single risk score (0 = no risk, 1 = high risk).
    """
    findings = []
    risk_score = 0.0

    for component, weight in RISK_WEIGHTS.items():
        changes = diff.get(component, {})
        changed = bool(changes.get("added") or changes.get("removed"))
        if changed:
            risk_score += weight
            findings.append(
                f"{component} changed: +{changes.get('added')} / -{changes.get('removed')}"
            )

    return findings, round(min(risk_score, 1.0), 4)

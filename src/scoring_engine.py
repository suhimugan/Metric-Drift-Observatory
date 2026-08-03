"""
scoring_engine.py

Reusable functions for the Unified Reliability Score Engine
(refactored from notebooks/05_unified_reliability_score_engine.ipynb).
"""

# Health status bands are config-driven so thresholds can be tuned
# without touching code — see config/config.example.yaml.
DEFAULT_HEALTH_BANDS = [
    (0.85, "Healthy"),
    (0.65, "Watch"),
    (0.0, "At Risk"),
]

DEFAULT_WEIGHTS = {
    "data_quality": 0.4,
    "metric_stability": 0.35,
    "sql_stability": 0.25,
}


def calculate_reliability_score(
    data_quality_score: float,
    metric_stability_score: float,
    sql_stability_score: float,
    weights: dict | None = None,
) -> float:
    """
    Combine the three independent reliability signals into a single
    weighted Reliability Score (0-1).
    """
    weights = weights or DEFAULT_WEIGHTS
    score = (
        data_quality_score * weights["data_quality"]
        + metric_stability_score * weights["metric_stability"]
        + sql_stability_score * weights["sql_stability"]
    )
    return round(score, 4)


def get_health_status(score: float, bands: list[tuple[float, str]] = DEFAULT_HEALTH_BANDS) -> str:
    """Map a Reliability Score to a health status label."""
    for threshold, label in bands:
        if score >= threshold:
            return label
    return bands[-1][1]


def generate_explanation(
    data_quality_score: float,
    metric_stability_score: float,
    sql_stability_score: float,
) -> str:
    """
    Produce a short, human-readable explanation of what's driving the
    Reliability Score — the weakest component is called out explicitly
    so the dashboard reader knows where to look first.
    """
    components = {
        "data quality": data_quality_score,
        "metric stability": metric_stability_score,
        "SQL stability": sql_stability_score,
    }
    weakest = min(components, key=components.get)
    return (
        f"Reliability driven primarily by {weakest} "
        f"(score: {components[weakest]:.2f}). "
        f"Component scores — quality: {data_quality_score:.2f}, "
        f"metric stability: {metric_stability_score:.2f}, "
        f"SQL stability: {sql_stability_score:.2f}."
    )

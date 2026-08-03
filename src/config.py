"""
config.py

Centralized configuration loader so no notebook or module hardcodes
storage account names, container names, table names, or thresholds.

Usage:
    from config import load_config
    cfg = load_config()
    cfg["storage_account"]
    cfg["paths"]["silver"]
    cfg["quality_thresholds"]["min_score"]
"""

import os
import yaml

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "config", "config.yaml"
)


def load_config(path: str = DEFAULT_CONFIG_PATH) -> dict:
    """
    Load pipeline configuration from YAML.

    In Databricks, secrets (storage keys, service principal credentials)
    should NOT live in this file — they should be pulled at runtime via
    dbutils.secrets.get(scope=..., key=...) backed by Azure Key Vault.
    This file holds only non-secret configuration: account/container
    NAMES, table names, and tunable thresholds.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Config file not found at {path}. "
            f"Copy config/config.example.yaml to config/config.yaml and fill it in."
        )
    with open(path, "r") as f:
        return yaml.safe_load(f)

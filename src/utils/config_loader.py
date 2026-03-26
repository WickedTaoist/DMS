from pathlib import Path
from typing import Any, Dict

import yaml

from src.utils.path_utils import resolve_project_path


def load_yaml(path: str) -> Dict[str, Any]:
    with resolve_project_path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(config_path: str) -> Dict[str, Any]:
    resolved_config = resolve_project_path(config_path)
    cfg = load_yaml(str(resolved_config))
    parent = cfg.get("inherits")
    if not parent:
        return cfg
    parent_path = Path(parent)
    if not parent_path.is_absolute():
        parent_path = resolved_config.parent / parent_path
    base = load_yaml(str(parent_path))
    return deep_merge(base, cfg)

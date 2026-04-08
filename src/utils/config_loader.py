"""
配置加载模块 / Configuration loading helpers.

本模块负责：
1. 读取 YAML 配置
2. 处理实验配置继承
3. 递归合并父子配置

This module is responsible for:
1. Loading YAML config files
2. Handling experiment config inheritance
3. Recursively merging parent and child configs
"""

from pathlib import Path
from typing import Any, Dict

import yaml

from src.utils.path_utils import resolve_project_path


def load_yaml(path: str) -> Dict[str, Any]:
    """
    读取单个 YAML 文件 / Load a single YAML file.

    Args:
        path: YAML 文件路径，可以是相对路径或绝对路径。

    Returns:
        解析后的字典；若文件为空，则返回空字典。
        Parsed dictionary; returns an empty dict for empty files.
    """
    # 统一先做项目相对路径解析，保证不同入口行为一致。
    # Resolve project-relative paths first for consistent behavior across runners.
    with resolve_project_path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    递归合并两个配置字典 / Recursively merge two config dictionaries.

    子配置中的值会覆盖父配置中的值；
    若同一键下仍然是字典，则继续递归合并。

    Child config values override parent values.
    If both values are dictionaries, merge them recursively.
    """
    # 先复制父配置，避免原地修改。
    # Copy the base config first to avoid in-place mutation.
    result = dict(base)

    # 逐项遍历子配置并进行覆盖或递归合并。
    # Iterate over override items and either replace or merge them.
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(config_path: str) -> Dict[str, Any]:
    """
    加载最终实验配置 / Load the final merged experiment config.

    支持 `inherits` 字段，用于在实验配置中继承基础配置。

    Supports the `inherits` field so experiment configs can inherit
    from a shared base configuration.
    """
    # 先解析当前配置文件的绝对路径。
    # Resolve the absolute path of the current config file first.
    resolved_config = resolve_project_path(config_path)

    # 读取当前配置文件内容。
    # Load the current config content.
    cfg = load_yaml(str(resolved_config))

    # 若未声明父配置，则当前配置就是最终配置。
    # If there is no parent config, the current config is final.
    parent = cfg.get("inherits")
    if not parent:
        return cfg

    # 解析父配置路径：支持绝对路径，也支持相对于当前配置文件的相对路径。
    # Resolve parent config path: support both absolute paths and paths
    # relative to the current config file.
    parent_path = Path(parent)
    if not parent_path.is_absolute():
        parent_path = resolved_config.parent / parent_path

    # 读取父配置，并与当前配置递归合并。
    # Load the parent config and recursively merge it with the current config.
    base = load_yaml(str(parent_path))
    return deep_merge(base, cfg)

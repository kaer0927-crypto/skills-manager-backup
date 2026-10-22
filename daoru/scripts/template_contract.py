"""Shared constants and helpers for the generic Excel import template."""

from __future__ import annotations

from pathlib import Path
from typing import Any

# 字体
FONT_NAME = "等线"

# 必填星号颜色
REQUIRED_STAR_COLOR = "FFFF0000"

# 填充（RGB，aRGB 完整写法）
TITLE_FILL = "FFF7F8FA"
MODULE_FILL = "FFF7F8FA"
FIELD_FILL = "FFF2F3F5"

# 文字颜色
TEXT_COLOR = "FF1D2129"
LOGIC_COLOR = "FF86909C"

# 边框细线
BORDER_COLOR = "FFD9D9D9"

# 行高（磅）
ROW_HEIGHTS = {1: 78.0, 2: 26.0, 3: 24.0, 4: 84.0}
DATA_ROW_HEIGHT = 30.0

# 默认列宽
DEFAULT_COLUMN_WIDTH = 20.0

# 默认空白数据行
DEFAULT_DATA_ROWS = 1000

# 默认工作表名
DEFAULT_SHEET_NAME = "导入模板"

# 默认第 1 行说明
DEFAULT_TITLE = "填写说明：请根据字段逻辑说明逐列填写，必填字段以红色 * 标注；表头已冻结，请勿自行删除或改动。"

# 冻结窗格
FREEZE_PANE = "A5"


def flatten_fields(modules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """把所有模块内的字段展开成一个有序列表。"""
    flat: list[dict[str, Any]] = []
    for module in modules:
        for field in module.get("fields", []):
            flat.append(field)
    return flat


def column_letter(index: int) -> str:
    """1-based 列号转列字母，避免依赖 openpyxl 循环导入。"""
    letters = ""
    while index > 0:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def has_module_names(modules: list[dict[str, Any]]) -> bool:
    """是否含非空模块名。全为空串视为无模块划分。"""
    return any((module.get("name") or "").strip() for module in modules)

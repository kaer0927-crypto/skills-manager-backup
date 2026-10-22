#!/usr/bin/env python3
"""Generate a generic Excel import template from a field definition JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from template_contract import (
    BORDER_COLOR,
    DATA_ROW_HEIGHT,
    DEFAULT_COLUMN_WIDTH,
    DEFAULT_DATA_ROWS,
    DEFAULT_SHEET_NAME,
    DEFAULT_TITLE,
    FIELD_FILL,
    FONT_NAME,
    FREEZE_PANE,
    LOGIC_COLOR,
    MODULE_FILL,
    REQUIRED_STAR_COLOR,
    ROW_HEIGHTS,
    TEXT_COLOR,
    TITLE_FILL,
    column_letter,
    has_module_names,
)


def load_fields(path: Path) -> dict:
    spec = json.loads(path.read_text(encoding="utf-8"))
    if not spec.get("modules"):
        raise ValueError("fields.json 必须包含 modules 字段与至少一个模块")
    return spec


def build_styles() -> dict:
    thin = Side(style="thin", color=BORDER_COLOR)
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    title_font = Font(name=FONT_NAME, size=11, bold=True, color=TEXT_COLOR)
    module_font = Font(name=FONT_NAME, size=11, bold=True, color=TEXT_COLOR)
    field_font = Font(name=FONT_NAME, size=11, bold=True, color=TEXT_COLOR)
    logic_font = Font(name=FONT_NAME, size=9, color=LOGIC_COLOR)

    title_fill = PatternFill(fill_type="solid", fgColor=TITLE_FILL)
    module_fill = PatternFill(fill_type="solid", fgColor=MODULE_FILL)
    field_fill = PatternFill(fill_type="solid", fgColor=FIELD_FILL)

    title_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    module_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    field_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    logic_align = Alignment(horizontal="left", vertical="top", wrap_text=True)

    star_font = InlineFont(rFont=FONT_NAME, b=True, sz=11.0, color=REQUIRED_STAR_COLOR)
    base_inline = InlineFont(rFont=FONT_NAME, b=True, sz=11.0, color=TEXT_COLOR)

    return {
        "border": border,
        "title_font": title_font,
        "module_font": module_font,
        "field_font": field_font,
        "logic_font": logic_font,
        "title_fill": title_fill,
        "module_fill": module_fill,
        "field_fill": field_fill,
        "title_align": title_align,
        "module_align": module_align,
        "field_align": field_align,
        "logic_align": logic_align,
        "star_font": star_font,
        "base_inline": base_inline,
    }


def make_field_rich_text(name: str, required: bool, styles: dict) -> CellRichText:
    runs = [TextBlock(styles["base_inline"], name)]
    if required:
        runs.append(TextBlock(styles["base_inline"], " "))
        runs.append(TextBlock(styles["star_font"], "*"))
    return CellRichText(*runs)


def generate(spec: dict, output: Path, force: bool = False) -> None:
    output = output.expanduser().resolve()
    if output.suffix.lower() != ".xlsx":
        raise ValueError("输出文件必须使用 .xlsx 扩展名")
    if output.exists() and not force:
        raise FileExistsError(f"目标文件已存在：{output}\n如确认覆盖，请加 --force。")

    modules = spec["modules"]
    fields = []
    for module in modules:
        fields.extend(module.get("fields", []))
    if not fields:
        raise ValueError("字段清单为空，无法生成模板")

    last_col = len(fields)
    last_letter = get_column_letter(last_col)

    styles = build_styles()
    wb = Workbook()
    ws = wb.active
    ws.title = spec.get("sheet_name") or DEFAULT_SHEET_NAME

    # 第 1 行：说明（跨列合并）
    ws.merge_cells(f"A1:{last_letter}1")
    c = ws["A1"]
    c.value = spec.get("title") or DEFAULT_TITLE
    c.font = styles["title_font"]
    c.fill = styles["title_fill"]
    c.alignment = styles["title_align"]
    c.border = styles["border"]
    ws.row_dimensions[1].height = ROW_HEIGHTS[1]

    # 第 2 行：模块分组
    show_modules = has_module_names(modules)
    if show_modules:
        col = 1
        for module in modules:
            n = len(module.get("fields", []))
            if n == 0:
                continue
            end = col + n - 1
            ws.merge_cells(f"{get_column_letter(col)}2:{get_column_letter(end)}2")
            cell = ws.cell(2, col)
            cell.value = module.get("name") or ""
            cell.font = styles["module_font"]
            cell.fill = styles["module_fill"]
            cell.alignment = styles["module_align"]
            cell.border = styles["border"]
            col = end + 1
    else:
        # 无模块：整行单一说明合并
        ws.merge_cells(f"A2:{last_letter}2")
        cell = ws["A2"]
        cell.value = spec.get("module_title") or ""
        cell.font = styles["module_font"]
        cell.fill = styles["module_fill"]
        cell.alignment = styles["module_align"]
        cell.border = styles["border"]
    ws.row_dimensions[2].height = ROW_HEIGHTS[2]

    # 第 3 行：字段名；第 4 行：字段逻辑
    for idx, field in enumerate(fields):
        col = idx + 1
        letter = get_column_letter(col)
        name = str(field.get("name", ""))
        required = bool(field.get("required", False))

        fcell = ws.cell(3, col)
        fcell.value = make_field_rich_text(name, required, styles)
        fcell.font = styles["field_font"]
        fcell.fill = styles["field_fill"]
        fcell.alignment = styles["field_align"]
        fcell.border = styles["border"]

        lcell = ws.cell(4, col)
        lcell.value = str(field.get("logic", ""))
        lcell.font = styles["logic_font"]
        lcell.alignment = styles["logic_align"]
        lcell.border = styles["border"]

        width = field.get("width") or DEFAULT_COLUMN_WIDTH
        ws.column_dimensions[letter].width = width

    ws.row_dimensions[3].height = ROW_HEIGHTS[3]
    ws.row_dimensions[4].height = ROW_HEIGHTS[4]

    # 第 5 行起：空白数据区
    data_rows = int(spec.get("data_rows") or DEFAULT_DATA_ROWS)
    for r in range(5, 5 + data_rows):
        ws.row_dimensions[r].height = DATA_ROW_HEIGHT

    # 表头边框补齐第 1-4 行空列（如有）
    for r in range(1, 5):
        for col in range(1, last_col + 1):
            ws.cell(r, col).border = styles["border"]

    ws.freeze_panes = FREEZE_PANE
    ws.sheet_view.showGridLines = True

    output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output)
    print(f"已生成：{output}")
    print(f"大小：{output.stat().st_size} bytes")
    print(f"字段数：{last_col}  模块数：{len([m for m in modules if m.get('fields')])}  数据行：{data_rows}")


def main() -> int:
    parser = argparse.ArgumentParser(description="依据字段定义生成通用 Excel 导入模板")
    parser.add_argument("--fields", type=Path, required=True, help="fields.json 路径")
    parser.add_argument("--output", type=Path, default=Path.cwd() / "导入模板.xlsx", help="输出 XLSX 路径")
    parser.add_argument("--force", action="store_true", help="目标文件已存在时覆盖")
    args = parser.parse_args()

    try:
        spec = load_fields(args.fields)
        generate(spec, args.output, args.force)
    except (FileExistsError, ValueError, json.JSONDecodeError) as exc:
        print(f"生成失败：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

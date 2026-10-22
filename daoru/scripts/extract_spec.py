#!/usr/bin/env python3
"""Re-export a field definition JSON from an existing import template (optional helper)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.utils import get_column_letter


def main() -> int:
    parser = argparse.ArgumentParser(description="从已生成的导入模板反推字段定义 JSON")
    parser.add_argument("workbook", type=Path, help="XLSX 模板路径")
    parser.add_argument("--output", type=Path, default=Path.cwd() / "fields.json")
    args = parser.parse_args()

    workbook = load_workbook(args.workbook, rich_text=True)
    if len(workbook.sheetnames) != 1:
        print("仅支持单工作表模板", file=sys.stderr)
        return 1
    sheet = workbook[workbook.sheetnames[0]]

    modules: list[dict] = []
    for row in sheet.merged_cells.ranges:
        if row.min_row != 2:
            continue
        name = sheet.cell(2, row.min_col).value or ""
        current = {"name": name, "fields": []}
        for col in range(row.min_col, row.max_col + 1):
            current["fields"].append(_read_field(sheet, col))
        modules.append(current)

    spec = {
        "title": sheet["A1"].value,
        "sheet_name": sheet.title,
        "data_rows": _count_data_rows(sheet),
        "modules": modules,
    }
    args.output.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已导出：{args.output}")
    return 0


def _count_data_rows(sheet) -> int:
    """从行 5 起，统计连续设置了行高的空白数据行数量。"""
    count = 0
    for r in range(5, 2000):
        if sheet.row_dimensions[r].height:
            count += 1
        else:
            break
    return count or 1000


def _read_field(sheet, column: int) -> dict:
    cell = sheet.cell(3, column)
    name = ""
    required = False
    if isinstance(cell.value, CellRichText):
        for run in cell.value:
            if isinstance(run, TextBlock) and run.text == "*":
                required = True
            elif isinstance(run, TextBlock):
                name += run.text
    else:
        name = str(cell.value or "")
    return {"name": name.strip(), "required": required, "logic": str(sheet.cell(4, column).value or "")}


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate a generated import template against the field definition spec."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.utils import get_column_letter

from template_contract import (
    DATA_ROW_HEIGHT,
    DEFAULT_COLUMN_WIDTH,
    DEFAULT_DATA_ROWS,
    DEFAULT_SHEET_NAME,
    FREEZE_PANE,
    LOGIC_COLOR,
    REQUIRED_STAR_COLOR,
    ROW_HEIGHTS,
    has_module_names,
)


class Validation:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.checks = 0

    def check(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.failures.append(message)


def flatten(spec: dict) -> list[dict]:
    flat: list[dict] = []
    for module in spec.get("modules", []):
        for field in module.get("fields", []):
            flat.append(field)
    return flat


def float_equal(a: float | None, b: float | None) -> bool:
    if a is None or b is None:
        return a is b
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-6)


def validate(candidate: Path, spec: dict) -> Validation:
    v = Validation()
    candidate = candidate.expanduser().resolve()
    v.check(candidate.is_file(), f"文件不存在：{candidate}")
    try:
        wb = load_workbook(candidate, rich_text=True)
    except Exception as exc:  # noqa: BLE001
        v.failures.append(f"无法读取工作簿：{exc}")
        return v

    sheet_name = spec.get("sheet_name") or DEFAULT_SHEET_NAME
    v.check(wb.sheetnames == [sheet_name], f"工作表名应为 [{sheet_name}]，实际 {wb.sheetnames}")
    if v.failures:
        return v
    ws = wb[sheet_name]

    fields = flatten(spec)
    n = len(fields)
    v.check(n > 0, "字段清单为空")
    if n == 0:
        return v

    last_letter = get_column_letter(n)

    # 冻结窗格
    v.check(ws.freeze_panes == FREEZE_PANE, f"冻结窗格应为 {FREEZE_PANE}，实际 {ws.freeze_panes}")

    # 第 1 行说明合并
    merged_row1 = [str(m) for m in ws.merged_cells.ranges if m.min_row == 1 and m.max_row == 1]
    v.check(merged_row1 == [f"A1:{last_letter}1"], f"第 1 行应合并为 A1:{last_letter}1，实际 {merged_row1}")
    v.check(ws.cell(1, 1).value is not None, "第 1 行说明不得为空")
    v.check(float_equal(ws.row_dimensions[1].height, ROW_HEIGHTS[1]), "第 1 行行高应一致")

    # 第 2 行模块合并
    show_modules = has_module_names(spec.get("modules", []))
    merged_row2 = sorted(
        [str(m) for m in ws.merged_cells.ranges if m.min_row == 2 and m.max_row == 2]
    )
    if show_modules:
        expected: list[str] = []
        col = 1
        for module in spec["modules"]:
            cnt = len(module.get("fields", []))
            if cnt == 0:
                continue
            end = col + cnt - 1
            expected.append(f"{get_column_letter(col)}2:{get_column_letter(end)}2")
            col = end + 1
        v.check(merged_row2 == expected, f"第 2 行模块合并应 {expected}，实际 {merged_row2}")
        # 模块名文本
        col = 1
        for module in spec["modules"]:
            cnt = len(module.get("fields", []))
            if cnt == 0:
                continue
            v.check(ws.cell(2, col).value == (module.get("name") or ""), "模块名文本应一致")
            col += cnt
    else:
        v.check(merged_row2 == [f"A2:{last_letter}2"], f"无模块时第 2 行应合并为 A2:{last_letter}2，实际 {merged_row2}")
    v.check(float_equal(ws.row_dimensions[2].height, ROW_HEIGHTS[2]), "第 2 行行高应一致")

    # 第 3 行字段名 + 必填星号；第 4 行逻辑
    for idx, field in enumerate(fields):
        col = idx + 1
        letter = get_column_letter(col)
        name = str(field.get("name", ""))
        required = bool(field.get("required", False))
        logic = str(field.get("logic", ""))

        cell3 = ws.cell(3, col)
        has_star = False
        if isinstance(cell3.value, CellRichText):
            text = "".join(b.text for b in cell3.value if isinstance(b, TextBlock))
            # 去掉尾部 * 与空格后应与字段名一致
            plain = text.rstrip().rstrip("*").rstrip()
            v.check(plain == name, f"{letter}3 字段名应为 {name!r}，实际 {plain!r}")
            has_star = any(
                isinstance(b, TextBlock) and b.text == "*"
                and b.font is not None
                and b.font.color is not None
                and b.font.color.rgb == REQUIRED_STAR_COLOR
                for b in cell3.value
            )
        else:
            v.check(str(cell3.value) == name, f"{letter}3 字段名应为 {name!r}，实际 {cell3.value!r}")
        if required:
            v.check(has_star, f"{letter}3 必填字段缺少红色 *")
        else:
            v.check(not has_star, f"{letter}3 非必填字段不应有 *")

        cell4 = ws.cell(4, col)
        v.check(cell4.value == logic, f"{letter}4 逻辑说明应一致")
        v.check(cell4.font.size == 9, f"{letter}4 字号应为 9")
        v.check(
            cell4.font.color is not None and cell4.font.color.rgb == LOGIC_COLOR,
            f"{letter}4 文字颜色应为 {LOGIC_COLOR}",
        )

        # 列宽
        width = field.get("width") or DEFAULT_COLUMN_WIDTH
        v.check(
            float_equal(ws.column_dimensions[letter].width, width),
            f"{letter} 列宽应一致",
        )

    # 第 3/4 行高
    v.check(float_equal(ws.row_dimensions[3].height, ROW_HEIGHTS[3]), "第 3 行行高应一致")
    v.check(float_equal(ws.row_dimensions[4].height, ROW_HEIGHTS[4]), "第 4 行行高应一致")

    # 空白数据区
    data_rows = int(spec.get("data_rows") or DEFAULT_DATA_ROWS)
    data_cells = [co for co in ws._cells if 5 <= co[0] <= 4 + data_rows]
    v.check(data_cells == [], "第 5 行起空白数据区不得包含数据单元格")
    v.check(float_equal(ws.row_dimensions[5].height, DATA_ROW_HEIGHT), "第 5 行数据行高应一致")

    # 禁止能力
    v.check(len(ws.data_validations.dataValidation) == 0, "不得包含数据验证/下拉")
    v.check(ws.auto_filter.ref is None, "不得包含自动筛选")
    v.check(len(ws.tables) == 0, "不得包含表格对象")
    v.check(len(ws.conditional_formatting) == 0, "不得包含条件格式")
    v.check(str(ws.print_area or "") == "", "不得包含打印区域")
    return v


def main() -> int:
    parser = argparse.ArgumentParser(description="校验导入模板结构与样式是否走样")
    parser.add_argument("candidate", type=Path, help="待校验 XLSX 文件")
    parser.add_argument("--spec", type=Path, required=True, help="fields.json 规范路径")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    result = validate(args.candidate, spec)
    if result.failures:
        print(f"校验失败：{len(result.failures)} 项不一致（共 {result.checks} 项检查）")
        for failure in result.failures[:100]:
            print(f"- {failure}")
        if len(result.failures) > 100:
            print(f"- 其余 {len(result.failures) - 100} 项未显示")
        return 1
    print(f"校验通过：{result.checks} 项检查全部一致")
    print(f"文件：{args.candidate.expanduser().resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Regenerate references/template-spec.md from the golden workbook."""

from __future__ import annotations

import argparse
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.utils import get_column_letter

from template_contract import (
    COLUMN_COUNT,
    EXPECTED_DIMENSION,
    FIRST_DATA_ROW,
    GOLDEN_SHA256,
    GOLDEN_TEMPLATE,
    LAST_PREFORMATTED_ROW,
    SHEET_NAME,
    SKILL_DIR,
    sha256_file,
)


def required_columns(sheet) -> list[str]:
    required: list[str] = []
    for column in range(1, COLUMN_COUNT + 1):
        cell = sheet.cell(3, column)
        if isinstance(cell.value, CellRichText):
            red_star = any(
                isinstance(run, TextBlock)
                and run.text == "*"
                and run.font.color is not None
                and run.font.color.rgb == "FFFF0000"
                for run in cell.value
            )
            if red_star:
                required.append(get_column_letter(column))
    return required


def header_label(cell) -> str:
    if isinstance(cell.value, CellRichText):
        return "".join(
            run.text if isinstance(run, TextBlock) else str(run) for run in cell.value
        ).replace(" *", "")
    return str(cell.value or "")


def format_number(value: float) -> str:
    return format(value, ".15g")


def build_markdown(sheet, source_hash: str, source_size: int) -> str:
    required = required_columns(sheet)
    required_set = set(required)
    widths = {
        get_column_letter(column): sheet.column_dimensions[get_column_letter(column)].width
        for column in range(1, COLUMN_COUNT + 1)
    }
    merged = sorted(str(item) for item in sheet.merged_cells.ranges)
    groups = [
        ("A2:J2", sheet["A2"].value),
        ("K2:N2", sheet["K2"].value),
        ("O2:AD2", sheet["O2"].value),
        ("AE2:AI2", sheet["AE2"].value),
    ]

    lines = [
        "# 兰州公物仓资产批量导入模板规范",
        "",
        "> 本文件由 `scripts/extract_spec.py` 从黄金母版自动生成，请勿手工改字段表。",
        "",
        "## 1. 母版",
        "",
        "| 项目 | 值 |",
        "|---|---|",
        f"| 文件 | `assets/兰州公物仓_资产批量导入模板.xlsx` |",
        f"| 大小 | {source_size:,} bytes |",
        f"| SHA-256 | `{source_hash}` |",
        f"| 工作表 | `{SHEET_NAME}` |",
        f"| 列范围 | `A:AI`，共 {COLUMN_COUNT} 列 |",
        f"| XML 使用范围 | `{EXPECTED_DIMENSION}` |",
        f"| 数据起始行 | 第 {FIRST_DATA_ROW} 行 |",
        f"| 预格式化空白数据行 | 第 {FIRST_DATA_ROW} 至 {LAST_PREFORMATTED_ROW} 行，共 {LAST_PREFORMATTED_ROW - FIRST_DATA_ROW + 1:,} 行 |",
        "",
        "母版是唯一格式依据。生成器必须复制母版，不得用代码重新拼装样式。",
        "",
        "## 2. 表头与合并单元格",
        "",
        "| 行 | 内容 | 合并范围 |",
        "|---|---|---|",
        f"| 1 | 填写说明 | `A1:AI1` |",
    ]
    for cell_range, label in groups:
        lines.append(f"| 2 | {label} | `{cell_range}` |")
    lines += [
        "| 3 | 字段列名 | 无 |",
        "| 4 | 填写要求 | 无 |",
        "",
        f"冻结窗格为 `{sheet.freeze_panes}`。工作表视图左上单元格为 `{sheet.sheet_view.topLeftCell}`，底部窗格活动单元格为 `{sheet.sheet_view.selection[1].activeCell}`。",
        "",
        "## 3. 行高与列宽",
        "",
        "### 行高",
        "",
        "| 行 | 行高 |",
        "|---|---:|",
    ]
    for row in range(1, 5):
        lines.append(f"| {row} | {sheet.row_dimensions[row].height:g} |")
    lines += [
        f"| {FIRST_DATA_ROW} 至 {LAST_PREFORMATTED_ROW} | {sheet.row_dimensions[FIRST_DATA_ROW].height:g} |",
        "",
        "### 列宽",
        "",
        "| 列 | 宽度 | 列 | 宽度 | 列 | 宽度 | 列 | 宽度 | 列 | 宽度 |",
        "|---|---:|---|---:|---|---:|---|---:|---|---:|",
    ]
    letters = [get_column_letter(column) for column in range(1, COLUMN_COUNT + 1)]
    for start in range(0, len(letters), 5):
        chunk = letters[start : start + 5]
        cells = [f"{letter} | {format_number(widths[letter])}" for letter in chunk]
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        "## 4. 视觉 Token",
        "",
        "| 区域 | 字体 | 字号 | 字重 | 颜色 | 填充 | 对齐 | 边框 |",
        "|---|---|---:|---|---|---|---|---|",
        "| A1 填写说明 | 等线 | 11 | 粗体 | `FF1D2129` | `FFF7F8FA` | 左对齐、垂直居中、自动换行 | 细线 `FFD9D9D9` |",
        "| 第 2 行分组标题 | 等线 | 11 | 粗体 | 默认 | `FFF7F8FA` | 水平/垂直居中 | 细线 |",
        "| 第 3 行字段列名 | 等线 | 11 | 粗体 | 默认 | `FFF2F3F5` | 水平/垂直居中、自动换行 | 细线 |",
        "| 第 4 行填写要求 | 等线 | 9 | 常规 | `FF86909C` | 无 | 左对齐、垂直靠上、自动换行 | 细线 |",
        "| 必填星号 | 等线 | 11 | 粗体 | `FFFF0000` | 同字段列名 | 同字段列名 | 同字段列名 |",
        "",
        "第 3 行所有字段名必须为富文本。必填字段为“字段名 + 一个尾随空格”普通粗体片段，再接红色粗体 `*` 片段；非必填字段为单个粗体富文本片段。不得把第 3 行改成普通字符串。",
        "",
        "## 5. 字段与填写要求",
        "",
        "| 列 | 表头 | 必填 | 宽度 | 第 4 行填写要求 |",
        "|---|---|---|---:|---|",
    ]
    for column in range(1, COLUMN_COUNT + 1):
        letter = get_column_letter(column)
        label = header_label(sheet.cell(3, column))
        instruction = str(sheet.cell(4, column).value or "").replace("|", "\\|")
        lines.append(
            f"| {letter} | {label} | {'是' if letter in required_set else '否'} | "
            f"{format_number(widths[letter])} | {instruction} |"
        )
    lines += [
        "",
        f"必填列共 {len(required)} 个：{'、'.join(required)}。",
        "",
        "## 6. A1 填写说明",
        "",
        "```text",
        str(sheet["A1"].value),
        "```",
        "",
        "## 7. 必须保持为空的能力",
        "",
        "母版不包含以下内容，生成或修改后也不得出现：",
        "",
        "- Excel 数据验证或下拉控件",
        "- 自动筛选",
        "- 表格对象",
        "- 条件格式",
        "- 打印区域、打印标题或页眉页脚",
        "- 示例数据、公式或占位资产",
        "- 额外工作表",
        f"- 第 {FIRST_DATA_ROW} 至 {LAST_PREFORMATTED_ROW} 行的业务数据",
        "",
        "## 8. 校验器判定",
        "",
        "`scripts/validate_template.py` 会将候选文件与母版逐项比较，至少检查：",
        "",
        "- 工作表名和数量",
        f"- XML 使用范围 `{EXPECTED_DIMENSION}`",
        "- 合并单元格范围",
        "- 列宽、行高、隐藏状态和自定义尺寸",
        "- 冻结窗格、视图位置和活动单元格",
        "- A1、四组表头、35 个字段名和 35 条填写要求",
        "- 第 3 行富文本片段、字体、字号、字重和红色星号",
        "- A1:AI4 每个单元格的字体、填充、边框、对齐、数字格式和保护状态",
        f"- 第 {FIRST_DATA_ROW} 至 {LAST_PREFORMATTED_ROW} 行无数据",
        "- 无数据验证、筛选、表格对象、条件格式和打印区域",
        "",
        "任一项不一致即判定失败。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="从黄金母版重新生成模板规范")
    parser.add_argument(
        "--output",
        type=Path,
        default=SKILL_DIR / "references" / "template-spec.md",
    )
    args = parser.parse_args()

    if sha256_file(GOLDEN_TEMPLATE) != GOLDEN_SHA256:
        raise SystemExit("黄金母版 SHA-256 与契约不一致，拒绝生成规范")
    workbook = load_workbook(GOLDEN_TEMPLATE, rich_text=True)
    if workbook.sheetnames != [SHEET_NAME]:
        raise SystemExit("黄金母版工作表与契约不一致")
    markdown = build_markdown(
        workbook[SHEET_NAME], GOLDEN_SHA256, GOLDEN_TEMPLATE.stat().st_size
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    print(f"已生成：{args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

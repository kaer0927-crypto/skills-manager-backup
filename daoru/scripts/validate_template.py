#!/usr/bin/env python3
"""Validate the import workbook against the golden template and XML contract."""

from __future__ import annotations

import argparse
import math
import re
import zipfile
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.utils import get_column_letter

from template_contract import (
    COLUMN_COUNT,
    EXPECTED_DIMENSION,
    EXPECTED_MERGED_RANGES,
    FIRST_DATA_ROW,
    GOLDEN_SHA256,
    GOLDEN_TEMPLATE,
    LAST_PREFORMATTED_ROW,
    SHEET_NAME,
    sha256_file,
)


class Validation:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.checks = 0

    def check(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.failures.append(message)

    def equal(self, actual: Any, expected: Any, message: str) -> None:
        self.check(actual == expected, f"{message}：预期 {expected!r}，实际 {actual!r}")


def color_value(color: Any) -> dict[str, Any] | None:
    if color is None:
        return None
    return {
        "type": color.type,
        "rgb": color.rgb if isinstance(color.rgb, str) else None,
        "indexed": color.indexed,
        "auto": color.auto,
        "theme": color.theme,
        "tint": color.tint,
    }


def font_value(font: Any) -> dict[str, Any]:
    return {
        "name": font.name,
        "size": font.sz,
        "bold": font.b,
        "italic": font.i,
        "underline": font.u,
        "strike": font.strike,
        "outline": font.outline,
        "shadow": font.shadow,
        "vertAlign": font.vertAlign,
        "charset": font.charset,
        "family": font.family,
        "scheme": font.scheme,
        "color": color_value(font.color),
    }


def inline_font_value(font: Any) -> dict[str, Any]:
    return {
        "name": font.rFont,
        "size": font.sz,
        "bold": font.b,
        "italic": font.i,
        "underline": font.u,
        "strike": font.strike,
        "vertAlign": font.vertAlign,
        "color": color_value(font.color),
    }


def fill_value(fill: Any) -> dict[str, Any]:
    return {
        "type": fill.fill_type,
        "pattern": fill.patternType,
        "fgColor": color_value(fill.fgColor),
        "bgColor": color_value(fill.bgColor),
    }


def side_value(side: Any) -> dict[str, Any]:
    if side is None:
        return {"style": None, "color": None}
    return {"style": side.style, "color": color_value(side.color)}


def border_value(border: Any) -> dict[str, Any]:
    return {
        "left": side_value(border.left),
        "right": side_value(border.right),
        "top": side_value(border.top),
        "bottom": side_value(border.bottom),
        "diagonal": side_value(border.diagonal),
        "diagonalUp": border.diagonalUp,
        "diagonalDown": border.diagonalDown,
        "outline": border.outline,
        "vertical": side_value(border.vertical),
        "horizontal": side_value(border.horizontal),
        "start": side_value(border.start),
        "end": side_value(border.end),
    }


def alignment_value(alignment: Any) -> dict[str, Any]:
    return {
        "horizontal": alignment.horizontal,
        "vertical": alignment.vertical,
        "wrapText": alignment.wrap_text,
        "shrinkToFit": alignment.shrink_to_fit,
        "textRotation": alignment.text_rotation,
        "indent": alignment.indent,
        "relativeIndent": alignment.relativeIndent,
        "justifyLastLine": alignment.justifyLastLine,
        "readingOrder": alignment.readingOrder,
    }


def protection_value(protection: Any) -> dict[str, Any]:
    return {"locked": protection.locked, "hidden": protection.hidden}


def rich_text_value(value: Any) -> Any:
    if not isinstance(value, CellRichText):
        return value
    runs: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, TextBlock):
            runs.append({"text": item.text, "font": inline_font_value(item.font)})
        else:
            runs.append({"text": str(item), "plain": True})
    return {"richText": runs}


def cell_value(cell: Any) -> Any:
    return rich_text_value(cell.value)


def cell_style(cell: Any) -> dict[str, Any]:
    return {
        "value": cell_value(cell),
        "font": font_value(cell.font),
        "fill": fill_value(cell.fill),
        "border": border_value(cell.border),
        "alignment": alignment_value(cell.alignment),
        "numberFormat": cell.number_format,
        "protection": protection_value(cell.protection),
    }


def dimension_float_equal(actual: float | None, expected: float | None) -> bool:
    if actual is None or expected is None:
        return actual is expected
    return math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12)


def read_xml_dimension(path: Path, sheet_index: int = 1) -> str | None:
    member = f"xl/worksheets/sheet{sheet_index}.xml"
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read(member).decode("utf-8")
    except (KeyError, zipfile.BadZipFile, OSError):
        return None
    match = re.search(r'<dimension\s+ref="([^"]+)"', xml)
    return match.group(1) if match else None


def load_sheet(path: Path) -> Any:
    workbook = load_workbook(path, rich_text=True)
    if SHEET_NAME not in workbook.sheetnames:
        raise ValueError(f"缺少工作表：{SHEET_NAME}")
    return workbook, workbook[SHEET_NAME]


def compare_sheet_metadata(validation: Validation, actual: Any, expected: Any) -> None:
    validation.equal(actual.freeze_panes, expected.freeze_panes, "冻结窗格")
    validation.equal(actual.sheet_view.topLeftCell, expected.sheet_view.topLeftCell, "视图左上单元格")
    validation.equal(actual.sheet_view.showGridLines, expected.sheet_view.showGridLines, "网格线显示")
    validation.equal(actual.sheet_view.zoomScale, expected.sheet_view.zoomScale, "缩放比例")
    validation.equal(
        actual.sheet_format.defaultColWidth,
        expected.sheet_format.defaultColWidth,
        "默认列宽",
    )
    validation.equal(
        actual.sheet_format.defaultRowHeight,
        expected.sheet_format.defaultRowHeight,
        "默认行高",
    )

    expected_selection = [
        (item.pane, item.activeCell, str(item.sqref)) for item in expected.sheet_view.selection
    ]
    actual_selection = [
        (item.pane, item.activeCell, str(item.sqref)) for item in actual.sheet_view.selection
    ]
    validation.equal(actual_selection, expected_selection, "活动单元格与选择区域")

    validation.equal(
        sorted(str(item) for item in actual.merged_cells.ranges),
        sorted(str(item) for item in expected.merged_cells.ranges),
        "合并单元格",
    )
    validation.equal(
        tuple(sorted(str(item) for item in actual.merged_cells.ranges)),
        tuple(sorted(EXPECTED_MERGED_RANGES)),
        "合并单元格固定契约",
    )


def compare_dimensions(validation: Validation, actual: Any, expected: Any) -> None:
    for index in range(1, COLUMN_COUNT + 1):
        letter = get_column_letter(index)
        actual_dim = actual.column_dimensions[letter]
        expected_dim = expected.column_dimensions[letter]
        validation.check(
            dimension_float_equal(actual_dim.width, expected_dim.width),
            f"{letter} 列宽：预期 {expected_dim.width!r}，实际 {actual_dim.width!r}",
        )
        validation.equal(actual_dim.hidden, expected_dim.hidden, f"{letter} 列隐藏状态")
        validation.equal(
            actual_dim.customWidth, expected_dim.customWidth, f"{letter} 列自定义宽度"
        )

    for row in range(1, LAST_PREFORMATTED_ROW + 1):
        actual_dim = actual.row_dimensions[row]
        expected_dim = expected.row_dimensions[row]
        validation.check(
            dimension_float_equal(actual_dim.height, expected_dim.height),
            f"第 {row} 行行高：预期 {expected_dim.height!r}，实际 {actual_dim.height!r}",
        )
        validation.equal(actual_dim.hidden, expected_dim.hidden, f"第 {row} 行隐藏状态")
        validation.equal(
            actual_dim.customHeight, expected_dim.customHeight, f"第 {row} 行自定义高度"
        )


def compare_header_cells(validation: Validation, actual: Any, expected: Any) -> None:
    expected_cells = set(expected._cells)
    actual_cells = set(actual._cells)
    expected_header_cells = {
        coordinate for coordinate in expected_cells if coordinate[0] <= 4
    }
    actual_header_cells = {
        coordinate for coordinate in actual_cells if coordinate[0] <= 4
    }
    validation.equal(actual_header_cells, expected_header_cells, "前 4 行单元格集合")

    for row in range(1, 5):
        for column in range(1, COLUMN_COUNT + 1):
            coordinate = f"{get_column_letter(column)}{row}"
            if (column, row) not in expected_header_cells:
                continue
            actual_style = cell_style(actual[coordinate])
            expected_style = cell_style(expected[coordinate])
            validation.equal(
                actual_style, expected_style, f"{coordinate} 单元格内容与样式"
            )

    for column in range(1, COLUMN_COUNT + 1):
        coordinate = f"{get_column_letter(column)}3"
        validation.check(
            isinstance(actual[coordinate].value, CellRichText),
            f"{coordinate} 必须为富文本字段名",
        )


def compare_empty_data_rows(validation: Validation, actual: Any) -> None:
    data_cells = [
        coordinate
        for coordinate in actual._cells
        if FIRST_DATA_ROW <= coordinate[0] <= LAST_PREFORMATTED_ROW
    ]
    validation.equal(data_cells, [], "第 5 至 1113 行不得包含数据单元格")


def compare_forbidden_features(validation: Validation, sheet: Any) -> None:
    validation.equal(len(sheet.data_validations.dataValidation), 0, "不得包含数据验证/下拉")
    validation.equal(sheet.auto_filter.ref, None, "不得包含自动筛选")
    validation.equal(len(sheet.tables), 0, "不得包含表格对象")
    validation.equal(len(sheet.conditional_formatting), 0, "不得包含条件格式")
    validation.equal(str(sheet.print_area or ""), "", "不得包含打印区域")
    validation.equal(sheet.print_title_rows, None, "不得包含打印标题行")
    validation.equal(sheet.print_title_cols, None, "不得包含打印标题列")
    validation.equal(sheet.protection.sheet, False, "工作表保护状态")

    header_footer = sheet.oddHeader
    footer = sheet.oddFooter
    header_text = "".join(
        [
            header_footer.left.text or "",
            header_footer.center.text or "",
            header_footer.right.text or "",
        ]
    )
    footer_text = "".join(
        [
            footer.left.text or "",
            footer.center.text or "",
            footer.right.text or "",
        ]
    )
    validation.equal(header_text, "", "不得包含页眉")
    validation.equal(footer_text, "", "不得包含页脚")


def validate(candidate: Path, golden: Path = GOLDEN_TEMPLATE) -> Validation:
    validation = Validation()
    candidate = candidate.expanduser().resolve()
    golden = golden.expanduser().resolve()

    validation.check(candidate.is_file(), f"文件不存在：{candidate}")
    validation.check(golden.is_file(), f"黄金母版不存在：{golden}")
    if validation.failures:
        return validation

    golden_hash = sha256_file(golden)
    validation.equal(golden_hash, GOLDEN_SHA256, "黄金母版 SHA-256")
    try:
        actual_workbook, actual_sheet = load_sheet(candidate)
        expected_workbook, expected_sheet = load_sheet(golden)
    except Exception as exc:
        validation.failures.append(f"无法读取工作簿：{exc}")
        return validation

    validation.equal(actual_workbook.sheetnames, [SHEET_NAME], "工作表名称与数量")
    validation.equal(expected_workbook.sheetnames, [SHEET_NAME], "黄金母版工作表名称")
    validation.equal(read_xml_dimension(candidate), EXPECTED_DIMENSION, "XML 使用范围")
    validation.equal(read_xml_dimension(golden), EXPECTED_DIMENSION, "黄金母版 XML 使用范围")

    compare_sheet_metadata(validation, actual_sheet, expected_sheet)
    compare_dimensions(validation, actual_sheet, expected_sheet)
    compare_header_cells(validation, actual_sheet, expected_sheet)
    compare_empty_data_rows(validation, actual_sheet)
    compare_forbidden_features(validation, actual_sheet)
    return validation


def main() -> int:
    parser = argparse.ArgumentParser(
        description="校验兰州公物仓资产批量导入模板的结构与样式"
    )
    parser.add_argument("candidate", type=Path, help="待校验 XLSX 文件")
    parser.add_argument(
        "--golden",
        type=Path,
        default=GOLDEN_TEMPLATE,
        help="黄金母版路径，默认使用技能内置母版",
    )
    args = parser.parse_args()

    result = validate(args.candidate, args.golden)
    if result.failures:
        print(f"校验失败：{len(result.failures)} 项不一致（共 {result.checks} 项检查）")
        for failure in result.failures[:100]:
            print(f"- {failure}")
        if len(result.failures) > 100:
            print(f"- 其余 {len(result.failures) - 100} 项未显示")
        return 1

    print(f"校验通过：{result.checks} 项检查全部一致")
    print(f"文件：{args.candidate.expanduser().resolve()}")
    print(f"SHA-256：{sha256_file(args.candidate)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate + validate round-trip and fault-injection tests for the import template."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

# 让测试能直接 import scripts 包内的模块
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from generate_template import generate  # noqa: E402
from validate_template import validate  # noqa: E402

SPEC = {
    "title": "填写说明：必填以红色 * 标注。",
    "sheet_name": "导入模板",
    "data_rows": 10,
    "modules": [
        {
            "name": "基本信息",
            "fields": [
                {"name": "名称", "required": True, "logic": "最多 99 个字符"},
                {"name": "分类", "required": True, "logic": "填写大类原文"},
            ],
        },
        {
            "name": "财务信息",
            "fields": [
                {"name": "原值(元)", "required": True, "logic": "数字 0~99999999.99"},
                {"name": "备注", "required": False, "logic": "选填"},
            ],
        },
    ],
}


class TemplateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(__file__).resolve().parent / "_tmp"
        self.tmp.mkdir(exist_ok=True)
        self.fields = self.tmp / "fields.json"
        self.fields.write_text(json.dumps(SPEC, ensure_ascii=False), encoding="utf-8")
        self.out = self.tmp / "导入模板.xlsx"

    def tearDown(self) -> None:
        for f in (self.out, self.fields):
            if f.exists():
                f.unlink()
        if self.tmp.exists():
            self.tmp.rmdir()

    def _generate(self) -> None:
        generate(SPEC, self.out, force=True)

    def test_generate_and_validate_pass(self) -> None:
        self._generate()
        result = validate(self.out, SPEC)
        self.assertEqual(result.failures, [], msg="\n".join(result.failures))

    def test_module_merges(self) -> None:
        from openpyxl import load_workbook

        self._generate()
        wb = load_workbook(self.out, rich_text=True)
        ws = wb["导入模板"]
        row2 = sorted(str(m) for m in ws.merged_cells.ranges if m.min_row == 2)
        self.assertEqual(row2, ["A2:B2", "C2:D2"])
        self.assertEqual(ws.cell(2, 1).value, "基本信息")
        self.assertEqual(ws.cell(2, 3).value, "财务信息")

    def test_required_stars(self) -> None:
        from openpyxl.cell.rich_text import CellRichText

        self._generate()
        from openpyxl import load_workbook

        ws = load_workbook(self.out, rich_text=True)["导入模板"]
        # 名称(必填) 应有红色 *；备注(非必填) 不应有
        self.assertIsInstance(ws.cell(3, 1).value, CellRichText)
        result = validate(self.out, SPEC)
        self.assertEqual(result.failures, [], msg="\n".join(result.failures))

    def test_changed_logic_fails(self) -> None:
        self._generate()
        from openpyxl import load_workbook

        wb = load_workbook(self.out)
        wb["导入模板"]["D4"] = "篡改后的逻辑"
        wb.save(self.out)
        result = validate(self.out, SPEC)
        self.assertTrue(any("D4" in f for f in result.failures))

    def test_missing_star_fails(self) -> None:
        self._generate()
        from openpyxl import load_workbook

        wb = load_workbook(self.out, rich_text=True)
        ws = wb["导入模板"]
        # 用纯文本覆盖必填字段名，去掉富文本 *
        ws["C3"] = "原值(元)"
        wb.save(self.out)
        result = validate(self.out, SPEC)
        self.assertTrue(any("C3" in f and "*" in f for f in result.failures))


if __name__ == "__main__":
    unittest.main()

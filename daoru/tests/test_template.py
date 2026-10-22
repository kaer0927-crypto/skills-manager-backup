from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.worksheet.datavalidation import DataValidation

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from template_contract import GOLDEN_SHA256, GOLDEN_TEMPLATE, sha256_file  # noqa: E402


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


generate_template = load_script("generate_template")
validate_template = load_script("validate_template")


class TemplateSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_golden_template_validates(self) -> None:
        result = validate_template.validate(GOLDEN_TEMPLATE)
        self.assertEqual(result.failures, [])
        self.assertGreater(result.checks, 3000)

    def test_generator_is_byte_identical(self) -> None:
        output = self.root / "generated.xlsx"
        generate_template.generate(output, force=False)
        self.assertEqual(sha256_file(output), GOLDEN_SHA256)
        result = validate_template.validate(output)
        self.assertEqual(result.failures, [])

    def test_generator_refuses_overwrite_without_force(self) -> None:
        output = self.root / "generated.xlsx"
        generate_template.generate(output, force=False)
        with self.assertRaises(FileExistsError):
            generate_template.generate(output, force=False)

    def test_changed_header_fails(self) -> None:
        path = self.copy_golden("header.xlsx")
        workbook = load_workbook(path, rich_text=True)
        sheet = workbook["导入模板"]
        sheet["B3"].value = CellRichText(
            [
                TextBlock(
                    InlineFont(rFont="等线", sz=11, b=True),
                    "被篡改的名称 ",
                ),
                TextBlock(
                    InlineFont(
                        rFont="等线",
                        sz=11,
                        b=True,
                        color="FFFF0000",
                    ),
                    "*",
                ),
            ]
        )
        workbook.save(path)
        result = validate_template.validate(path)
        self.assertTrue(any("B3" in failure for failure in result.failures))

    def test_changed_width_fails(self) -> None:
        path = self.copy_golden("width.xlsx")
        workbook = load_workbook(path, rich_text=True)
        workbook["导入模板"].column_dimensions["B"].width = 27
        workbook.save(path)
        result = validate_template.validate(path)
        self.assertTrue(any("B 列宽" in failure for failure in result.failures))

    def test_removed_merge_fails(self) -> None:
        path = self.copy_golden("merge.xlsx")
        workbook = load_workbook(path, rich_text=True)
        workbook["导入模板"].unmerge_cells("A2:J2")
        workbook.save(path)
        result = validate_template.validate(path)
        self.assertTrue(any("合并单元格" in failure for failure in result.failures))

    def test_added_data_validation_fails(self) -> None:
        path = self.copy_golden("validation.xlsx")
        workbook = load_workbook(path, rich_text=True)
        sheet = workbook["导入模板"]
        validation = DataValidation(type="list", formula1='"是,否"')
        sheet.add_data_validation(validation)
        validation.add("B5:B1113")
        workbook.save(path)
        result = validate_template.validate(path)
        self.assertTrue(
            any("数据验证" in failure for failure in result.failures)
        )

    def copy_golden(self, name: str) -> Path:
        path = self.root / name
        shutil.copy2(GOLDEN_TEMPLATE, path)
        return path


if __name__ == "__main__":
    unittest.main()

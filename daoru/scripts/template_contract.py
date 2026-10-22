"""Shared constants for the Lanzhou public-property import template."""

from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
GOLDEN_TEMPLATE = SKILL_DIR / "assets" / "兰州公物仓_资产批量导入模板.xlsx"
SHEET_NAME = "导入模板"
OUTPUT_FILENAME = "兰州公物仓_资产批量导入模板.xlsx"
GOLDEN_SHA256 = "931fd7f872d4b11a66fec3009a319a5aa0ad15e12980e024f12955eb0f3d076a"
EXPECTED_DIMENSION = "A1:AI1113"
EXPECTED_MERGED_RANGES = (
    "A1:AI1",
    "A2:J2",
    "K2:N2",
    "O2:AD2",
    "AE2:AI2",
)
FIRST_DATA_ROW = 5
LAST_PREFORMATTED_ROW = 1113
COLUMN_COUNT = 35


def sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

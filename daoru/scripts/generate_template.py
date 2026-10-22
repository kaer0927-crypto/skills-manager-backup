#!/usr/bin/env python3
"""Generate the import template by copying the authoritative golden workbook."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

from template_contract import (
    GOLDEN_SHA256,
    GOLDEN_TEMPLATE,
    OUTPUT_FILENAME,
    sha256_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="生成兰州公物仓资产批量导入模板（字节级复制黄金母版）"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd() / OUTPUT_FILENAME,
        help=f"输出 XLSX 路径，默认当前目录/{OUTPUT_FILENAME}",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="目标文件已存在时覆盖；仅在用户明确同意后使用",
    )
    return parser.parse_args()


def generate(output: Path, force: bool) -> None:
    if not GOLDEN_TEMPLATE.is_file():
        raise FileNotFoundError(f"黄金母版不存在：{GOLDEN_TEMPLATE}")

    actual_hash = sha256_file(GOLDEN_TEMPLATE)
    if actual_hash != GOLDEN_SHA256:
        raise RuntimeError(
            "黄金母版 SHA-256 已变化，拒绝生成。"
            f"\n预期：{GOLDEN_SHA256}\n实际：{actual_hash}"
        )

    output = output.expanduser().resolve()
    if output.suffix.lower() != ".xlsx":
        raise ValueError("输出文件必须使用 .xlsx 扩展名")
    if output.exists() and not force:
        raise FileExistsError(
            f"目标文件已存在：{output}\n如确认覆盖，请加 --force。"
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{output.stem}.",
            suffix=".xlsx",
            dir=output.parent,
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
        shutil.copy2(GOLDEN_TEMPLATE, temp_path)
        with temp_path.open("rb") as handle:
            os.fsync(handle.fileno())
        os.replace(temp_path, output)
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()

    output_hash = sha256_file(output)
    if output_hash != GOLDEN_SHA256:
        raise RuntimeError(f"生成后校验失败：{output_hash}")

    print(f"已生成：{output}")
    print(f"大小：{output.stat().st_size} bytes")
    print(f"SHA-256：{output_hash}")


def main() -> int:
    args = parse_args()
    try:
        generate(args.output, args.force)
    except (FileNotFoundError, FileExistsError, RuntimeError, ValueError) as exc:
        print(f"生成失败：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

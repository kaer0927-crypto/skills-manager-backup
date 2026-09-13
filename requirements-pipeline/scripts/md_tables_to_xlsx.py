#!/usr/bin/env python3
"""把 Markdown 文件中的表格转成 xlsx（每个表格一个工作表）。

用途：需求流水线 P5 功能清单 md → 发客户确认的 xlsx。
依赖：openpyxl（pip install openpyxl）
用法：
    python3 md_tables_to_xlsx.py input.md -o output.xlsx
    python3 md_tables_to_xlsx.py input.md            # 输出同名 .xlsx
"""
import argparse
import re
import sys
from pathlib import Path


def parse_md_tables(text: str):
    """提取 md 中所有表格。返回 [(表名, [行]), ...]，表名取表格前最近的标题。"""
    lines = text.splitlines()
    tables, current, heading = [], [], "Sheet"
    last_heading = heading
    for line in lines:
        h = re.match(r"^#{1,6}\s+(.*)", line)
        if h:
            last_heading = re.sub(r"[\\/*?:\[\]]", "·", h.group(1)).strip()[:28] or "Sheet"
        if re.match(r"^\s*\|.*\|\s*$", line):
            current.append([c.strip() for c in line.strip().strip("|").split("|")])
        else:
            if len(current) >= 2:
                tables.append((last_heading, current))
            current = []
    if len(current) >= 2:
        tables.append((last_heading, current))
    # 去掉分隔行（|---|---|），清理加粗标记
    cleaned = []
    for name, rows in tables:
        body = [
            [re.sub(r"\*\*(.*?)\*\*", r"\1", c) for c in r]
            for r in rows
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c) or not r
        ]
        if len(body) >= 2:
            cleaned.append((name, body))
    return cleaned


def write_xlsx(tables, out_path: Path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    wb = Workbook()
    wb.remove(wb.active)
    head_fill = PatternFill("solid", fgColor="1F4E79")
    head_font = Font(bold=True, color="FFFFFF", size=11)
    body_font = Font(size=11)
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    used_names = set()

    for name, rows in tables:
        sheet_name, i = name, 2
        while sheet_name in used_names:
            sheet_name, i = f"{name[:25]}_{i}", i + 1
        used_names.add(sheet_name)
        ws = wb.create_sheet(sheet_name[:31])
        n_cols = max(len(r) for r in rows)
        widths = [0] * n_cols
        for ri, row in enumerate(rows, 1):
            for ci in range(n_cols):
                val = row[ci] if ci < len(row) else ""
                cell = ws.cell(row=ri, column=ci + 1, value=val)
                cell.border = border
                # 中文按 2 倍宽度估列宽
                w = sum(2 if ord(ch) > 127 else 1 for ch in str(val))
                widths[ci] = max(widths[ci], min(w, 60))
                if ri == 1:
                    cell.fill, cell.font = head_fill, head_font
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    cell.font = body_font
                    cell.alignment = Alignment(vertical="center", wrap_text=True)
        for ci, w in enumerate(widths, 1):
            ws.column_dimensions[ws.cell(row=1, column=ci).column_letter].width = max(w + 4, 10)
        ws.freeze_panes = "A2"
    wb.save(out_path)


def main():
    ap = argparse.ArgumentParser(description="Markdown 表格 → xlsx")
    ap.add_argument("input", help="输入 .md 文件")
    ap.add_argument("-o", "--output", help="输出 .xlsx 路径（默认同名）")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.exit(f"输入文件不存在: {src}")
    out = Path(args.output) if args.output else src.with_suffix(".xlsx")

    try:
        import openpyxl  # noqa: F401
    except ImportError:
        sys.exit("缺少依赖 openpyxl，请先执行: pip install openpyxl")

    tables = parse_md_tables(src.read_text(encoding="utf-8"))
    if not tables:
        sys.exit("未在输入文件中找到任何 Markdown 表格")
    write_xlsx(tables, out)
    print(f"✅ 已生成 {out}（{len(tables)} 个工作表）")


if __name__ == "__main__":
    main()

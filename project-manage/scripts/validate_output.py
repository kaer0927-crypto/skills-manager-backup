#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目管理表输出校验脚本：检查字段完整性、依赖闭环、排期合理性。

用法：
    python validate_output.py --input <项目管理.md>

检查项：
  A. 表格字段（必须 9 列，与规范一致）
  B. 10 项核心里程碑（按序，末位为业务培训）
  C. 状态默认「未开始」
  D. 依赖关系闭环（无循环、无孤立引用）
  E. 排期合理性（结束 ≥ 开始、后置开始 ≥ 前置结束）
  F. 无优先级字段
  G. 信息不足处标注「待补充」

退出码：0 = 通过，1 = 失败。
"""

import argparse
import io
import re
import sys
from datetime import datetime

# 修复 Windows GBK 编码下的 emoji 输出问题
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


MILESTONES = [
    "需求评审",
    "技术方案评审",
    "UI 评审",
    "测试用例评审",
    "开发提测",
    "测试完成",
    "验收完成",
    "发版上线",
    "生产验证",
    "业务培训",
]

EXPECTED_HEADER = [
    "任务/子任务",
    "所属阶段/里程碑",
    "负责人/角色",
    "开始时间",
    "结束时间",
    "预估工期",
    "依赖关系",
    "状态",
    "备注",
]

FORBIDDEN_FIELDS = ["优先级", "进度", "工时", "Story Point"]


def parse_table(content):
    """提取所有 Markdown 表格，返回 (header, rows) 列表。"""
    tables = []
    lines = content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "|" in line[1:]:
            # 解析表头
            header = [c.strip() for c in line.strip("|").split("|")]
            i += 1
            # 跳过分隔行
            if i < len(lines) and re.match(r"^\|[\s\-:|]+\|?$", lines[i].strip()):
                i += 1
            else:
                continue
            rows = []
            while i < len(lines):
                row_line = lines[i].strip()
                if not row_line.startswith("|"):
                    break
                row = [c.strip() for c in row_line.strip("|").split("|")]
                if len(row) != len(header):
                    # 跳过列数不匹配的行
                    i += 1
                    continue
                rows.append(row)
                i += 1
            tables.append((header, rows))
        else:
            i += 1
    return tables


def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def find_main_table(tables):
    """查找主项目管理明细表（9 列）。"""
    for header, rows in tables:
        if header == EXPECTED_HEADER:
            return (header, rows)
    return None


def validate(content):
    """主校验函数。返回 (passed, issues)。"""
    issues = []
    warnings = []

    tables = parse_table(content)
    if not tables:
        issues.append("❌ 未找到任何 Markdown 表格")
        return False, issues

    main = find_main_table(tables)
    if not main:
        issues.append(
            f"❌ 未找到项目管理明细表（应包含 9 列：{EXPECTED_HEADER}）"
        )
        return False, issues

    header, rows = main

    # A. 字段检查
    if header != EXPECTED_HEADER:
        issues.append(
            f"❌ 表头字段不匹配\n   期望：{EXPECTED_HEADER}\n   实际：{header}"
        )
    else:
        print("✅ A. 表格字段与规范一致（9 列）")

    # F. 禁止字段检查
    for forbidden in FORBIDDEN_FIELDS:
        if any(forbidden in h for h in header):
            issues.append(f"❌ 出现禁止字段：[{forbidden}]")

    # B. 10 项核心里程碑检查
    task_names = [r[0] for r in rows]
    milestone_indices = {}
    for ms in MILESTONES:
        # 匹配"等于"或"以<ms>开头（敏捷版用 Sprint 前缀）"
        for idx, name in enumerate(task_names):
            if name == ms or name.endswith(f" - {ms}") or name.endswith(f"-{ms}"):
                milestone_indices[ms] = idx
                break

    missing = [ms for ms in MILESTONES if ms not in milestone_indices]
    if missing:
        issues.append(f"❌ 缺少里程碑：{missing}")
    else:
        print("✅ B. 10 项核心里程碑全部覆盖")

    # 顺序检查
    order_issues = []
    last_idx = -1
    for ms in MILESTONES:
        idx = milestone_indices.get(ms, -1)
        if idx > 0 and idx < last_idx:
            order_issues.append(
                f"   - [{ms}] 出现在第 {idx + 1} 行，但应在 [{MILESTONES[MILESTONES.index(ms) - 1]}] 之后"
            )
        if idx > last_idx:
            last_idx = idx
    if order_issues:
        issues.append("❌ 里程碑顺序错误：\n" + "\n".join(order_issues))
    else:
        print("✅ B. 里程碑顺序正确（末位为业务培训）")

    # 业务培训必须在末位
    if "业务培训" in milestone_indices:
        training_idx = milestone_indices["业务培训"]
        if training_idx != max(milestone_indices.values()):
            warnings.append(
                f"⚠️ 业务培训未在末位（出现在第 {training_idx + 1} 行）"
            )

    # C. 状态默认「未开始」
    status_col_idx = header.index("状态")
    non_default_status = []
    for row in rows:
        if row[status_col_idx] not in ["未开始", "进行中", "已完成", "已阻塞", "-"]:
            non_default_status.append(
                f"   - [{row[0]}] 状态值非法：[{row[status_col_idx]}]"
            )
    if non_default_status:
        warnings.append("⚠️ 状态值非默认值：\n" + "\n".join(non_default_status))
    else:
        print("✅ C. 状态值合法（默认未开始）")

    # D. 依赖关系闭环检查
    deps_col_idx = header.index("依赖关系")
    name_to_row = {r[0]: r for r in rows}
    all_task_names = set(name_to_row.keys())
    dep_issues = []

    for row in rows:
        deps_str = row[deps_col_idx].strip()
        if not deps_str or deps_str == "-":
            continue
        deps = [d.strip() for d in deps_str.split(",") if d.strip()]
        for dep in deps:
            if dep not in all_task_names:
                dep_issues.append(
                    f"   - [{row[0]}] 引用了不存在的前置任务 [{dep}]"
                )

    # 检查循环依赖（简化版：DFS）
    def has_cycle(graph):
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {n: WHITE for n in all_task_names}

        def dfs(node):
            color[node] = GRAY
            row = name_to_row[node]
            deps_str = row[deps_col_idx].strip()
            deps = [] if not deps_str or deps_str == "-" else [
                d.strip() for d in deps_str.split(",") if d.strip()
            ]
            for d in deps:
                if color[d] == GRAY:
                    return True
                if color[d] == WHITE and dfs(d):
                    return True
            color[node] = BLACK
            return False

        for n in all_task_names:
            if color[n] == WHITE and dfs(n):
                return True
        return False

    cycle = has_cycle({n: name_to_row[n] for n in all_task_names})
    if cycle:
        dep_issues.append("   - 存在循环依赖")

    if dep_issues:
        issues.append("❌ 依赖关系错误：\n" + "\n".join(dep_issues))
    else:
        print("✅ D. 依赖关系闭环（无循环、无孤立引用）")

    # E. 排期合理性检查
    start_col_idx = header.index("开始时间")
    end_col_idx = header.index("结束时间")
    duration_col_idx = header.index("预估工期")

    schedule_issues = []
    for row in rows:
        task = row[0]
        start = row[start_col_idx].strip()
        end = row[end_col_idx].strip()

        # 跳过待排期
        if start in ["待排期", "-", ""] or end in ["待排期", "-", ""]:
            continue

        try:
            s = parse_date(start)
            e = parse_date(end)
        except ValueError:
            schedule_issues.append(
                f"   - [{task}] 日期格式错误：start=[{start}] end=[{end}]"
            )
            continue

        if e < s:
            schedule_issues.append(
                f"   - [{task}] 结束时间早于开始时间"
            )
            continue

        # 工期一致性
        duration_days = (e - s).days + 1
        duration_str = row[duration_col_idx].strip()
        m = re.match(r"^(\d+)\s*d", duration_str)
        if m:
            d = int(m.group(1))
            if d != duration_days:
                schedule_issues.append(
                    f"   - [{task}] 工期 [{duration_str}] 与起止日期 [{duration_days}d] 不一致"
                )

    # 后置任务开始 ≥ 前置结束
    for row in rows:
        task = row[0]
        deps_str = row[deps_col_idx].strip()
        start = row[start_col_idx].strip()
        if not deps_str or deps_str == "-":
            continue
        if start in ["待排期", "-", ""]:
            continue
        try:
            s = parse_date(start)
        except ValueError:
            continue

        deps = [d.strip() for d in deps_str.split(",") if d.strip()]
        for dep in deps:
            if dep not in name_to_row:
                continue
            dep_row = name_to_row[dep]
            dep_end = dep_row[end_col_idx].strip()
            if dep_end in ["待排期", "-", ""]:
                continue
            try:
                de = parse_date(dep_end)
            except ValueError:
                continue
            if s < de:
                schedule_issues.append(
                    f"   - [{task}] 开始时间 [{start}] 早于前置 [{dep}] 结束时间 [{dep_end}]"
                )

    if schedule_issues:
        issues.append("❌ 排期问题：\n" + "\n".join(schedule_issues))
    else:
        print("✅ E. 排期合理（结束 ≥ 开始、后置开始 ≥ 前置结束、工期一致）")

    # G. 备注含"待补充"提示（不强制，仅提醒）
    note_col_idx = header.index("备注")
    placeholder_count = sum(
        1 for r in rows if "待补充" in r[note_col_idx]
        or "待确认" in r[note_col_idx]
    )
    if placeholder_count > 0:
        warnings.append(
            f"⚠️ 有 {placeholder_count} 个任务备注含「待补充/待确认」，请人工确认"
        )

    passed = len(issues) == 0

    print()
    print("=" * 50)
    if passed:
        print(f"🎉 校验通过！共 {len(rows)} 行任务")
    else:
        print(f"❌ 校验失败！共 {len(issues)} 个错误：")
        for issue in issues:
            print(issue)
    if warnings:
        print()
        print("提醒：")
        for w in warnings:
            print(w)
    print("=" * 50)

    return passed, issues + warnings


def main():
    parser = argparse.ArgumentParser(description="项目管理表输出校验")
    parser.add_argument("--input", required=True, help="项目管理 Markdown 文件路径")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    passed, _ = validate(content)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
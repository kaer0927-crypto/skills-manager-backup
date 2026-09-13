#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
排期推算脚本：基于起始日 + 任务工期 + 依赖关系，推算每个任务的开始/结束时间。

用法：
    python calc_schedule.py --tasks tasks.json --start 2026-07-10

输入：
    tasks.json 格式（示例）：
    [
      {"name": "需求评审", "duration": 1, "depends": []},
      {"name": "技术方案评审", "duration": 2, "depends": ["需求评审"]},
      ...
    ]

输出（stdout，JSON）：
    [
      {"name": "需求评审", "start": "2026-07-10", "end": "2026-07-10", "duration": 1},
      ...
    ]
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict, deque


def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def add_days(d, n):
    return d + timedelta(days=n)


def topo_sort(tasks):
    """拓扑排序，返回拓扑序的任务列表。若存在循环依赖，抛出异常。"""
    name_to_task = {t["name"]: t for t in tasks}
    in_degree = {t["name"]: 0 for t in tasks}
    graph = defaultdict(list)

    for t in tasks:
        for dep in t.get("depends", []):
            if dep not in name_to_task:
                raise ValueError(f"任务 [{t['name']}] 依赖了不存在的任务 [{dep}]")
            graph[dep].append(t["name"])
            in_degree[t["name"]] += 1

    # 检查孤立引用（依赖不在任务列表中）
    all_deps = set()
    for t in tasks:
        for dep in t.get("depends", []):
            all_deps.add(dep)
    missing = all_deps - set(name_to_task.keys())
    if missing:
        raise ValueError(f"存在孤立引用（依赖的任务不存在）：{missing}")

    queue = deque([n for n, d in in_degree.items() if d == 0])
    result = []
    while queue:
        n = queue.popleft()
        result.append(n)
        for m in graph[n]:
            in_degree[m] -= 1
            if in_degree[m] == 0:
                queue.append(m)

    if len(result) != len(tasks):
        raise ValueError("依赖关系存在循环，无法完成拓扑排序")

    return [name_to_task[n] for n in result]


def calc_schedule(tasks, start_date_str):
    """推算每个任务的开始/结束时间。"""
    start_date = parse_date(start_date_str)
    name_to_end = {}  # 任务名 -> 结束日期

    sorted_tasks = topo_sort(tasks)

    for t in sorted_tasks:
        duration = t["duration"]
        if duration < 1:
            raise ValueError(f"任务 [{t['name']}] 工期 < 1d，非法")

        deps = t.get("depends", [])
        if not deps:
            # 无前置：使用项目起始日
            task_start = start_date
        else:
            # 有前置：取所有前置结束时间的最大值 +1d
            latest_end = max(name_to_end[d] for d in deps)
            task_start = add_days(latest_end, 1)

        task_end = add_days(task_start, duration - 1)
        name_to_end[t["name"]] = task_end

        t["start"] = task_start.strftime("%Y-%m-%d")
        t["end"] = task_end.strftime("%Y-%m-%d")

    return sorted_tasks


def calc_critical_path(sorted_tasks):
    """计算关键路径（最长链路）。返回关键路径上的任务名列表。"""
    # 已按拓扑序排好；计算每个任务的「最早完成时间」对应的最长链
    longest_chain = {}
    for t in sorted_tasks:
        deps = t.get("depends", [])
        if not deps:
            longest_chain[t["name"]] = [t["name"]]
        else:
            # 找到前置中累计链路最长的那个
            best_dep = max(deps, key=lambda d: len(longest_chain.get(d, [])))
            longest_chain[t["name"]] = longest_chain[best_dep] + [t["name"]]
    # 取最终最长的
    final = max(sorted_tasks, key=lambda t: len(longest_chain[t["name"]]))
    return longest_chain[final["name"]]


def main():
    parser = argparse.ArgumentParser(description="排期推算脚本")
    parser.add_argument("--tasks", required=True, help="任务列表 JSON 文件路径")
    parser.add_argument("--start", required=True, help="项目起始日 YYYY-MM-DD")
    args = parser.parse_args()

    with open(args.tasks, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    scheduled = calc_schedule(tasks, args.start)
    critical = calc_critical_path(scheduled)

    output = {
        "start_date": args.start,
        "tasks": [{"name": t["name"], "start": t["start"], "end": t["end"],
                   "duration": t["duration"]} for t in scheduled],
        "critical_path": critical,
        "total_duration_days": (
            datetime.strptime(scheduled[-1]["end"], "%Y-%m-%d").date()
            - datetime.strptime(scheduled[0]["start"], "%Y-%m-%d").date()
        ).days + 1,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
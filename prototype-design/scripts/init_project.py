#!/usr/bin/env python3
"""初始化一个 PRD 原型项目骨架。

用法:
    python init_project.py <target_dir> [--name <项目名>]

行为:
1. 检测 <target_dir>/nav.json 或 CLAUDE.md 是否已存在：存在则报错退出（项目只能在创建时初始化一次）。
2. 整个 ``assets/scaffold/`` 拷到 <target_dir>。
3. 替换 <target_dir>/CLAUDE.md 里的 ``{{PROJECT_NAME}}`` 为 --name（若有）或目录名，并把 ``nav.json.projectName`` 也设为 --name。
4. 调 scaffold/scripts/sync_nav.py 生成 nav.js 并渲染所有 desc/<id>.html（sync_nav 内部已调 build_desc）。
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure stdout can print emojis on Windows GBK terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SCAFFOLD = SKILL_DIR / "assets" / "scaffold"


def fail(msg: str) -> None:
    print(f"❌ {msg}")
    sys.exit(1)


def copy_scaffold(target: Path) -> None:
    """把整个 scaffold 拷到 target。"""
    if not SCAFFOLD.exists():
        fail(f"scaffold 不存在: {SCAFFOLD}")
    # 防递归自拷贝：目标目录不能与 scaffold 互相包含
    if target.is_relative_to(SCAFFOLD) or SCAFFOLD.is_relative_to(target):
        fail("目标目录与 scaffold 存在包含关系，拒绝拷贝。")

    target.mkdir(parents=True, exist_ok=True)

    for src in SCAFFOLD.rglob("*"):
        # 排除 Python 编译缓存，避免把 .pyc 带进每个新项目
        if "__pycache__" in src.parts:
            continue
        rel = src.relative_to(SCAFFOLD)
        dst = target / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def set_project_name(target: Path, name: str) -> None:
    """替换 CLAUDE.md 里的 {{PROJECT_NAME}}，并把 nav.json.projectName 同步成 --name。"""
    claude_md = target / "CLAUDE.md"
    if claude_md.exists():
        text = claude_md.read_text(encoding="utf-8")
        text = text.replace("{{PROJECT_NAME}}", name)
        claude_md.write_text(text, encoding="utf-8")

    nav_json = target / "nav.json"
    if nav_json.exists():
        nav = json.loads(nav_json.read_text(encoding="utf-8"))
        nav["projectName"] = name
        nav_json.write_text(
            json.dumps(nav, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def run_subprocess(cmd: list[str]) -> None:
    """跑子命令；失败抛错。"""
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        fail(f"子命令失败: {' '.join(cmd)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化 PRD 原型项目")
    parser.add_argument("target_dir", help="目标目录路径")
    parser.add_argument("--name", default=None, help="项目显示名（默认 = 目录名）")
    args = parser.parse_args()

    target = Path(args.target_dir).resolve()

    # 1) 检测目标：必须是空目录（或不存在），防止与既有业务文件混入 / 递归自拷贝
    if target.exists() and any(target.iterdir()):
        fail(
            "目标目录必须为空或不存在：`<target>` 下已有内容。\n"
            "   - 若它已是原型项目：原型项目只能在创建时初始化一次，后续修改请进入\n"
            "     项目目录后按 CLAUDE.md 工作流操作，不要手动删 nav.json / CLAUDE.md 绕过。\n"
            "   - 请换一个空目录重新 init。"
        )

    # 2) 整体拷贝 scaffold
    copy_scaffold(target)

    # 3) 设置项目名
    project_name = args.name or target.name
    set_project_name(target, project_name)

    # 4) 同步 nav.js 并渲染 desc（sync_nav 内部已调用 build_desc，勿重复渲染）
    sync_nav = SCAFFOLD / "scripts" / "sync_nav.py"
    run_subprocess([sys.executable, str(sync_nav), str(target)])

    print(f"✓ 初始化完成 → 双击 {target / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

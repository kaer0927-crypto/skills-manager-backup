#!/usr/bin/env bash
# 自检：列出 <project-root>/demo-code 下的现有 Demo 项目及其类型。
# 用法: list-demos.sh
# 项目根目录默认取当前工作目录，可用环境变量 DEMO_DESIGN_ROOT 覆盖。
set -euo pipefail

PROJECT_ROOT="${DEMO_DESIGN_ROOT:-$PWD}"
DEMO_CODE_DIR="$PROJECT_ROOT/demo-code"

if [ ! -d "$DEMO_CODE_DIR" ]; then
  echo "STATE=NO_DEMO_CODE"
  echo "demo-code 目录不存在: $DEMO_CODE_DIR"
  exit 0
fi

# 收集子目录（含 package.json 才算一个项目）
found=0
for d in "$DEMO_CODE_DIR"/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  pkg="$d/package.json"
  type="unknown"
  if [ -f "$pkg" ]; then
    if grep -q '"vant"' "$pkg"; then
      type="mobile"
    elif grep -q '"element-plus"' "$pkg"; then
      type="admin"
    fi
    installed="no"
    [ -d "$d/node_modules" ] && installed="yes"
    if [ "$found" -eq 0 ]; then
      echo "STATE=HAS_PROJECTS"
      echo "现有 Demo 项目（$DEMO_CODE_DIR）:"
    fi
    found=1
    echo "  - $name  [类型:$type] [依赖已装:$installed]"
  fi
done

if [ "$found" -eq 0 ]; then
  echo "STATE=EMPTY_DEMO_CODE"
  echo "demo-code 存在但无有效项目: $DEMO_CODE_DIR"
fi

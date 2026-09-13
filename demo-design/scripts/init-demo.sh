#!/usr/bin/env bash
# 初始化一个新的 Demo 项目到 <project-root>/demo-code/<name>
# 用法: init-demo.sh <type> <project-name> [--no-install]
#   type          : mobile | admin
#   project-name  : kebab-case（小写字母/数字/连字符）
#   --no-install  : 只复制模板，不执行 npm install
#
# 项目根目录默认取当前工作目录，可用环境变量 DEMO_DESIGN_ROOT 覆盖。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES_DIR="$SKILL_DIR/templates"

PROJECT_ROOT="${DEMO_DESIGN_ROOT:-$PWD}"
DEMO_CODE_DIR="$PROJECT_ROOT/demo-code"

usage() {
  echo "用法: init-demo.sh <mobile|admin> <project-name(kebab-case)> [--no-install]"
}

TYPE="${1:-}"
NAME="${2:-}"
NO_INSTALL="${3:-}"

if [ -z "$TYPE" ] || [ -z "$NAME" ]; then
  usage
  exit 1
fi

case "$TYPE" in
  mobile|admin) ;;
  *) echo "❌ 未知类型: $TYPE（当前支持 mobile / admin）"; exit 1 ;;
esac

if ! printf '%s' "$NAME" | grep -Eq '^[a-z][a-z0-9]*(-[a-z0-9]+)*$'; then
  echo "❌ 项目名需为 kebab-case（小写字母开头，仅含小写字母/数字/连字符）: $NAME"
  exit 1
fi

SRC="$TEMPLATES_DIR/$TYPE"
if [ ! -d "$SRC" ]; then
  echo "❌ 模板不存在: $SRC"
  exit 1
fi

DEST="$DEMO_CODE_DIR/$NAME"
if [ -e "$DEST" ]; then
  echo "❌ 目标目录已存在，避免覆盖: $DEST"
  exit 1
fi

mkdir -p "$DEMO_CODE_DIR"
echo "📦 复制模板 [$TYPE] → $DEST（排除 node_modules / dist）"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude 'node_modules' --exclude 'dist' "$SRC/" "$DEST/"
else
  mkdir -p "$DEST"
  (
    cd "$SRC"
    find . \( -type d \( -name node_modules -o -name dist \) -prune \) -o -type f -print | while IFS= read -r f; do
      d="$DEST/$(dirname "$f")"
      mkdir -p "$d"
      cp "$f" "$DEST/$f"
    done
  )
fi

# 初始化后的项目与模板保持一致，不改写任何被复制的文件（含 CLAUDE.md）。
if [ "$NO_INSTALL" = "--no-install" ]; then
  echo "⏭️  已跳过依赖安装（--no-install）。稍后请在 $DEST 执行 npm install"
else
  echo "📥 安装依赖: npm install（cwd=$DEST）"
  ( cd "$DEST" && npm install )
fi

echo ""
echo "✅ 初始化完成: $DEST"
echo "下一步:"
echo "  cd \"$DEST\""
echo "  npm run dev      # 本地开发"
echo "  npm run build    # 生产构建 → dist/"

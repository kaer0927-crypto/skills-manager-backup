#!/usr/bin/env bash
# 构建指定 Demo 项目为静态产物，并输出发布说明（Nginx / Apache）。
# 用法: build-demo.sh <project-name>
# 项目根目录默认取当前工作目录，可用环境变量 DEMO_DESIGN_ROOT 覆盖。
set -euo pipefail

PROJECT_ROOT="${DEMO_DESIGN_ROOT:-$PWD}"
NAME="${1:-}"

if [ -z "$NAME" ]; then
  echo "用法: build-demo.sh <project-name>"
  exit 1
fi

DEST="$PROJECT_ROOT/demo-code/$NAME"
if [ ! -d "$DEST" ]; then
  echo "❌ 项目不存在: $DEST"
  exit 1
fi

if [ ! -d "$DEST/node_modules" ]; then
  echo "📥 未检测到依赖，先执行 npm install"
  ( cd "$DEST" && npm install )
fi

echo "🔨 构建: npm run build（cwd=$DEST）"
( cd "$DEST" && npm run build )

DIST="$DEST/dist"
if [ ! -d "$DIST" ]; then
  echo "❌ 构建未产出 dist/，请检查构建日志"
  exit 1
fi

echo ""
echo "✅ 构建完成，静态产物: $DIST"
echo "产物文件数: $(find "$DIST" -type f | wc -l | tr -d ' ')"
echo ""
cat <<'EOF'
────────────────────── 发布说明 ──────────────────────
Demo 使用 hash 路由 + 相对资源路径，dist/ 为纯静态文件，可直接托管。

▶ Nginx（放到任意子路径均可，例如 /demo/foo/）:
  location /demo/foo/ {
      alias /var/www/demo-foo/dist/;   # 指向 dist 目录
      index index.html;
      try_files $uri $uri/ /demo/foo/index.html;
  }

▶ Apache（.htaccess，与 dist 同目录）:
  <IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /demo/foo/
    RewriteRule ^index\.html$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . index.html [L]
  </IfModule>

▶ 本地快速验证:
  npm run preview        # 使用 vite 预览服务器
  # 或直接把 dist/ 拷到静态服务器根目录
────────────────────────────────────────────────────
EOF

#!/usr/bin/env python3
"""
md_to_html.py — 横纵分析法 HTML 网页版报告生成器

将 Markdown 研究报告注入到精美的 HTML 模板中，生成可直接在浏览器中打开的单文件网页。

使用方式:
  python3 md_to_html.py input.md output.html \
    --title "报告标题" \
    --subtitle "副标题描述" \
    --author "liuyz" \
    --tag "横纵深研" \
    --date "2026年04月"

除 input.md 和 output.html 外，所有参数均可选，脚本会尝试从 Markdown 内容自动推断。

依赖: 无（纯 Python，零外部依赖）
模板: 同目录下的 report_template.html
"""

import argparse
import os
import re
import sys
from datetime import datetime


def extract_meta_from_md(md_content: str) -> dict:
    """从 Markdown 内容中尝试自动提取元信息"""
    meta = {}

    # 提取 H1 标题
    h1_match = re.match(r'^#\s+(.+)', md_content, re.MULTILINE)
    if h1_match:
        meta['title'] = h1_match.group(1).strip()

    # 提取 blockquote 元信息行（> 研究时间：... | 所属领域：... | ...）
    bq_match = re.search(r'>\s*研究时间[：:](.+?)(?:\||$)', md_content)
    if bq_match:
        meta['date'] = bq_match.group(1).strip()

    # 提取制作人
    author_match = re.search(r'制作人[：:](.+?)(?:\||$|\n)', md_content)
    if author_match:
        meta['author'] = author_match.group(1).strip()

    # 提取所属领域作为 tag
    field_match = re.search(r'所属领域[：:](.+?)(?:\||$)', md_content)
    if field_match:
        meta['tag'] = field_match.group(1).strip()

    # 提取一句话定义作为副标题
    # 查找「一句话定义」章节下的第一段非空文本
    definition_match = re.search(
        r'##\s*一[、.]?\s*一句话定义\s*\n+(.+?)(?:\n\n|\n---|\n##)',
        md_content, re.DOTALL
    )
    if definition_match:
        subtitle_raw = definition_match.group(1).strip()
        # 截取合理长度（取第一句或前80字）
        # 先去掉 markdown 格式
        subtitle_clean = re.sub(r'[*_`\[\]]', '', subtitle_raw)
        if len(subtitle_clean) > 80:
            # 尝试在句号、破折号等处截断
            for sep in ['——', '。', '，', '；', '—']:
                idx = subtitle_clean.find(sep, 30)
                if 30 < idx < 100:
                    subtitle_clean = subtitle_clean[:idx + len(sep)]
                    break
            else:
                subtitle_clean = subtitle_clean[:80] + '……'
        meta['subtitle'] = subtitle_clean

    return meta


def build_html(md_content: str, template_path: str,
               title: str, subtitle: str, author: str,
               tag: str, date_str: str) -> str:
    """将 Markdown 内容注入 HTML 模板"""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    year = datetime.now().strftime('%Y')

    replacements = {
        '{{REPORT_TITLE}}': f'{title} — 横纵分析报告',
        '{{HEADER_TAG}}': tag,
        '{{HERO_TITLE}}': f'{title}深度研究报告',
        '{{HERO_SUBTITLE}}': subtitle,
        '{{AUTHOR}}': author,
        '{{DATE}}': date_str,
        '{{YEAR}}': year,
        '{{MARKDOWN_CONTENT}}': md_content,
    }

    result = template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result


def main():
    parser = argparse.ArgumentParser(
        description='横纵分析法 HTML 网页版报告生成器'
    )
    parser.add_argument('input', help='输入 Markdown 文件路径')
    parser.add_argument('output', help='输出 HTML 文件路径')
    parser.add_argument('--title', help='报告标题（默认从 Markdown H1 提取）')
    parser.add_argument('--subtitle', help='副标题/描述（默认从「一句话定义」提取）')
    parser.add_argument('--author', default='liuyz', help='作者名（默认 liuyz）')
    parser.add_argument('--tag', help='顶部标签文字（默认从「所属领域」提取，兜底为「横纵深研」）')
    parser.add_argument('--date', help='日期文字（默认从「研究时间」提取或取当前年月）')

    args = parser.parse_args()

    # 读取 Markdown
    if not os.path.exists(args.input):
        print(f'[错误] 文件不存在: {args.input}', file=sys.stderr)
        sys.exit(1)

    with open(args.input, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 自动推断元信息
    auto_meta = extract_meta_from_md(md_content)

    title = args.title or auto_meta.get('title', '横纵分析报告')
    subtitle = args.subtitle or auto_meta.get('subtitle', '横纵分析法深度研究报告')
    author = args.author  # 已有默认值 liuyz
    tag = args.tag or auto_meta.get('tag', '横纵深研')
    date_str = args.date or auto_meta.get('date', datetime.now().strftime('%Y年%m月'))

    # 定位模板
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'report_template.html')
    if not os.path.exists(template_path):
        print(f'[错误] 模板文件不存在: {template_path}', file=sys.stderr)
        sys.exit(1)

    # 生成 HTML
    html_output = build_html(
        md_content=md_content,
        template_path=template_path,
        title=title,
        subtitle=subtitle,
        author=author,
        tag=tag,
        date_str=date_str,
    )

    # 写入输出
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html_output)

    size_kb = os.path.getsize(args.output) / 1024
    print(f'[OK] HTML 已生成: {args.output} ({size_kb:.1f} KB)')


if __name__ == '__main__':
    main()

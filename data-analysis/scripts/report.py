#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report.py —— analysis.json (+ AI 洞见) → 单文件离线 HTML 报告

报告只包含四个板块：
  1. 核心指标（KPI 卡片）
  2. AI 智能洞见（核心结论 / 支撑数据 / 异常与风险 / 可执行建议 / 下一步）
  3. 可视化分析（ECharts 图表，离线内嵌）
  4. 可视化分析数据（每张图表背后的底层数据表格 + 「导出 CSV」按钮，纯前端 Blob 下载）

离线：ECharts 直接内联进 HTML，不引用任何远程资源，双击即开。
洞见来源：analysis.json 里的 "insights" 字段（由 Claude 填写）；缺失时给出占位提示。
"""
import argparse
import html
import json
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def cleanup_intermediates(analysis_path, insights_path, source_path):
    """渲染完成后删除流程产生的中间 JSON（analysis/insights/focus/schema），仅保留 HTML 与原始数据。

    以「原始数据源 stem」为命名约定，在数据同目录定位：
      <stem>.analysis.json  <stem>.insights.json  <stem>.focus.json  <stem>.schema.json
    另删除本次实际传入的 analysis.json / insights.json（路径可能由 --out 自定义）。
    只删 .json 文件，绝不触碰原始 CSV / HTML。
    """
    src = Path(source_path)
    d = src.parent
    stem = src.stem
    targets = [
        Path(analysis_path),
        d / f"{stem}.analysis.json",
        d / f"{stem}.insights.json",
        d / f"{stem}.focus.json",
        d / f"{stem}.schema.json",
    ]
    if insights_path:
        targets.append(Path(insights_path))
    deleted, seen = [], set()
    for t in targets:
        t = t.resolve()
        key = str(t)
        if key in seen:
            continue
        seen.add(key)
        try:
            if t.exists() and t.suffix.lower() == ".json":
                t.unlink()
                deleted.append(str(t))
        except OSError as e:
            print(f"[report] ⚠️ 删除失败 {t}: {e}")
    return deleted


def _esc(x) -> str:
    return html.escape("" if x is None else str(x))


# --------------------------------------------------------------------------- #
# 各板块渲染
# --------------------------------------------------------------------------- #
def render_kpis(kpis):
    cards = []
    for k in kpis or []:
        cards.append(f"""
      <div class="kpi">
        <div class="kpi-label">{_esc(k.get('label'))}</div>
        <div class="kpi-value">{_esc(k.get('value'))}<span class="kpi-unit">{_esc(k.get('unit'))}</span></div>
        <div class="kpi-sub">{_esc(k.get('sub'))}</div>
      </div>""")
    return f'<div class="kpi-grid">{"".join(cards)}</div>'


def _ul(items):
    if not items:
        return '<p class="muted">—</p>'
    if isinstance(items, str):
        items = [items]
    return "<ul>" + "".join(f"<li>{_esc(i)}</li>" for i in items) + "</ul>"


def render_insights(ins):
    if not ins:
        return """
      <div class="insight-empty">
        ⚠️ 尚未生成 AI 洞见。请让 Claude 读取 analysis.json，以数据分析专家视角填写
        insights（核心结论 / 支撑数据 / 异常与风险 / 可执行建议 / 下一步）后重新渲染。
      </div>"""
    blocks = [
        ("🎯 核心结论", ins.get("core_conclusion"), "conclusion"),
        ("📊 支撑数据", ins.get("supporting_data"), "support"),
        ("⚠️ 异常与风险", ins.get("risks"), "risk"),
        ("✅ 可执行建议", ins.get("recommendations"), "action"),
        ("🚀 下一步", ins.get("next_steps"), "next"),
    ]
    out = []
    for label, content, cls in blocks:
        body = f"<p>{_esc(content)}</p>" if isinstance(content, str) else _ul(content)
        out.append(f"""
      <div class="insight-block {cls}">
        <h3>{label}</h3>
        {body}
      </div>""")
    return f'<div class="insight-grid">{"".join(out)}</div>'


def render_charts_containers(charts):
    return "".join(
        f'<div class="chart-card"><div class="chart-title">{_esc(c.get("title"))}</div>'
        f'<div class="chart" id="chart_{i}"></div></div>'
        for i, c in enumerate(charts or [])
    )


def chart_option(c):
    """把一个 chart dict 转成 ECharts option。"""
    t = c.get("type")
    if t == "pie":
        return {
            "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
            "legend": {"type": "scroll", "bottom": 0},
            "series": [{
                "type": "pie", "radius": ["40%", "70%"], "avoidLabelOverlap": True,
                "itemStyle": {"borderRadius": 6, "borderColor": "#fff", "borderWidth": 2},
                "data": c.get("data", []),
            }],
        }
    axis_x = {"type": "category", "data": c.get("x", []), "axisLabel": {"rotate": 30 if len(c.get("x", [])) > 6 else 0}}
    series = [{"name": s["name"], "type": t, "data": s["data"],
               "smooth": t == "line", "areaStyle": {} if t == "line" else None} for s in c.get("series", [])]
    return {
        "tooltip": {"trigger": "axis"},
        "grid": {"left": 48, "right": 24, "top": 24, "bottom": 64, "containLabel": True},
        "xAxis": axis_x,
        "yAxis": {"type": "value"},
        "series": series,
    }


def chart_to_table(c: dict) -> dict:
    """把一个 chart dict 转成 {title, columns, rows} 的表格数据，供「可视化分析数据」板块展示 + 导出。"""
    t = c.get("type")
    title = c.get("title", "")
    if t == "pie":
        cols = ["类别", "值"]
        rows = [[d.get("name"), d.get("value")] for d in c.get("data", [])]
    else:
        series = c.get("series", [])
        x = c.get("x", [])
        xlabel = "时间" if t == "line" else "类别"
        cols = [xlabel] + [(s.get("name") or f"系列{i + 1}") for i, s in enumerate(series)]
        rows = []
        for i in range(len(x)):
            row = [x[i]]
            for s in series:
                d = s.get("data", [])
                row.append(d[i] if i < len(d) else None)
            rows.append(row)
    return {"title": title, "columns": cols, "rows": rows}


def render_chart_data(charts):
    tables = [chart_to_table(c) for c in (charts or [])]
    if not tables:
        return '<p class="muted">— 暂无可视化分析数据</p>'
    out = ['<div class="chart-data-grid">']
    for tb in tables:
        thead = "".join(f"<th>{_esc(c)}</th>" for c in tb["columns"])
        body = "".join("<tr>" + "".join(f"<td>{_esc(v)}</td>" for v in r) + "</tr>" for r in tb["rows"])
        out.append(f"""
      <div class="chart-data-card">
        <div class="chart-data-title">{_esc(tb['title'])}</div>
        <div class="table-wrap">
          <table><thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table>
        </div>
      </div>""")
    out.append("</div>")
    return "".join(out)


# --------------------------------------------------------------------------- #
# 组装 HTML
# --------------------------------------------------------------------------- #
def build_html(data: dict) -> str:
    meta = data.get("meta", {})
    charts = data.get("charts", [])
    title = meta.get("title", "数据分析报告")

    echarts_js = (ASSETS / "echarts.min.js").read_text(encoding="utf-8")
    chart_options = [chart_option(c) for c in charts]

    payload = {
        "options": chart_options,
        "chart_tables": [chart_to_table(c) for c in charts],
        "title": title,
    }
    payload_json = json.dumps(payload, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{_esc(title)} · 数据分析报告</title>
<style>
  :root {{
    --card:#ffffff; --ink:#1e293b; --muted:#64748b;
    --line:#e2e8f0; --brand:#4f46e5; --brand2:#0ea5e9;
    --risk:#dc2626; --action:#059669; --warn:#d97706;
    --radius:14px; --gap:16px;
    --pad-y:24px; --pad-x:32px;
    --h1:26px; --h2:19px; --kpi-val:30px;
  }}
  @media (max-width: 640px) {{
    :root {{
      --gap:12px; --pad-y:16px; --pad-x:16px;
      --h1:20px; --h2:17px; --kpi-val:24px; --radius:12px;
    }}
  }}
  * {{ box-sizing:border-box; }}
  html,body {{ -webkit-text-size-adjust:100%; }}
  body {{ margin:0; font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;
         background:#f1f5f9; color:var(--ink); line-height:1.6;
         font-size:15px; }}
  @media (max-width: 640px) {{ body {{ font-size:14px; }} }}
  .header {{ background:linear-gradient(135deg,#4f46e5,#0ea5e9); color:#fff;
            padding:var(--pad-y) var(--pad-x);
            padding-top:max(var(--pad-y), env(safe-area-inset-top)); }}
  .header h1 {{ margin:0 0 6px; font-size:var(--h1); word-break:break-word; }}
  .header .meta {{ opacity:.9; font-size:13px; }}
  .wrap {{ width:100%; max-width:1160px; margin:0 auto;
           padding:var(--pad-y) var(--pad-x) calc(48px + env(safe-area-inset-bottom));
           padding-top:var(--pad-y); }}
  section {{ margin-top:var(--gap); }}
  @media (max-width: 640px) {{ section {{ margin-top:24px; }} }}
  section > h2 {{ font-size:var(--h2); margin:0 0 var(--gap); padding-left:12px;
                 border-left:4px solid var(--brand); }}
  .muted {{ color:var(--muted); font-size:13px; }}

  .kpi-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:var(--gap); }}
  @media (max-width: 480px) {{ .kpi-grid {{ grid-template-columns:repeat(2,1fr); gap:10px; }} }}
  .kpi {{ background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:16px; }}
  @media (max-width: 640px) {{ .kpi {{ padding:12px; }} }}
  .kpi-label {{ color:var(--muted); font-size:13px; }}
  .kpi-value {{ font-size:var(--kpi-val); font-weight:700; margin:6px 0; color:var(--brand); word-break:break-word; }}
  .kpi-unit {{ font-size:14px; color:var(--muted); margin-left:4px; }}
  .kpi-sub {{ color:var(--muted); font-size:12px; }}

  .insight-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:var(--gap); }}
  @media (max-width: 640px) {{ .insight-grid {{ grid-template-columns:1fr; }} }}
  .insight-block {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--muted); border-radius:var(--radius); padding:16px 18px; }}
  .insight-block.conclusion {{ grid-column:1/-1; border-left-color:var(--brand); }}
  .insight-block.support {{ border-left-color:var(--brand2); }}
  .insight-block.risk {{ border-left-color:var(--risk); }}
  .insight-block.action {{ border-left-color:var(--action); }}
  .insight-block.next {{ border-left-color:var(--warn); }}
  .insight-block h3 {{ margin:0 0 8px; font-size:15px; }}
  .insight-block ul {{ margin:0; padding-left:20px; }}
  .insight-block li {{ margin:4px 0; }}
  .insight-empty {{ background:#fef9c3; border:1px solid #fde047; border-radius:12px; padding:16px; }}

  .chart-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(380px,1fr)); gap:var(--gap); }}
  @media (max-width: 640px) {{ .chart-grid {{ grid-template-columns:1fr; }} }}
  .chart-card {{ background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:14px; }}
  .chart-title {{ font-weight:600; margin-bottom:8px; font-size:14px; }}
  .chart {{ width:100%; height:340px; }}
  @media (max-width: 640px) {{ .chart {{ height:280px; }} }}

  .detail-bar {{ display:flex; align-items:center; gap:12px; margin-bottom:12px;
                 flex-wrap:wrap; }}
  #export-btn {{ background:var(--brand); color:#fff; border:0; border-radius:8px;
                padding:9px 18px; font-size:14px; cursor:pointer; -webkit-appearance:none; }}
  #export-btn:hover {{ background:#4338ca; }}
  #export-btn:active {{ background:#4338ca; }}
  .chart-data-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); gap:var(--gap); }}
  @media (max-width: 640px) {{ .chart-data-grid {{ grid-template-columns:1fr; }} }}
  .chart-data-card {{ background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:14px; }}
  .chart-data-title {{ font-weight:600; margin-bottom:8px; font-size:14px; }}
  .chart-data-card .table-wrap {{ max-height:360px; }}
  .table-wrap {{ overflow:auto; max-height:560px; background:var(--card);
                border:1px solid var(--line); border-radius:10px; -webkit-overflow-scrolling:touch; }}
  table {{ border-collapse:collapse; width:100%; font-size:13px; }}
  th,td {{ padding:8px 12px; border-bottom:1px solid var(--line); text-align:left; white-space:nowrap; }}
  thead th {{ position:sticky; top:0; background:#f8fafc; z-index:1; }}
  tbody tr:hover {{ background:#f8fafc; }}
  .footer {{ text-align:center; color:var(--muted); font-size:12px; margin-top:32px;
             padding-bottom:env(safe-area-inset-bottom); }}
</style>
</head>
<body>
  <div class="header">
    <h1>{_esc(title)} · 数据分析报告</h1>
    <div class="meta">数据规模 {meta.get('rows','?')} 行 × {meta.get('cols','?')} 列 · 单文件离线报告</div>
  </div>
  <div class="wrap">

    <section>
      <h2>核心指标</h2>
      {render_kpis(data.get('kpis'))}
    </section>

    <section>
      <h2>AI 智能洞见</h2>
      {render_insights(data.get('insights'))}
    </section>

    <section>
      <h2>可视化分析</h2>
      <div class="chart-grid">{render_charts_containers(charts)}</div>
    </section>

    <section>
      <h2>可视化分析数据</h2>
      <div class="detail-bar">
        <button id="export-btn" onclick="exportCSV()">⬇ 导出 CSV</button>
        <span class="muted">下图各表为「可视化分析」中每张图表所依据的底层数据</span>
      </div>
      {render_chart_data(charts)}
    </section>

    <div class="footer">Generated by data-analysis · 离线单文件报告</div>
  </div>

<script>{echarts_js}</script>
<script>
const __PAYLOAD__ = {payload_json};
function isMobile() {{ return window.innerWidth <= 640; }}
// 渲染图表
__PAYLOAD__.options.forEach(function(opt, i) {{
  var el = document.getElementById('chart_' + i);
  if (!el) return;
  var ch = echarts.init(el);
  // 移动端微调：tooltip 限定在容器内不溢出屏幕，grid 收紧，坐标轴标签倾斜
  if (isMobile()) {{
    if (opt.tooltip) {{ opt.tooltip.confine = true; }}
    if (opt.xAxis && opt.xAxis.axisLabel) {{ opt.xAxis.axisLabel.rotate = 45; opt.xAxis.axisLabel.interval = 0; }}
    if (opt.grid) {{ opt.grid.left = 8; opt.grid.right = 12; opt.grid.bottom = 56; opt.grid.top = 16; }}
  }}
  ch.setOption(opt);
  window.addEventListener('resize', function() {{ ch.resize(); }});
}});
// 导出 CSV（纯前端，离线可用；带 BOM 兼容 Excel）——导出各图表的底层数据
function exportCSV() {{
  var tables = __PAYLOAD__.chart_tables || [];
  var esc = function(v) {{
    v = (v === null || v === undefined) ? '' : String(v);
    return /[",\\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
  }};
  var lines = [];
  tables.forEach(function(tb, idx) {{
    if (idx > 0) lines.push('');
    lines.push('# ' + tb.title);
    lines.push(tb.columns.map(esc).join(','));
    tb.rows.forEach(function(r) {{ lines.push(r.map(esc).join(',')); }});
  }});
  var blob = new Blob(['\\ufeff' + lines.join('\\r\\n')], {{type:'text/csv;charset=utf-8'}});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = (__PAYLOAD__.title || 'data') + '_可视化分析数据.csv';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
}}
</script>
</body>
</html>"""


def main():
    # Windows 控制台默认 GBK，print 含 中文/emoji 警告会抛 UnicodeEncodeError；统一容错
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description="analysis.json (+AI洞见) → 单文件离线 HTML 报告")
    ap.add_argument("analysis", help="analyze.py 产出的 analysis.json")
    ap.add_argument("--insights", default=None, help="单独的 insights.json（可选；也可直接写进 analysis.json 的 insights 字段）")
    ap.add_argument("--out", default=None, help="HTML 输出路径，默认与数据同目录 <stem>_报告.html")
    ap.add_argument("--clean", dest="clean", action="store_true", default=True,
                    help="渲染成功后删除中间 JSON（analysis/insights/focus/schema），仅保留 HTML 与原始数据（默认开启）")
    ap.add_argument("--no-clean", dest="clean", action="store_false", help="保留中间文件，不自动清理")
    args = ap.parse_args()

    data = json.loads(Path(args.analysis).read_text(encoding="utf-8"))
    if args.insights:
        data["insights"] = json.loads(Path(args.insights).read_text(encoding="utf-8"))

    html_str = build_html(data)

    if args.out:
        out = Path(args.out)
    else:
        src = Path(data.get("meta", {}).get("source", args.analysis))
        stem = data.get("meta", {}).get("title") or src.stem
        out = src.with_name(f"{stem}_报告.html")
    out.write_text(html_str, encoding="utf-8")

    size_kb = out.stat().st_size / 1024
    warn = "" if data.get("insights") else "  ⚠️ insights 为空，报告中 AI 洞见板块是占位提示"
    print(f"[report] 已生成 → {out}  ({size_kb:.0f} KB，离线可双击打开){warn}")

    # 渲染成功后清理中间文件，仅保留 HTML 与原始数据（默认行为，可用 --no-clean 关闭）
    if args.clean:
        source_path = data.get("meta", {}).get("source", args.analysis)
        deleted = cleanup_intermediates(args.analysis, args.insights, source_path)
        print(f"[report] 已清理中间文件 {len(deleted)} 个（仅保留 HTML 与原始数据）")


if __name__ == "__main__":
    main()

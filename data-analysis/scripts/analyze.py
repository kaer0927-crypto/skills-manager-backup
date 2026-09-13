#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze.py —— CSV → analysis.json

把一份 CSV 做「自动数据分析」：
  1. 识别每列的角色（时间 / 度量 / 维度）
  2. 计算核心指标 KPI
  3. 生成可视化图表数据（趋势 / 对比 / 占比）——同时作为报告中「可视化分析数据」板块的底层数据

另有 --explore 探查模式：只识别字段语义并打印画像与候选度量 / 维度，不写任何文件，
供 Claude 拆解候选分析方向、与用户确认分析目标与方案（见 SKILL.md 第 ⓪ 步）。

输出一个 analysis.json，交给 Claude 写「AI 智能洞见」，最后由 report.py 渲染成
单文件离线 HTML 报告。

设计原则：
  - 仅依赖 pandas + 标准库
  - **只支持 CSV**；其他数据源（xlsx / api / mysql）留在 load_dataframe() 作为扩展点
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd


# --------------------------------------------------------------------------- #
# 1. 数据加载（唯一的数据源扩展点）
# --------------------------------------------------------------------------- #
def load_dataframe(source: str) -> pd.DataFrame:
    """
    加载数据源为 DataFrame。

    目前只实现 CSV / TSV。要扩展 xlsx / api / mysql 时，在这里按后缀 / 协议分派即可，
    下游流程（角色识别、KPI、图表、字段画像）完全不用改。
    """
    p = Path(source)
    if not p.exists():
        raise FileNotFoundError(f"数据文件不存在: {source}")

    suffix = p.suffix.lower()
    if suffix in (".csv", ".tsv"):
        sep = "\t" if suffix == ".tsv" else None  # sep=None + python 引擎自动嗅探分隔符
        for enc in ("utf-8-sig", "gbk", "utf-8"):
            try:
                return pd.read_csv(p, encoding=enc, sep=sep, engine="python")
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError("csv", b"", 0, 1, "无法用 utf-8-sig / gbk / utf-8 解码，请另存为 UTF-8")

    # --- 扩展点：其他数据源在此分派 ---
    # if suffix in (".xlsx", ".xls"): return pd.read_excel(p)
    # if source == "api": return load_from_api(...)
    # if source == "mysql": return load_from_mysql(...)
    raise ValueError(f"暂仅支持 CSV / TSV 数据源，收到: {suffix or source}")


# --------------------------------------------------------------------------- #
# 2. 字段角色识别
# --------------------------------------------------------------------------- #
TIME_HINTS = ("date", "time", "日期", "时间", "月份", "年月", "月", "年", "day", "week", "quarter")
ID_HINTS = ("id", "编号", "单号", "code", "编码", "no", "number", "序号")


def _looks_like_time(col: str, s: pd.Series) -> bool:
    name = str(col).lower()
    if any(h in name for h in TIME_HINTS):
        parsed = pd.to_datetime(s, errors="coerce")
        if parsed.notna().mean() >= 0.7:
            return True
    # 名字没提示，但整列能解析成日期
    if s.dtype == object:
        parsed = pd.to_datetime(s, errors="coerce")
        if parsed.notna().mean() >= 0.9:
            return True
    return False


def _looks_like_id(col: str, s: pd.Series) -> bool:
    name = str(col).lower()
    if any(h in name for h in ID_HINTS):
        return True
    # 近乎唯一 → 更像主键，但**仅限整数型**：浮点列（金额/价格/度量）几乎从不是 ID
    if pd.api.types.is_numeric_dtype(s) and len(s) > 20:
        nonnull = s.dropna()
        is_int = pd.api.types.is_integer_dtype(s) or (len(nonnull) > 0 and (nonnull % 1 == 0).all())
        if is_int and s.nunique(dropna=True) >= 0.95 * len(s):
            return True
    return False


# 业务金额类度量优先作「主度量」（用于趋势 / 对比 / 占比 / KPI 头卡）
MEASURE_HINTS = ("金额", "销售额", "销额", "营收", "收入", "gmv", "amount", "value", "销售")


def _sort_measures(measures) -> list:
    return sorted(measures, key=lambda c: 0 if any(h in str(c).lower() for h in MEASURE_HINTS) else 1)


# --------------------------------------------------------------------------- #
# 2.2 字段语义分析——拿到数据后先逐列推断业务语义（不只是 time/measure/dimension
#     三类粗角色，而是金额 / 单价 / 数量 / 标识 / 分类 / 日期 等细粒度标签）。
#     若用户提供了字段语义说明（schema.json），以其为权威依据，覆盖自动推断。
# --------------------------------------------------------------------------- #
SEMANTIC_AMOUNT_HINTS = ("金额", "销额", "销售额", "营收", "收入", "gmv", "amount", "value", "总价", "小计", "余额")
SEMANTIC_PRICE_HINTS = ("单价", "价格", "price", "cost", "成本")
SEMANTIC_QTY_HINTS = ("数量", "qty", "count", "件数", "库存", "变动", "天数", "age", "days")


def _infer_semantic(col: str, s: pd.Series, role: str) -> str:
    """在已知 role 的基础上，推断更细的业务语义标签。"""
    name = str(col)
    nl = name.lower()
    if role == "time":
        return "datetime"
    if role == "dimension":
        if any(h in nl for h in ID_HINTS):
            return "identifier"
        n = s.nunique(dropna=True)
        if n <= 2:
            return "flag"
        if n <= 50:
            return "category"
        return "text"
    # role == measure：按列名细分为金额 / 单价 / 数量 / 通用度量
    if any(h in nl for h in SEMANTIC_AMOUNT_HINTS) or "金额" in name:
        return "amount"
    if any(h in nl for h in SEMANTIC_PRICE_HINTS) or "单价" in name:
        return "price"
    if any(h in nl for h in SEMANTIC_QTY_HINTS):
        return "quantity"
    return "measure"


SCHEMA_NOTES = (
    "schema.json（可选，用户字段语义说明）格式：\n"
    '  {"<列名>": {"role": "measure|dimension|time", "semantic": "amount|price|quantity|...|", "unit": "元", "desc": "业务含义"}}\n'
    "  每个字段任一键均可缺省，缺省键自动推断；用户提供的键为权威依据，覆盖自动推断。\n"
    "  Claude 也可把用户的自然语言字段说明转译成此 JSON 后传入。"
)


def load_schema(path: str | None) -> dict:
    """读取用户字段语义说明；空路径或不存在返回 {}。格式见 SCHEMA_NOTES。"""
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        print(f"[analyze] ⚠️ schema 文件不存在，忽略: {path}")
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            print("[analyze] ⚠️ schema 顶层不是对象，忽略")
            return {}
        return data
    except json.JSONDecodeError as e:
        print(f"[analyze] ⚠️ schema JSON 解析失败({e})，忽略，回退自动推断")
        return {}


# --------------------------------------------------------------------------- #
# 2.1 用户分析意图（focus）——由 Claude 把自然语言解析成结构化配置后传入
# --------------------------------------------------------------------------- #
FOCUS_SCHEMA_NOTES = (
    "focus.json 可选键：\n"
    "  goal          : str  ——分析目标（仅记录进 meta，供写洞见参考）\n"
    "  measures      : list ——指定主度量（按此顺序优先；必须为数值列）\n"
    "  dimensions    : list ——指定优先切分维度（必须为维度列；高基数会按 topn 截断）\n"
    "  time_col      : str  ——指定用作趋势的时间列\n"
    "  granularity   : str  ——趋势粒度 D / ME / QE（不填则按跨度自动）\n"
    "  topn          : int  ——对比 / 占比图每张最多展示项数，默认 12\n"
    "  max_charts    : int  ——图表总数软上限（核心图优先保留）；不填 / 0 = 不限，张数按数据灵活生成\n"
    "未填或填写无效的键回退到自动识别，不会报错。"
)


def load_focus(path: str | None) -> dict:
    """读取用户意图配置；空路径或文件不存在返回 {}。"""
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        print(f"[analyze] ⚠️ focus 文件不存在，忽略: {path}")
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[analyze] ⚠️ focus JSON 解析失败({e})，忽略，回退自动识别")
        return {}


def apply_focus(focus: dict, roles: dict):
    """把 focus 叠加到自动识别结果上，返回 (measures, priority_dims, times, granularity, topn)。

    指定但角色不符的列会被静默过滤（回退到自动识别），保证确定性脚本不因用户笔误崩溃。
    """
    auto_measures = _sort_measures([c for c, r in roles.items() if r == "measure"])
    auto_dims = [c for c, r in roles.items() if r == "dimension"]
    auto_times = [c for c, r in roles.items() if r == "time"]

    # 度量：用户指定优先，保留其顺序，过滤掉非数值列
    if focus.get("measures"):
        picked = [c for c in focus["measures"] if roles.get(c) == "measure"]
        measures = picked + [m for m in auto_measures if m not in picked]
    else:
        measures = auto_measures

    # 优先维度：用户指定靠前（不限基数，groupby 后按 topn 截断）
    if focus.get("dimensions"):
        picked = [c for c in focus["dimensions"] if roles.get(c) == "dimension"]
        priority_dims = picked + [d for d in auto_dims if d not in picked]
    else:
        priority_dims = auto_dims

    # 时间列：用户指定若确为 time 角色则提到首位
    tc = focus.get("time_col")
    if tc and roles.get(tc) == "time":
        times = [tc] + [t for t in auto_times if t != tc]
    else:
        times = auto_times

    gran = str(focus.get("granularity", "")).upper()
    granularity = gran if gran in ("D", "ME", "QE") else None
    try:
        topn = int(focus.get("topn", 12))
    except (TypeError, ValueError):
        topn = 12
    # 用户显式指定且角色合法的维度（build_charts 对其放宽基数限制）
    focus_dims = [c for c in (focus.get("dimensions") or []) if roles.get(c) == "dimension"]
    return measures, priority_dims, times, granularity, topn, focus_dims


def classify_columns(df: pd.DataFrame) -> dict:
    """返回 {列名: 'time'|'measure'|'dimension'}。"""
    roles = {}
    for col in df.columns:
        s = df[col]
        if _looks_like_time(col, s):
            roles[col] = "time"
        elif _looks_like_id(col, s):
            roles[col] = "dimension"
        elif pd.api.types.is_numeric_dtype(s):
            roles[col] = "measure"
        else:
            roles[col] = "dimension"
    return roles


VALID_ROLES = ("time", "measure", "dimension")


def apply_schema(df: pd.DataFrame, roles: dict, schema: dict | None) -> tuple[dict, dict, dict]:
    """用用户字段语义说明（schema）覆盖自动识别结果。

    返回 (roles, semantics, descs)：
      - roles:     {列名: role}        ——用户指定的 role 覆盖自动结果（影响 KPI/图表/焦点过滤）
      - semantics: {列名: semantic}    ——细粒度业务语义标签
      - descs:     {列名: desc/unit}   ——用户给的业务含义/单位（仅记录，供写洞见参考）
    schema 中出现的列名必须在 df 里存在，否则忽略；role 取值不合法时忽略该键。
    """
    schema = schema or {}
    roles = dict(roles)
    semantics, descs = {}, {}
    for col in df.columns:
        s = df[col]
        spec = schema.get(str(col))
        if isinstance(spec, dict):
            r = spec.get("role")
            if r in VALID_ROLES:
                roles[col] = r  # 用户语义为权威依据，覆盖自动识别
            sem = spec.get("semantic")
            semantics[col] = sem if isinstance(sem, str) and sem else _infer_semantic(col, s, roles[col])
            desc = spec.get("desc") or spec.get("unit")
            if isinstance(desc, str) and desc:
                descs[col] = desc
        else:
            semantics[col] = _infer_semantic(col, s, roles[col])
    return roles, semantics, descs


def _fmt_num(v) -> str:
    """给 KPI 卡片用的人类可读数字。"""
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    a = abs(v)
    if a >= 1e8:
        return f"{v / 1e8:.2f} 亿"
    if a >= 1e4:
        return f"{v / 1e4:.2f} 万"
    if a == int(a):
        return f"{int(v):,}"
    return f"{v:,.2f}"


# --------------------------------------------------------------------------- #
# 3. KPI / 图表
# --------------------------------------------------------------------------- #
def build_kpis(df, roles, measures):
    kpis = [{"label": "总记录数", "value": _fmt_num(len(df)), "unit": "行", "sub": f"{len(df.columns)} 个字段"}]
    for m in measures[:3]:
        # 防御：schema 误把非数值列标成 measure 时跳过，避免 sum/mean 崩溃
        if m not in df.columns or not pd.api.types.is_numeric_dtype(df[m]):
            continue
        col = df[m].dropna()
        if col.empty:
            continue
        total, avg = col.sum(), col.mean()
        kpis.append({
            "label": f"{m} · 合计",
            "value": _fmt_num(total),
            "unit": "",
            "sub": f"均值 {_fmt_num(avg)} · 最大 {_fmt_num(col.max())}",
        })
    return kpis


def build_charts(df, roles, measures, dimensions, times, topn=12, granularity=None, focus_dims=None, max_charts=0):
    """生成图表数据——张数不设固定上限，按数据实际情况灵活生成。

    编排（核心图在前，便于 max_charts 截尾时不伤主图）：
      1. 主度量趋势（时间 × 主度量）
      2. 每个适合分组的维度 × 主度量的对比柱状；主维度及低基数（≤10 类）维度追加占比饼图
      3. 其余度量的趋势（数据有多个度量时逐个补齐）
    dimensions 已按用户意图排好优先级（focus 指定的列在前）。
    focus_dims：用户显式指定的维度，放宽基数限制（靠 head(topn) 截断），其余守 cap 规则。
    granularity 非 None 时强制覆盖趋势粒度，否则按时间跨度自动选 D/ME/QE。
    max_charts：软上限（focus.json 可配）；0 表示不限。
    """
    charts = []
    # 主度量取第一个「真正可求和」的数值列（schema 误标非数值列时自动跳过，避免崩溃）
    numeric_measures = [m for m in measures if m in df.columns and pd.api.types.is_numeric_dtype(df[m])]
    main_measure = numeric_measures[0] if numeric_measures else None
    focus_dims = focus_dims or []

    # 选「适合分组」的维度：排除高基数列（如接近唯一的 ID），优先基数适中的
    cap = max(2, min(30, len(df) // 2))
    auto_good = [d for d in dimensions if 2 <= df[d].nunique(dropna=True) <= cap]
    # 用户显式指定的维度强制排最前（放宽基数限制，靠 head(topn) 截断展示），再补其余
    good_dims = [d for d in focus_dims if df[d].nunique(dropna=True) >= 2]
    good_dims += [d for d in auto_good if d not in good_dims]

    # 趋势图公共部件：时间列解析一次、粒度定一次，供各度量复用
    _trend = None
    if times:
        t = times[0]
        tt = pd.to_datetime(df[t], errors="coerce")
        valid = tt.dropna()
        if granularity:
            freq = granularity
        else:
            span = (valid.max() - valid.min()).days if not valid.empty else 0
            freq = "D" if span <= 90 else ("ME" if span <= 1500 else "QE")

        def _trend(measure):
            tmp = pd.DataFrame({t: tt, measure: df[measure]}).dropna(subset=[t])
            if tmp.empty:
                return None
            g = tmp.groupby(pd.Grouper(key=t, freq=freq))[measure].sum().dropna()
            if len(g) < 2:
                return None
            return {
                "type": "line",
                "title": f"{measure} 趋势 ({freq})",
                "x": [d.strftime("%Y-%m-%d") for d in g.index],
                "series": [{"name": measure, "data": [round(float(v), 2) for v in g.values]}],
            }

    # 3.1 趋势（主度量）
    if _trend and main_measure:
        c = _trend(main_measure)
        if c:
            charts.append(c)

    # 3.2 对比 / 占比：每个适合分组的维度 × 主度量（张数随维度数灵活）
    if main_measure:
        for idx, d in enumerate(good_dims):
            g = df.groupby(d)[main_measure].sum().sort_values(ascending=False).head(topn)
            if len(g) < 2:
                continue
            charts.append({
                "type": "bar",
                "title": f"各 {d} 的 {main_measure}（Top {len(g)}）",
                "x": [str(i) for i in g.index],
                "series": [{"name": main_measure, "data": [round(float(v), 2) for v in g.values]}],
            })
            # 3.3 占比：主维度必出饼图；其余低基数维度（≤10 类，饼图仍可读）也出
            if idx == 0 or df[d].nunique(dropna=True) <= 10:
                charts.append({
                    "type": "pie",
                    "title": f"{main_measure} 按 {d} 占比（Top {len(g)}）",
                    "data": [{"name": str(i), "value": round(float(v), 2)} for i, v in g.items()],
                })

    # 3.4 趋势（其余度量）：有多个度量时逐个补趋势
    if _trend:
        for m in numeric_measures[1:]:
            c = _trend(m)
            if c:
                charts.append(c)

    # 3.5 没有度量时：每个适合分组的维度出记录数柱状
    if not charts and (good_dims or dimensions):
        for d in (good_dims or dimensions[:1]):
            g = df[d].value_counts().head(topn)
            if g.empty:
                continue
            charts.append({
                "type": "bar",
                "title": f"各 {d} 记录数（Top {len(g)}）",
                "x": [str(i) for i in g.index],
                "series": [{"name": "记录数", "data": [int(v) for v in g.values]}],
            })

    # 软上限：仅当 focus.max_charts 指定时截断（核心图排前，截尾不伤主图）
    if max_charts and len(charts) > max_charts:
        charts = charts[:max_charts]
    return charts


def build_profile(df, roles, semantics=None, descs=None):
    semantics = semantics or {}
    descs = descs or {}
    cols = []
    for col in df.columns:
        s = df[col]
        info = {
            "name": str(col),
            "role": roles[col],
            "semantic": semantics.get(col, ""),
            "dtype": str(s.dtype),
            "nulls": int(s.isna().sum()),
            "unique": int(s.nunique(dropna=True)),
        }
        if descs.get(col):
            info["desc"] = descs[col]
        if roles[col] == "measure" and pd.api.types.is_numeric_dtype(s):
            c = s.dropna()
            if not c.empty:
                info["stats"] = {
                    "sum": float(c.sum()), "mean": float(c.mean()),
                    "min": float(c.min()), "max": float(c.max()),
                }
            else:
                info["samples"] = [str(x) for x in s.dropna().unique()[:5]]
        else:
            info["samples"] = [str(x) for x in s.dropna().unique()[:5]]
        cols.append(info)
    return cols


# --------------------------------------------------------------------------- #
# 3.5 探查模式（--explore）——分析方案确认环节的数据依据
#     只做字段语义识别与画像打印，不写 analysis.json。Claude 读终端输出后，
#     拆解候选分析指标 / 维度，与用户提问式确认分析目标，再跑完整分析。
# --------------------------------------------------------------------------- #
def explore(source: str, schema: dict | None = None) -> None:
    df = load_dataframe(source)
    roles_auto = classify_columns(df)
    roles, semantics, descs = apply_schema(df, roles_auto, schema)

    print(f"[explore] {len(df)} 行 × {len(df.columns)} 列  来源: {Path(source).resolve()}")
    print("[explore] 逐列画像（列名 | role@semantic | dtype | 非空/唯一 | 统计或样本）:")
    for col in df.columns:
        s = df[col]
        line = (f"  {col} | {roles[col]}@{semantics.get(col) or '-'} | {s.dtype}"
                f" | 非空{int(s.notna().sum())}/唯一{int(s.nunique(dropna=True))}")
        if roles[col] == "measure" and pd.api.types.is_numeric_dtype(s):
            c = s.dropna()
            if not c.empty:
                line += f" | 合计{_fmt_num(c.sum())} 均值{_fmt_num(c.mean())} 范围[{_fmt_num(c.min())}, {_fmt_num(c.max())}]"
        else:
            line += " | 样本: " + ", ".join(str(x) for x in s.dropna().unique()[:5])
        if descs.get(col):
            line += f" | {descs[col]}"
        print(line)

    measures = _sort_measures([c for c, r in roles.items() if r == "measure"])
    dims = [c for c, r in roles.items() if r == "dimension"]
    times = [c for c, r in roles.items() if r == "time"]
    cap = max(2, min(30, len(df) // 2))
    group_dims = [d for d in dims if 2 <= df[d].nunique(dropna=True) <= cap]
    id_dims = [d for d in dims if d not in group_dims]
    print(f"[explore] 候选度量: {measures}")
    print(f"[explore] 适合分组的维度（基数适中）: {group_dims}")
    print(f"[explore] 高基数 / 标识类维度（默认不用于分组）: {id_dims}")
    print(f"[explore] 时间列: {times}")
    if times:
        t = pd.to_datetime(df[times[0]], errors="coerce").dropna()
        if not t.empty:
            print(f"[explore] 时间跨度: {t.min().date()} ~ {t.max().date()}")
    print("[explore] 未写出任何文件。下一步：Claude 基于以上画像拆解候选分析指标与维度，"
          "与用户确认分析目标与方案后生成 focus.json（如需纠正字段语义则加 schema.json），再运行完整分析")


# --------------------------------------------------------------------------- #
# 4. 主流程
# --------------------------------------------------------------------------- #
def analyze(source: str, title: str | None, focus: dict | None = None, schema: dict | None = None) -> dict:
    df = load_dataframe(source)
    roles_auto = classify_columns(df)
    # 字段语义分析：用户提供的 schema 为权威依据，覆盖自动识别的 role / semantic
    roles, semantics, descs = apply_schema(df, roles_auto, schema)
    focus = focus or {}
    measures, dimensions, times, granularity, topn, focus_dims = apply_focus(focus, roles)
    try:
        max_charts = max(0, int(focus.get("max_charts", 0)))
    except (TypeError, ValueError):
        max_charts = 0
    # meta 里同时保留「全部」角色，便于写洞见时参考；用户意图单独存 focus 摘要
    all_measures = _sort_measures([c for c, r in roles.items() if r == "measure"])
    all_dims = [c for c, r in roles.items() if r == "dimension"]
    all_times = [c for c, r in roles.items() if r == "time"]

    return {
        "meta": {
            "source": str(Path(source).resolve()),
            "title": title or Path(source).stem,
            "rows": int(len(df)),
            "cols": int(len(df.columns)),
            "roles": {"time": all_times, "measure": all_measures, "dimension": all_dims},
            # 字段语义：用户提供的 schema 为权威依据时记 true，提示写洞见时以用户语义为准
            "field_semantics": {
                "user_provided": bool(schema),
                "source": "schema.json" if schema else "auto-inferred",
            },
            "analysis": {
                "measures": measures,
                "dimensions": dimensions,
                "time_col": times[0] if times else None,
                "granularity": granularity,
                "topn": topn,
                "goal": focus.get("goal"),
            },
        },
        "kpis": build_kpis(df, roles, measures),
        "charts": build_charts(df, roles, measures, dimensions, times, topn, granularity, focus_dims, max_charts),
        "profile": build_profile(df, roles, semantics, descs),
        # 占位：Claude 以数据分析专家视角填充（见 SKILL.md）
        "insights": None,
    }


def main():
    # Windows 控制台默认 GBK，print 含 中文/emoji 警告会抛 UnicodeEncodeError 中断流程；统一容错
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description="CSV → analysis.json（自动分析）")
    ap.add_argument("source", help="CSV / TSV 文件路径")
    ap.add_argument("--title", default=None, help="报告标题，默认取文件名")
    ap.add_argument("--out", default=None, help="analysis.json 输出路径，默认与数据同目录")
    ap.add_argument("--focus", default=None, help="用户意图配置 focus.json（由 Claude 从自然语言解析）")
    ap.add_argument("--schema", default=None, help="用户字段语义说明 schema.json（由 Claude 从自然语言解析；为权威依据，覆盖自动识别）")
    ap.add_argument("--explore", action="store_true",
                    help="探查模式：只识别字段语义并打印画像与候选度量/维度，不写 analysis.json（供与用户确认分析方案）")
    args = ap.parse_args()

    focus = load_focus(args.focus)
    schema = load_schema(args.schema)
    if args.explore:
        explore(args.source, schema)
        return
    result = analyze(args.source, args.title, focus, schema)

    out = Path(args.out) if args.out else Path(args.source).with_name(Path(args.source).stem + ".analysis.json")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    m = result["meta"]
    print(f"[analyze] {m['rows']} 行 × {m['cols']} 列")
    print(f"[analyze] 角色  时间={m['roles']['time']}  度量={m['roles']['measure']}  维度={m['roles']['dimension']}")
    sem_src = m["field_semantics"]["source"]
    print(f"[analyze] 字段语义  依据={sem_src}（{'以用户提供的字段语义为准' if m['field_semantics']['user_provided'] else '自动推断'}）")
    # 逐列语义一览（role@semantic），便于核验
    sem_line = "  ".join(f"{p['name']}:{p['role']}@{p['semantic'] or '-'}" for p in result["profile"])
    print(f"[analyze] 字段语义  {sem_line}")
    a = m["analysis"]
    print(f"[analyze] 本次分析  主度量={a['measures'][:3]}  优先维度={a['dimensions'][:3]}  时间列={a['time_col']}  粒度={a['granularity'] or '自动'}  TopN={a['topn']}")
    if a.get("goal"):
        print(f"[analyze] 分析目标  {a['goal']}")
    print(f"[analyze] 图表 {len(result['charts'])} 张 · KPI {len(result['kpis'])} 个")
    print(f"[analyze] 已写出 → {out}")
    print(f"[analyze] 下一步：Claude 读取该文件，以数据分析专家视角写 insights，再跑 report.py")


if __name__ == "__main__":
    sys.exit(main())

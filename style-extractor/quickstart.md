# 快速上手 / Quickstart（一键调用示例）

下面是可直接复制的常用调用方式。

**Skill 名称**
- **中文名**：网页风格提取器
- **英文名**：Web Style Extractor
- **调用命令（skill 名）**：`/style-extractor`（旧名 `/vibepm-style-extractor` 仍走本技能；其余为自然语言需求描述）

## 1) URL 输入（完整提取 + 提示词 + 评分）

```text
/style-extractor
请分析这个网页并输出完整风格包（含评分）：
https://example.com
目标页面类型：SaaS 仪表盘
目标用户：中小团队运营人员
```

## 2) URL 输入（仅提取，不生成提示词）

```text
/style-extractor analyze
请只提取该网站的风格 DNA 与设计 Tokens（Design Tokens），不要生成提示词：
https://example.com
```

## 3) 已有提取结果（仅生成提示词）

```text
/style-extractor prompt
基于以下风格提取结果，生成基础 / 组件 / 变体三套中文提示词并按 scoring-rubric 输出中文评分区块：
[在这里粘贴你的 Style Snapshot + Tokens + Principles]
```

## 4) 截图输入（适合视觉参考站）

```text
/style-extractor
请基于我上传的网页截图提取风格并生成可复用提示词。
如果参数不确定，用 ~ 标注估算值，并输出评分与修正建议。
```

## 5) 局部组件输入（只分析按钮/卡片/表单）

```text
/style-extractor analyze
只分析这个页面的按钮、卡片、表单三类组件：
- 按钮尺寸体系、状态与视觉差异
- 卡片边框/阴影/圆角层级
- 表单输入框与焦点样式
最后给出可复用 token。
```

## 6) 生成同风格多变体（A/B 测试）

```text
/style-extractor prompt
基于现有风格 DNA 生成 3 个变体：
A: 更高转化（按钮更突出）
B: 更内容导向（弱化营销感）
C: 更高端（降低饱和度，提升留白）
要求：保留相同布局体系和组件几何规则，并分别评分。
```

## 7) 质量门禁用法（强制 80 分以上）/ Quality Gate Usage

```text
/style-extractor
请执行完整流程，并将评分作为门禁：
- 低于 80 分不得通过
- 必须输出「优先修订（三项）」
- 直接给出修订版，直到结论为「通过」
```

## 常用补充参数（建议附带）/ Common Optional Parameters

- 页面类型：官网 / 落地页 / 后台 / 电商 / 博客
- 用户类型：新手 / 专业用户 / 管理员 / 消费者
- 终端优先级：移动优先 / 桌面优先 / 双端一致
- 品牌关键词：例如“理性、可信、克制”
- 禁用项：明确你不想要的视觉元素

## 结果检查清单 / Result Checklist

拿到结果后，优先看这 5 点：
1. Token 是否可直接实现（不是纯形容词）
2. 按钮状态是否完整（hover/focus/active）
3. 布局与间距是否有明确节奏
4. 是否有防跑偏规则（避免项）
5. 总分是否 >= 80

# 兰州公物仓资产批量导入模板 Skill

基于原始资产批量导入模板建立的格式控制技能。

## 快速使用

调用技能后，先确认本次模板要与哪个功能表单对齐，以及是否提供了对应字段说明。未说明时必须先反问，不得自行推断。

```bash
python3 scripts/generate_template.py --output ./兰州公物仓_资产批量导入模板.xlsx
python3 scripts/validate_template.py ./兰州公物仓_资产批量导入模板.xlsx
```

## 设计

- `assets/` 保存黄金母版
- `references/template-spec.md` 保存完整格式规范
- `scripts/generate_template.py` 只做安全复制，不重建样式
- `scripts/validate_template.py` 对表头、富文本、样式、列宽、行高、合并单元格和禁止项做严格校验

## 测试

```bash
python3 -m unittest discover -s tests -v
```

## 约束

模板固定 35 列、四层表头、14 个必填列、1,109 行预格式化空白数据行。不得擅自新增下拉、筛选、表格对象、示例数据或业务字段。

生成、修改或校验前，必须先由用户确认目标功能表单和字段对齐范围；对话中缺少说明时，应先反问用户，不得根据文件名或现有字段自行猜测。

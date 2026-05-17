# 合规监管文档智能分析 — SDD 规范文档

> **SDD 第一步**：在写任何代码之前，先定义清楚 Agent 的行为规范。

---

## 1. 业务场景

金融监管机构（MAS / FCA / CSRC）发布新规或修订现有规则时，合规分析师需要：
1. 获取最新监管文档
2. 对比新旧版本，识别变更点
3. 评估变更对企业现有 SOP 的影响
4. 生成结构化影响报告

**目标**：用 Agent 自动化步骤 1-4，分析师只需审核最终报告。

---

## 2. 输入规范

### 2.1 支持的文档格式
- PDF（监管机构官方文件）
- HTML（网页发布的通知/公告）
- TXT / Markdown（内部合规手册）

### 2.2 输入字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `document_path` | string | 是 | 新规文档路径或 URL |
| `baseline_path` | string | 否 | 旧版规则路径（用于变更对比） |
| `scope` | string | 否 | 分析范围（如 "AML", "KYC", "Data Privacy"） |
| `company_sop_path` | string | 否 | 企业现有 SOP 文档路径 |

---

## 3. 输出规范

### 3.1 合规影响报告结构

```json
{
  "report_id": "CR-2026-0316-001",
  "generated_at": "2026-03-16T10:30:00Z",
  "source_document": "MAS-Notice-648-Amendment-2026.pdf",
  "summary": "一句话概述本次变更的核心内容",
  "changes": [
    {
      "change_id": "CHG-001",
      "section": "Section 3.2 - Customer Due Diligence",
      "change_type": "amendment | addition | deletion",
      "description": "变更内容描述",
      "original_text": "原文引用（如有）",
      "new_text": "新文引用",
      "impact_level": "high | medium | low",
      "impact_analysis": "对企业现有流程的具体影响",
      "recommended_action": "建议采取的行动",
      "confidence": 0.95,
      "source_reference": "Page 12, Paragraph 3"
    }
  ],
  "overall_impact": "high | medium | low",
  "action_items": [
    {
      "priority": 1,
      "action": "具体行动项",
      "deadline_suggestion": "建议完成时间",
      "responsible_team": "建议负责团队"
    }
  ],
  "review_required": true,
  "review_reason": "存在高影响变更，需人工确认"
}
```

### 3.2 输出质量标准

- [ ] 每条变更必须附带 `source_reference`（原文出处）
- [ ] `confidence` 低于 0.8 的结论必须标记 `review_required: true`
- [ ] `impact_level: high` 的变更必须有 `recommended_action`
- [ ] 报告必须包含 `overall_impact` 总体评估
- [ ] 所有引用文本必须可追溯到原始文档

---

## 4. 质量评估规范

Agent 输出必须通过以下自动化检查：

| 检查项 | 规则 | 不通过处理 |
|--------|------|-----------|
| 引用完整性 | 每条 change 都有 source_reference | 标记为待补充 |
| 置信度阈值 | confidence >= 0.8 | 标记为待人工复核 |
| 影响覆盖 | high 级变更必须有 action | 阻断，要求补充 |
| 格式合规 | 输出 JSON 符合上述 schema | 阻断，重新生成 |
| 幻觉检测 | 引用文本必须在原文中存在 | 标记为疑似幻觉 |

---

## 5. Agent 行为约束

- **不得**生成原文中不存在的引用
- **不得**对 impact_level 为 high 的变更自动做出最终判断——必须标记为 review_required
- **必须**在无法解析文档时返回明确的错误信息，而非编造内容
- **必须**保留完整的推理链日志（reasoning trace）

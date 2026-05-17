# 会议纪要自动生成 Agent — SDD 规范文档

> **SDD 第一步**：明确定义会议纪要 Agent 的输入、输出和质量标准。

---

## 1. 业务场景

LSEG 内部团队会议频繁，会议纪要整理耗时。Agent 自动完成：
1. 接收会议记录文本（语音转文字后的原始文本）
2. 提取会议要点、决策、行动项
3. 按标准模板生成结构化纪要
4. 自动分配行动项责任人和截止日期

---

## 2. 输入规范

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `transcript` | string | 是 | 会议记录文本（转写后的文字） |
| `meeting_title` | string | 否 | 会议标题 |
| `participants` | list[string] | 否 | 参会人员列表 |
| `meeting_date` | string | 否 | 会议日期 |

---

## 3. 输出规范

### 3.1 会议纪要结构

```json
{
  "meeting_title": "string",
  "date": "2026-03-16",
  "participants": ["Alice", "Bob"],
  "duration_minutes": 45,
  "summary": "2-3 句话的会议总结",
  "key_points": [
    {
      "topic": "讨论主题",
      "discussion": "讨论要点摘要",
      "decision": "最终决定（如有）"
    }
  ],
  "action_items": [
    {
      "id": "AI-001",
      "description": "行动项描述",
      "assignee": "负责人",
      "deadline": "2026-03-20",
      "priority": "high | medium | low"
    }
  ],
  "next_meeting": "下次会议安排（如有提及）"
}
```

### 3.2 输出质量标准

- [ ] summary 不超过 100 字
- [ ] 每个 action_item 必须有 assignee（如文本中未提及，标注为 "TBD"）
- [ ] key_points 至少提取 2 个主题
- [ ] 不得添加会议中未讨论的内容
- [ ] deadline 必须为具体日期（若原文仅说"下周"，转换为具体日期）

---

## 4. Agent 行为约束

- **不得**编造会议中未提及的决策或行动项
- **必须**保持中立客观，不添加主观评价
- 对模糊的行动项，用 "TBD" 标注而非猜测

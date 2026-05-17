# 多 Agent 工单审查流水线 — SDD 规范文档

> **SDD 第一步**：在写任何代码之前，先定义清楚每个 Agent 的职责、通信协议和质量标准。

---

## 1. 业务场景

LSEG 内部的缺陷工单系统中，开发者提交的 bug report 质量参差不齐。常见问题：
- 复现步骤缺失或模糊
- 环境信息不完整
- 优先级标注不当（P1 标成 P3，或反之）
- 类似问题历史上已解决但未被引用

**目标**：构建多 Agent 协作流水线，自动审查工单质量，匹配历史知识，输出整改建议。

---

## 2. Agent 职责规范

### Agent 1: 工单解析器（Ticket Parser）

| 项目 | 规范 |
|------|------|
| **输入** | 原始工单文本（标题 + 描述） |
| **输出** | 结构化工单对象（JSON） |
| **职责** | 从非结构化文本中提取关键字段 |

输出 schema：
```json
{
  "ticket_id": "string",
  "title": "string",
  "component": "string | null",
  "environment": "string | null",
  "severity_claimed": "P1 | P2 | P3 | P4 | null",
  "reproduction_steps": ["step1", "step2"],
  "expected_behavior": "string | null",
  "actual_behavior": "string | null",
  "attachments_mentioned": true | false
}
```

### Agent 2: 质量检测器（Quality Inspector）

| 项目 | 规范 |
|------|------|
| **输入** | Agent 1 输出的结构化工单 |
| **输出** | 质量评估报告 |
| **职责** | 检查工单信息完整性和优先级合理性 |

检查项：
| 检查 | 规则 | 严重等级 |
|------|------|---------|
| 复现步骤 | reproduction_steps 至少 2 步 | error |
| 环境信息 | environment 不为 null | warning |
| 组件标注 | component 不为 null | warning |
| 预期行为 | expected_behavior 不为 null | error |
| 优先级合理性 | 根据描述中的关键词评估是否与 severity_claimed 匹配 | info |

输出 schema：
```json
{
  "ticket_id": "string",
  "quality_score": 0-100,
  "issues": [
    {
      "field": "reproduction_steps",
      "severity": "error | warning | info",
      "message": "问题描述",
      "suggestion": "修改建议"
    }
  ],
  "severity_assessment": {
    "claimed": "P2",
    "recommended": "P1",
    "reason": "评估理由"
  },
  "pass": true | false
}
```

### Agent 3: 知识库匹配器（Knowledge Matcher）

| 项目 | 规范 |
|------|------|
| **输入** | Agent 1 输出的结构化工单 |
| **输出** | 历史匹配结果 |
| **职责** | 从历史工单库中检索类似问题和解决方案 |

输出 schema：
```json
{
  "ticket_id": "string",
  "matches": [
    {
      "historical_id": "TICKET-1234",
      "similarity_score": 0.92,
      "title": "历史工单标题",
      "resolution": "解决方案摘要",
      "is_duplicate": false
    }
  ],
  "potential_duplicate": true | false
}
```

---

## 3. 协作规范（Agent 间通信）

```
[原始工单]
     │
     ▼
┌─────────────┐
│ Agent 1     │ → 结构化工单 JSON
│ 工单解析器   │
└──────┬──────┘
       │
   ┌───┴───┐
   ▼       ▼
┌──────┐ ┌──────┐
│ Ag.2 │ │ Ag.3 │  ← 并行执行
│ 质检  │ │ 知识  │
└──┬───┘ └──┬───┘
   │        │
   ▼        ▼
┌─────────────┐
│  结果合并    │ → 最终审查报告
│  + 人工审批  │
└─────────────┘
```

### 通信协议
- Agent 间传递 **结构化 JSON**（报告式通信），不传原始工单文本
- 每个 Agent 只接收自己需要的字段（上下文隔离）
- Agent 2 和 Agent 3 **并行执行**（无依赖关系）

---

## 4. 风险分层规范（Human-in-the-Loop）

| 条件 | 处理 |
|------|------|
| quality_score >= 80 且无 error 级问题 | 自动通过 |
| quality_score 60-79 或有 warning | 生成建议，抄送工单作者 |
| quality_score < 60 或有 error | **需人工审批**：通知 Tech Lead |
| potential_duplicate == true | **需人工确认**：是否与历史工单重复 |
| severity 被重新评估为 P1 | **需人工确认**：是否需要紧急处理 |

---

## 5. 最终审查报告输出规范

```json
{
  "ticket_id": "TICKET-5678",
  "review_timestamp": "2026-03-16T14:30:00Z",
  "parsed_ticket": { ... },
  "quality_report": { ... },
  "knowledge_matches": { ... },
  "final_verdict": "approved | needs_revision | needs_human_review",
  "auto_comments": [
    "建议补充复现步骤（当前仅1步）",
    "发现类似历史工单 TICKET-1234，请确认是否重复"
  ],
  "auto_labels": ["needs-repro-steps", "potential-duplicate"]
}
```

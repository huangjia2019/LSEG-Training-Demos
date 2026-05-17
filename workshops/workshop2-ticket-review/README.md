# Workshop 2: 多 Agent 工单审查流水线

> **SDD 实践**：规范定义每个 Agent 的职责边界和通信协议，LangGraph 负责编排。

## 场景

LSEG 内部缺陷工单系统中，三个 Agent 协作审查工单质量：
1. **Agent 1 (Parser)**: 从非结构化文本中提取结构化字段
2. **Agent 2 (Quality)**: 检查信息完整性 + 优先级合理性
3. **Agent 3 (Knowledge)**: 从历史工单库中匹配类似问题

最终汇总后按风险分层决策：自动通过 / 需修改 / 需人工审批。

## 快速开始

```bash
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env

cd src
python main.py  # Demo 模式，演示三种工单场景
```

## 交互式可视化 Demo

运行 CLI 之后，可以直接打开：

```bash
open visual/index.html
```

这页把同一个 demo 拆成六步：原始工单、Parser Agent、Quality Agent、Knowledge Agent、Merge 节点、Human Review，并把职责边界和风险路由对应到设计模式。页面里可以切换 `Good ticket`、`Poor ticket`、`Potential duplicate` 三种场景，再点击 `Run Demo` 或 `Next Step` 观察不同路由结果。

## 文件结构

```
workshop2-ticket-review/
├── specs/
│   └── ticket-review-spec.md        ← SDD 规范文档
├── src/
│   ├── config.py                    ← 配置
│   ├── agents/
│   │   ├── parser_agent.py          ← Agent 1: 工单解析
│   │   ├── quality_agent.py         ← Agent 2: 质量检测
│   │   └── knowledge_agent.py       ← Agent 3: 知识匹配
│   ├── graph.py                     ← LangGraph 状态图编排（核心！）
│   └── main.py                      ← 完整流程 + Demo
├── requirements.txt
└── README.md
```

## LangGraph 架构图

```
[Raw Ticket]
     │
     ▼
┌─────────────────┐
│  parse           │ → Structured JSON
│  (Agent 1)       │
└────┬────────┬───┘
     │        │
     ▼        ▼         ← 并行执行
┌────────┐  ┌──────────┐
│quality │  │knowledge │
│(Ag. 2) │  │(Ag. 3)   │
└────┬───┘  └────┬─────┘
     │           │
     ▼           ▼
┌─────────────────┐
│  merge           │ → Risk-tiered decision
│  (Aggregation)   │
└────┬────────┬───┘
     │        │
     ▼        ▼
  [END]   [human_review] → [END]
```

## 三种测试工单

| 工单 | 特点 | 预期结果 |
|------|------|---------|
| Good ticket | 信息完整，优先级合理 | ✅ auto-approved |
| Poor ticket | 缺少复现步骤、环境、预期行为 | ❌ needs_human_review (score < 60) |
| Duplicate ticket | 信息完整，但与历史工单相似 | ⚠ needs_human_review (potential duplicate) |

---

## GitHub Copilot 操作步骤

### Step 0: 用规范驱动设计

1. 打开 `specs/ticket-review-spec.md`
2. Copilot Chat:

```
@workspace 根据 ticket-review-spec.md 的规范，
我要用 LangGraph 构建一个多 Agent 工单审查流水线。
请帮我规划代码结构和每个 Agent 的模块。
```

### Step 1: 生成 Agent 1 — 工单解析器

```
@workspace 根据规范中 Agent 1 的输出 schema，
生成 parser_agent.py，使用 Azure OpenAI 从工单文本中提取结构化字段。
```

### Step 2: 生成 Agent 2 — 质量检测器

```
@workspace 根据规范中 Agent 2 的检查项和评分规则，
生成 quality_agent.py。评分规则：
- 起始 100 分
- error 级问题 -20 分
- warning 级问题 -10 分
```

### Step 3: 生成 Agent 3 — 知识匹配器

```
@workspace 生成 knowledge_agent.py，
使用 ChromaDB + Azure OpenAI Embeddings 实现历史工单的语义检索。
```

### Step 4: LangGraph 编排

这是核心步骤。在 Copilot Chat 中：

```
@workspace 用 LangGraph 构建状态图：
- 入口节点 parse（调用 Agent 1）
- parse 后并行执行 quality 和 knowledge
- 两者完成后进入 merge 节点
- merge 根据风险分层规范决定是 END 还是 human_review

状态定义参考 ticket-review-spec.md §5 的最终报告格式。
```

> **教学要点**：让学员理解 LangGraph 的 `add_conditional_edges` 如何实现风险分层逻辑。

### Step 5: SDD 闭环

```
@workspace 在 merge 节点中，按照规范 §4 的风险分层表实现判断逻辑：
- score >= 80 且无 error → approved
- score < 60 或有 error → needs_human_review
- P1 升级 → needs_human_review
- potential_duplicate → needs_human_review
```

### Copilot 操作技巧

| 技巧 | 说明 |
|------|------|
| 规范中的 JSON schema → 注释 | 把 schema 贴到 Agent 代码的注释中，Copilot 会严格遵守 |
| LangGraph 节点模板 | 先写 `def node_xxx(state: State) -> dict:` 签名，Copilot 补全实现 |
| `/explain` 检查编排逻辑 | 让 Copilot 解释 conditional_edges 的路由是否正确 |
| 并行 vs 串行 | 提醒 Copilot: "quality 和 knowledge 无依赖，应并行" |

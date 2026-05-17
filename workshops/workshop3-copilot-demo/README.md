# Workshop 3: Copilot 驱动的 Agent 开发全流程

> **SDD + Copilot**：规范文档 = Copilot 的最强上下文。写好规范 → 生成代码 → 用规范验证。

## 场景

用 GitHub Copilot 从零开始构建一个"会议纪要自动生成 Agent"，展示 SDD + Copilot 的完整工作流。

## 快速开始

```bash
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env

cd src
python main.py  # Demo 模式
```

## 可视化讲解页

运行 CLI 之后，可以直接打开：

```bash
open visual/index.html
```

这页把同一个 demo 拆成六步：规约上下文、Copilot 计划、Prompt Chain、质量验证、Skill Package、渐进交付，并把 SDD 与设计模式对应起来。

## 文件结构

```
workshop3-copilot-demo/
├── specs/
│   └── meeting-agent-spec.md     ← SDD 规范文档
├── src/
│   ├── meeting_agent.py          ← Agent 核心代码
│   └── main.py                   ← Demo 演示
├── requirements.txt
└── README.md                     ← Copilot 操作步骤（本文件）
```

---

## GitHub Copilot 详细操作步骤

> 这是本 Workshop 的核心教学内容：一步步展示如何用 Copilot 高效开发 Agent。

### 准备工作

1. 确保 VS Code 已安装 **GitHub Copilot** 和 **GitHub Copilot Chat** 插件
2. 确保 Copilot 已激活（右下角应显示 Copilot 图标）
3. 打开终端，确认 Python 环境和 Azure OpenAI 配置就绪

### Phase 1: 规范驱动设计（5 min）

**操作**：
1. 在 VS Code 中打开 `specs/meeting-agent-spec.md`
2. 按 `Ctrl+Shift+I` 打开 Copilot Chat
3. 输入：

```
@workspace 我要按照 specs/meeting-agent-spec.md 中的规范构建一个会议纪要 Agent。
请帮我规划 Python 项目结构，使用 Azure OpenAI + LangChain。
```

4. Copilot 会建议项目结构，确认后继续

**教学要点**：
- SDD 的第一步永远是"写规范"，而非"写代码"
- 规范文档是 Copilot 最好的上下文——比口头描述精确 10 倍

### Phase 2: 生成 Agent 骨架（15 min）

**操作 2.1 — 配置文件**：
1. 新建 `src/meeting_agent.py`
2. 输入注释：

```python
# Azure OpenAI configuration for LSEG tech stack
# Using Microsoft AI Foundry endpoint
```

3. 按 `Tab` 接受 Copilot 的自动补全
4. Copilot 会生成 endpoint、key、model 等配置代码

**操作 2.2 — System Prompt**：
1. 在 meeting_agent.py 中，输入：

```python
# SDD-driven System Prompt — output format defined by meeting-agent-spec.md
MEETING_PROMPT = ChatPromptTemplate.from_messages([
```

2. 在 Copilot Chat 中：

```
@workspace 根据 meeting-agent-spec.md 第3节的输出 schema，
生成 System Prompt。要求 Agent 严格按照 JSON 格式输出会议纪要。
```

3. Copilot 会生成包含 JSON schema 的完整 System Prompt

**教学要点**：
- 把规范中的 JSON schema 直接嵌入 System Prompt
- 这就是"规范即输入"——规范驱动 Agent 行为

**操作 2.3 — 核心函数**：
1. 输入函数签名：

```python
def generate_minutes(
    transcript: str,
    meeting_title: str = "Team Meeting",
    participants: list[str] = None,
    meeting_date: str = None,
) -> dict:
    """生成结构化会议纪要"""
```

2. 按 `Tab` 让 Copilot 补全实现
3. 检查：是否使用了 Azure OpenAI？是否按规范格式输出？

### Phase 3: 生成质量验证（10 min）

**操作**：
1. 在 Copilot Chat 中：

```
@workspace 根据 meeting-agent-spec.md 第3.2节的质量标准，
生成 validate_minutes() 函数，检查：
- summary 不超过 100 字
- 所有 action_item 都有 assignee
- 至少 2 个 key_points
- deadline 是具体日期
```

2. Copilot 生成验证代码后，审查每个检查项是否与规范一致

**教学要点**：
- 这就是"规范即评估"——用同一份规范检查 Agent 输出
- SDD 闭环：规范 → 代码 → 输出 → 用规范验证输出

### Phase 4: Copilot 辅助调试（10 min）

**操作 4.1 — 错误诊断**：
1. 选中代码，右键 → "Copilot: Explain This"（或输入 `/explain`）
2. 如果有错误，选中错误信息，输入 `/fix`

**操作 4.2 — 代码优化**：
1. 选中 `generate_minutes()` 函数
2. Copilot Chat：

```
@workspace 这个函数有没有安全问题？
特别关注：JSON 解析失败的处理、Token 长度限制、API 超时。
```

3. 根据 Copilot 建议添加错误处理

### Phase 5: 运行验证（15 min）

**操作**：
1. 在终端运行：`python main.py`
2. 观察输出：
   - 会议纪要是否符合规范格式？
   - 质量检查是否全部通过？
   - 行动项是否都有 assignee 和 deadline？
3. 如果质量检查不通过，用 Copilot 调整 System Prompt

### Phase 6: 生成邮件草稿（Bonus, 5 min）

**操作**：
1. 在 Copilot Chat 中：

```
@workspace 给 meeting_agent.py 添加一个 generate_email() 函数，
从会议纪要生成跟进邮件草稿。包含摘要、行动项、下次会议时间。
```

---

## Copilot 最佳实践总结

### Do's ✅

| 做法 | 原因 |
|------|------|
| 先写规范文档，再开 Copilot | 规范 = 最精确的上下文 |
| 用 `@workspace` 引用规范文件 | 让 Copilot 看到完整上下文 |
| 先写函数签名 + docstring | 引导 Copilot 生成正确的实现 |
| 把约束写在注释中 | Copilot 会遵守注释中的约束 |
| 用 `/explain` 检查生成代码 | 确保理解代码逻辑 |
| 把 JSON schema 放入 Prompt | SDD：规范驱动 Agent 输出格式 |

### Don'ts ❌

| 做法 | 原因 |
|------|------|
| 一次让 Copilot 生成整个项目 | 太大的上下文会降低质量 |
| 不审查直接用 Copilot 代码 | 可能有安全漏洞或逻辑错误 |
| 忽略 API key 的安全处理 | 必须用 .env，不硬编码 |
| 跳过质量验证 | SDD 闭环不能少 |
| 用 Copilot 处理敏感数据 | 注意数据隐私合规 |

### Copilot 快捷键速查

| 快捷键 | 功能 |
|--------|------|
| `Tab` | 接受代码补全 |
| `Esc` | 取消补全 |
| `Ctrl+Shift+I` | 打开 Copilot Chat |
| `Ctrl+I` | Inline Chat（行内对话） |
| `/explain` | 解释选中代码 |
| `/fix` | 修复错误 |
| `/tests` | 生成测试代码 |
| `@workspace` | 引用整个工作区上下文 |

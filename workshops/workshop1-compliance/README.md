# Workshop 1: 合规监管文档智能分析

> **SDD 实践**：先写规范，再写代码，最后用规范评估结果。

## 场景

MAS / FCA 等金融监管机构发布新规，Agent 自动：
1. 解析新旧版监管文档
2. 对比变更点
3. 检索企业内部合规知识库（RAG）
4. 生成结构化合规影响报告
5. 自动质量检查（SDD 闭环）

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 Azure OpenAI 的 endpoint 和 key

# 3. 运行 Demo（无需真实 API，课堂演示用）
cd src
python main.py

# 4. 运行完整流程（需要 Azure OpenAI API）
python main.py new_regulation.pdf baseline.pdf company_sop.pdf "AML/KYC"
```

## 交互式可视化 Demo

运行 CLI 之后，可以直接打开：

```bash
open visual/index.html
```

这页把同一个 demo 拆成六步：SDD 契约、文档接入、语义差异、政策 RAG、影响报告、质量门，并把每一步对应到设计模式。页面里可以点击 `Run Demo`、`Next Step`、`Reset`，实时查看状态 JSON、执行日志、质量门和最终输出。

## 文件结构

```
workshop1-compliance/
├── specs/
│   └── compliance-spec.md     ← SDD 规范文档（第一步！）
├── src/
│   ├── config.py              ← Azure OpenAI 配置
│   ├── document_parser.py     ← 文档解析（PDF/HTML/TXT）
│   ├── rag_engine.py          ← RAG 向量知识库
│   ├── compliance_agent.py    ← 合规分析 Agent（核心）
│   └── main.py                ← 完整流程编排
├── data/                      ← 示例文档
├── requirements.txt
└── README.md
```

---

## GitHub Copilot 操作步骤

> 以下步骤展示如何用 Copilot 加速 Workshop 代码开发。

### Step 0: 用规范文档作为 Copilot 上下文

1. 在 VS Code 中打开 `specs/compliance-spec.md`
2. 打开 Copilot Chat（`Ctrl+Shift+I`）
3. 输入：

```
@workspace 我要按照 specs/compliance-spec.md 中的规范，
用 Python + Azure OpenAI + LangChain 构建一个合规文档分析 Agent。
请帮我规划代码结构。
```

> **SDD 要点**：规范文档 = Copilot 的最强上下文。先让 Copilot "读"规范，再生成代码。

### Step 1: 生成配置文件

1. 新建 `src/config.py`
2. 输入注释，Copilot 自动补全：

```python
# Azure OpenAI configuration for LSEG tech stack
# Using Microsoft AI Foundry endpoint
```

3. Copilot 会自动补全 endpoint、key、model 等配置
4. **Copilot Chat** 追问：`@workspace 帮我加上 .env 文件加载和 ChromaDB 配置`

### Step 2: 生成文档解析器

1. 新建 `src/document_parser.py`
2. 在 Copilot Chat 中：

```
@workspace 根据 compliance-spec.md 第2节的输入规范，
生成一个文档解析模块，支持 PDF、HTML、TXT 格式，
使用 LangChain 的 document loaders。
```

3. Copilot 生成完整代码后，检查：
   - 是否覆盖了规范要求的三种格式？
   - 是否有合理的文本分块逻辑？

### Step 3: 生成 RAG 引擎

1. 新建 `src/rag_engine.py`
2. 输入函数签名，让 Copilot 补全：

```python
def build_vectorstore(chunks: list[dict], collection_name: str = "compliance") -> Chroma:
    """将文档块存入 ChromaDB 向量库"""
```

3. Copilot 会自动补全 embedding + ChromaDB 集成代码
4. 用 `/explain` 检查生成的代码是否正确使用了 Azure OpenAI Embeddings

### Step 4: 生成合规分析 Agent

这是核心步骤。在 Copilot Chat 中：

```
@workspace 根据 compliance-spec.md 第3节的输出规范，
生成合规分析 Agent，要求：
1. System Prompt 严格按照规范中的 JSON schema 输出
2. 置信度低于 0.8 标记为需人工复核
3. 每条变更必须有 source_reference
4. 使用 Azure OpenAI gpt-4o
```

> **关键技巧**：把 SDD 规范的具体条款直接写进 Copilot 提示词，Copilot 生成的代码就会自动遵守这些约束。

### Step 5: 生成质量检查器

```
@workspace 根据 compliance-spec.md 第4节的质量评估规范，
生成一个 quality_check 函数，检查：
- 引用完整性
- 置信度阈值
- 高影响变更的行动建议
- 幻觉检测
```

### Step 6: 组装主流程

在 `main.py` 中，输入注释让 Copilot 补全：

```python
# Full pipeline: spec → parse → vectorize → analyze → quality check → report
def run_full(new_doc_path, baseline_path, sop_path, scope):
```

### Copilot 使用技巧总结

| 技巧 | 说明 |
|------|------|
| `@workspace` + 规范文件 | 让 Copilot 以规范为上下文生成代码 |
| 先写函数签名和 docstring | 引导 Copilot 生成符合预期的实现 |
| `/explain` | 检查生成代码的逻辑是否正确 |
| `/fix` | 修复 Copilot 生成代码中的错误 |
| 把规范条款写进注释 | Copilot 会遵守注释中的约束 |

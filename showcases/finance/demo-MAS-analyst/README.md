# MAS Compliance Analyst Agent — Demo V1

AI Agent demo that automates the work of a **Regulatory Compliance Manager** at a Singapore bank regulated by MAS.

## Quick Start

```bash
pip install streamlit
streamlit run app.py
```

Open http://localhost:8501

## What It Does

Based on a real [Compliance Manager job description](JobDescription.txt), the demo shows how an AI Agent can handle key compliance tasks for a bank selling financial products.

### 4 Demo Tabs

| Tab | Description |
|-----|-------------|
| **Pipeline Demo** | 5-step end-to-end flow: Search MAS website → Extract regulations → Map to tasks → Run compliance checks → Generate report |
| **Compliance Check** | Interactive: input customer profile + select product → get real-time compliance verdict |
| **Analyst Tasks** | 8 compliance tasks from the JD, with AI automation potential for each |
| **Knowledge Base** | Browse MAS regulations (FAA-N16, Fair Dealing, AML/CFT, etc.) |

### Sample Scenarios

| Scenario | Verdict |
|----------|---------|
| Sell high-risk structured deposit to 72-year-old retiree | 🚫 BLOCKED |
| Sell high-risk fund to customer with heavy debt | ⚠️ WARNING |
| Rep says "guaranteed 8% returns" for non-guaranteed product | 🚫 BLOCKED |

## Files

```
app.py              # Streamlit UI (main app)
mas_knowledge.py    # MAS regulation knowledge base + demo scenarios
requirements.txt    # Dependencies
JobDescription.txt  # Source JD for the compliance manager role
```

## V2 Roadmap

- Plug in LLM (Claude/GPT) for dynamic regulation analysis
- Scrape MAS website for real-time regulatory updates
- Add voice recording compliance review (pitch recording analysis)
- Vector DB (Milvus/Qdrant) for semantic regulation search
- Multi-agent orchestration with LangGraph

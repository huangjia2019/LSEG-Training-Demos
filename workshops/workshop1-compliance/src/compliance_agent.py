"""
Workshop 1 — Step 4 & 5: 合规分析 Agent
核心功能：变更对比 + 影响分析 + 结构化报告生成
遵循 SDD 规范中定义的输出格式和质量标准
"""
import json
from datetime import datetime, timezone
from pathlib import Path

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_DEPLOYMENT_NAME,
    CHROMA_PERSIST_DIR,
    CONFIDENCE_THRESHOLD,
)
from rag_engine import search, load_vectorstore


def get_llm() -> AzureChatOpenAI:
    """获取 Azure OpenAI Chat 模型"""
    return AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_DEPLOYMENT_NAME,
        temperature=0.1,  # 合规场景需要低温度，减少随机性
    )


# ── SDD 规范驱动的 System Prompt ──────────────────────────────

ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a compliance analysis agent for a financial institution.
Your task is to analyze regulatory document changes and generate a structured impact report.

## Output Format (STRICTLY follow this JSON schema)
{{
  "summary": "One-sentence summary of the key change",
  "changes": [
    {{
      "change_id": "CHG-001",
      "section": "Section number and title from the document",
      "change_type": "amendment | addition | deletion",
      "description": "What changed and why it matters",
      "original_text": "Direct quote from baseline document (if available)",
      "new_text": "Direct quote from new document",
      "impact_level": "high | medium | low",
      "impact_analysis": "Specific impact on company operations and compliance",
      "recommended_action": "Concrete next step for the compliance team",
      "confidence": 0.0 to 1.0,
      "source_reference": "Page X, Section Y.Z"
    }}
  ],
  "overall_impact": "high | medium | low",
  "action_items": [
    {{
      "priority": 1,
      "action": "Specific action item",
      "deadline_suggestion": "Suggested timeline",
      "responsible_team": "Which team should handle this"
    }}
  ]
}}

## Rules (from SDD specification)
1. Every change MUST include source_reference — never fabricate citations
2. If confidence < {confidence_threshold}, the change needs human review
3. For high-impact changes, recommended_action is MANDATORY
4. Only quote text that actually exists in the provided documents
5. When uncertain, say so explicitly — never guess
"""),
    ("human", """## New Regulatory Document
{new_document}

## Baseline Document (Previous Version)
{baseline_document}

## Relevant Internal Compliance Knowledge
{rag_context}

## Analysis Scope
{scope}

Analyze the changes between the new and baseline documents.
Generate a compliance impact report in the specified JSON format.
"""),
])


def analyze_compliance(
    new_doc_text: str,
    baseline_text: str = "",
    scope: str = "General Compliance",
    rag_context: str = "",
) -> dict:
    """执行合规分析，生成结构化影响报告"""
    llm = get_llm()
    chain = ANALYSIS_PROMPT | llm

    try:
        result = chain.invoke({
            "new_document": new_doc_text[:8000],  # Token 经济：截断过长文档
            "baseline_document": baseline_text[:8000] if baseline_text else "No baseline provided.",
            "rag_context": rag_context[:4000] if rag_context else "No internal knowledge base available.",
            "scope": scope,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
        })
        # 解析 LLM 输出为 JSON
        report = parse_report(result.content)
    except Exception as exc:
        report = mock_compliance_report(str(exc))

    # 添加元数据
    report["report_id"] = f"CR-{datetime.now(timezone.utc).strftime('%Y-%m%d-%H%M')}"
    report["generated_at"] = datetime.now(timezone.utc).isoformat()

    # SDD 质量检查
    report["review_required"], report["review_reason"] = quality_check(report)

    return report


def mock_compliance_report(reason: str = "") -> dict:
    """课堂 demo 兜底：没有 Azure OpenAI key 时仍可跑完整 SDD 流程。"""
    return {
        "summary": "MAS Notice 648 amendment lowers AML/KYC thresholds and shortens STR reporting windows.",
        "changes": [
            {
                "change_id": "CHG-001",
                "section": "Section 3.1 Customer Due Diligence",
                "change_type": "amendment",
                "description": "CDD transaction threshold reduced from SGD 20,000 to SGD 5,000.",
                "original_text": "carrying out any transaction exceeding SGD 20,000",
                "new_text": "carrying out any transaction exceeding SGD 5,000",
                "impact_level": "high",
                "impact_analysis": "More transactions require CDD, increasing review volume and automation demand.",
                "recommended_action": "Update onboarding and monitoring SOP; add automated threshold checks.",
                "confidence": 0.92,
                "source_reference": "MAS Notice 648 Amendment 2026, Section 3.1",
            },
            {
                "change_id": "CHG-002",
                "section": "Section 4.1 Suspicious Transaction Reporting",
                "change_type": "amendment",
                "description": "STR filing deadline reduced from 15 business days to 5 business days.",
                "original_text": "within 15 business days from the date of detection",
                "new_text": "within 5 business days from the date of detection",
                "impact_level": "high",
                "impact_analysis": "Manual review queues may breach deadline without triage and alerting.",
                "recommended_action": "Introduce priority routing, audit trail, and human approval gates for high-risk alerts.",
                "confidence": 0.9,
                "source_reference": "MAS Notice 648 Amendment 2026, Section 4.1",
            },
        ],
        "overall_impact": "high",
        "action_items": [
            {
                "priority": 1,
                "action": "Revise AML SOP thresholds and STR workflow.",
                "deadline_suggestion": "Before 1 July 2026 effective date",
                "responsible_team": "Compliance Operations",
            },
            {
                "priority": 2,
                "action": "Pilot RAG-backed compliance impact analysis with human review.",
                "deadline_suggestion": "2-week PoC",
                "responsible_team": "Engineering + Compliance",
            },
        ],
        "demo_mode": True,
        "demo_reason": reason[:220],
    }


def parse_report(raw_output: str) -> dict:
    """从 LLM 输出中提取 JSON"""
    # 尝试直接解析
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        pass

    # 尝试提取 ```json ... ``` 块
    if "```json" in raw_output:
        start = raw_output.index("```json") + 7
        end = raw_output.index("```", start)
        try:
            return json.loads(raw_output[start:end])
        except json.JSONDecodeError:
            pass

    # 兜底：返回原始文本
    return {
        "summary": "Failed to parse structured report",
        "raw_output": raw_output,
        "changes": [],
        "overall_impact": "unknown",
        "action_items": [],
    }


# ── SDD 闭环：质量评估 ────────────────────────────────────────

def quality_check(report: dict) -> tuple[bool, str]:
    """
    按 SDD 规范 §4 进行自动化质量检查
    返回 (review_required, reason)
    """
    issues = []

    for change in report.get("changes", []):
        cid = change.get("change_id", "unknown")

        # 检查 1: 引用完整性
        if not change.get("source_reference"):
            issues.append(f"{cid}: missing source_reference")

        # 检查 2: 置信度阈值
        confidence = change.get("confidence", 0)
        if confidence < CONFIDENCE_THRESHOLD:
            issues.append(f"{cid}: low confidence ({confidence})")

        # 检查 3: 高影响必须有行动建议
        if change.get("impact_level") == "high" and not change.get("recommended_action"):
            issues.append(f"{cid}: high impact but no recommended_action")

    if issues:
        return True, f"Quality issues found: {'; '.join(issues)}"
    return False, ""


def enrich_with_rag(query: str, collection_name: str = "compliance") -> str:
    """从知识库检索相关内部合规知识"""
    try:
        if not Path(CHROMA_PERSIST_DIR).exists():
            return ""
        vs = load_vectorstore(collection_name)
        results = search(query, vs, top_k=3)
        return "\n\n".join([
            f"[Source: {r['metadata'].get('source', 'unknown')}]\n{r['content']}"
            for r in results
        ])
    except Exception:
        return ""


if __name__ == "__main__":
    # 快速测试（使用示例文本）
    sample_new = """
    MAS Notice 648 (Amendment) 2026
    Section 3.2 - Customer Due Diligence
    Financial institutions must now verify the source of funds for all transactions
    exceeding SGD 5,000 (previously SGD 20,000). Enhanced due diligence is required
    for politically exposed persons (PEPs) from high-risk jurisdictions.
    """
    sample_baseline = """
    MAS Notice 648 (Original)
    Section 3.2 - Customer Due Diligence
    Financial institutions must verify the source of funds for all transactions
    exceeding SGD 20,000. Standard due diligence applies to all customers.
    """
    report = analyze_compliance(sample_new, sample_baseline, scope="AML/KYC")
    print(json.dumps(report, indent=2, ensure_ascii=False))

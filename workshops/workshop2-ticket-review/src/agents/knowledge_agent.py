"""
Agent 3: 知识库匹配器（Knowledge Matcher）
职责：从历史工单库中检索类似问题和解决方案
遵循 SDD 规范 §2 Agent 3 的输出 schema
"""
import json
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION, AZURE_DEPLOYMENT_NAME,
    AZURE_EMBEDDING_DEPLOYMENT, CHROMA_PERSIST_DIR,
)

# ── 历史工单知识库 ─────────────────────────────────────────────

SAMPLE_HISTORICAL_TICKETS = [
    {
        "id": "TICKET-1001",
        "title": "Market data feed delay during high-volume trading",
        "resolution": "Increased message queue buffer size from 10K to 50K. Added circuit breaker for feed reconnection.",
        "component": "Market Data Service",
    },
    {
        "id": "TICKET-1023",
        "title": "Authentication timeout for API clients during peak hours",
        "resolution": "Implemented connection pooling for OAuth token validation. Increased timeout from 5s to 15s.",
        "component": "Auth Gateway",
    },
    {
        "id": "TICKET-1045",
        "title": "Incorrect currency conversion in settlement reports",
        "resolution": "Fixed FX rate cache staleness. Now refreshes every 60s instead of daily. Added rate validation check.",
        "component": "Settlement Engine",
    },
    {
        "id": "TICKET-1067",
        "title": "Memory leak in real-time risk calculation service",
        "resolution": "Fixed unbounded cache growth in position aggregator. Added LRU eviction policy with 100K entry limit.",
        "component": "Risk Engine",
    },
    {
        "id": "TICKET-1089",
        "title": "Compliance report generation fails for large portfolios",
        "resolution": "Switched from in-memory processing to streaming pipeline. Added pagination for portfolio queries.",
        "component": "Compliance Reporting",
    },
]


def build_ticket_knowledge_base() -> Chroma:
    """构建历史工单向量知识库"""
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_EMBEDDING_DEPLOYMENT,
    )
    docs = [
        Document(
            page_content=f"Title: {t['title']}\nResolution: {t['resolution']}",
            metadata={"ticket_id": t["id"], "component": t["component"]},
        )
        for t in SAMPLE_HISTORICAL_TICKETS
    ]
    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="historical_tickets",
        persist_directory=CHROMA_PERSIST_DIR,
    )


MATCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a knowledge matching agent. Given a new ticket and similar historical tickets,
determine if any are relevant matches or potential duplicates.

Output STRICTLY as JSON:
{{
  "ticket_id": "from input",
  "matches": [
    {{
      "historical_id": "TICKET-XXXX",
      "similarity_score": 0.0-1.0,
      "title": "historical ticket title",
      "resolution": "how it was resolved",
      "is_duplicate": true/false
    }}
  ],
  "potential_duplicate": true if any match has similarity > 0.9
}}
"""),
    ("human", """New ticket:
{new_ticket}

Similar historical tickets found:
{historical_matches}

Analyze relevance and potential duplicates."""),
])


def match_knowledge(parsed_ticket: dict, llm: AzureChatOpenAI = None) -> dict:
    """从历史知识库中匹配类似工单"""
    if llm is None:
        llm = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_deployment=AZURE_DEPLOYMENT_NAME,
            temperature=0,
        )

    # 构建查询
    query = f"{parsed_ticket.get('title', '')} {parsed_ticket.get('actual_behavior', '')}"

    # RAG 检索
    try:
        embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_deployment=AZURE_EMBEDDING_DEPLOYMENT,
        )
        vs = Chroma(
            collection_name="historical_tickets",
            embedding_function=embeddings,
            persist_directory=CHROMA_PERSIST_DIR,
        )
        results = vs.similarity_search_with_score(query, k=3)
        historical = "\n\n".join([
            f"[{doc.metadata.get('ticket_id', 'unknown')}] (distance: {score:.3f})\n{doc.page_content}"
            for doc, score in results
        ])
    except Exception:
        historical = "No historical knowledge base available."

    chain = MATCH_PROMPT | llm
    result = chain.invoke({
        "new_ticket": json.dumps(parsed_ticket, indent=2),
        "historical_matches": historical,
    })

    try:
        report = json.loads(result.content)
    except json.JSONDecodeError:
        if "```json" in result.content:
            start = result.content.index("```json") + 7
            end = result.content.index("```", start)
            report = json.loads(result.content[start:end])
        else:
            report = {"error": "Failed to parse", "matches": [], "potential_duplicate": False}

    return report

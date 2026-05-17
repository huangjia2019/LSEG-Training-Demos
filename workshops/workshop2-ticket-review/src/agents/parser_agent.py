"""
Agent 1: 工单解析器（Ticket Parser）
职责：从非结构化工单文本中提取结构化字段
遵循 SDD 规范 §2 Agent 1 的输出 schema
"""
import json
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION, AZURE_DEPLOYMENT_NAME,
)

PARSER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a ticket parsing agent for a financial software company.
Extract structured information from bug reports.

Output STRICTLY as JSON:
{{
  "ticket_id": "extracted or generated ID",
  "title": "ticket title",
  "component": "affected component or null",
  "environment": "OS/browser/version or null",
  "severity_claimed": "P1|P2|P3|P4 or null",
  "reproduction_steps": ["step1", "step2", ...],
  "expected_behavior": "what should happen or null",
  "actual_behavior": "what actually happens or null",
  "attachments_mentioned": true/false
}}

Rules:
- Extract only what is explicitly stated. Do NOT infer missing fields.
- If a field is not mentioned, set it to null (or empty array for steps).
- For severity, look for keywords like P1/P2/Critical/Major/Minor.
"""),
    ("human", "Parse this ticket:\n\n{ticket_text}"),
])


def parse_ticket(ticket_text: str, llm: AzureChatOpenAI = None) -> dict:
    """解析工单文本，返回结构化 JSON"""
    if llm is None:
        llm = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_deployment=AZURE_DEPLOYMENT_NAME,
            temperature=0,
        )

    chain = PARSER_PROMPT | llm
    result = chain.invoke({"ticket_text": ticket_text})

    try:
        parsed = json.loads(result.content)
    except json.JSONDecodeError:
        if "```json" in result.content:
            start = result.content.index("```json") + 7
            end = result.content.index("```", start)
            parsed = json.loads(result.content[start:end])
        else:
            parsed = {"error": "Failed to parse", "raw": result.content}

    return parsed

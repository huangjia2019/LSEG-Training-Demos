"""
Agent 2: 质量检测器（Quality Inspector）
职责：检查工单信息完整性和优先级合理性
遵循 SDD 规范 §2 Agent 2 的检查项和输出 schema
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

QUALITY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a ticket quality inspector for a financial software company.
Evaluate the quality of a parsed bug report.

## Quality Checks (from SDD specification)
1. reproduction_steps: must have at least 2 steps → severity: error
2. environment: must not be null → severity: warning
3. component: must not be null → severity: warning
4. expected_behavior: must not be null → severity: error
5. severity assessment: evaluate if claimed severity matches the actual impact

## Scoring
- Start at 100 points
- Each "error" issue: -20 points
- Each "warning" issue: -10 points
- Each "info" issue: -5 points
- Minimum score: 0

Output STRICTLY as JSON:
{{
  "ticket_id": "from input",
  "quality_score": 0-100,
  "issues": [
    {{
      "field": "field_name",
      "severity": "error|warning|info",
      "message": "what's wrong",
      "suggestion": "how to fix"
    }}
  ],
  "severity_assessment": {{
    "claimed": "P1-P4 or null",
    "recommended": "P1-P4",
    "reason": "why this severity"
  }},
  "pass": true if score >= 80 and no errors
}}
"""),
    ("human", "Evaluate this parsed ticket:\n\n{parsed_ticket}"),
])


def inspect_quality(parsed_ticket: dict, llm: AzureChatOpenAI = None) -> dict:
    """检查工单质量，返回评估报告"""
    if llm is None:
        llm = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_deployment=AZURE_DEPLOYMENT_NAME,
            temperature=0,
        )

    chain = QUALITY_PROMPT | llm
    result = chain.invoke({"parsed_ticket": json.dumps(parsed_ticket, indent=2)})

    try:
        report = json.loads(result.content)
    except json.JSONDecodeError:
        if "```json" in result.content:
            start = result.content.index("```json") + 7
            end = result.content.index("```", start)
            report = json.loads(result.content[start:end])
        else:
            report = {"error": "Failed to parse", "raw": result.content}

    return report

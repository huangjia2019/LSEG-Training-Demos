"""
Workshop 3 — 会议纪要自动生成 Agent
SDD 驱动：规范文档定义输入输出格式，Copilot 辅助生成代码
展示从需求到可运行代码的完整 Copilot 工作流
"""
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ── 配置（Copilot Step 1: 输入注释让 Copilot 补全） ──────────

# Azure OpenAI configuration for LSEG tech stack
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "your-api-key")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")


def get_llm() -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_DEPLOYMENT_NAME,
        temperature=0.1,
    )


# ── SDD 规范驱动的 Prompt（Copilot Step 2: 规范 → Prompt） ────

MEETING_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a meeting minutes agent for a financial services company (LSEG).
Generate structured meeting minutes from a transcript.

## Output Format (STRICTLY follow this JSON schema — from SDD spec)
{{
  "meeting_title": "string",
  "date": "YYYY-MM-DD",
  "participants": ["name1", "name2"],
  "duration_minutes": integer,
  "summary": "2-3 sentence summary (max 100 words)",
  "key_points": [
    {{
      "topic": "Discussion topic",
      "discussion": "Summary of discussion",
      "decision": "Final decision (if any, else null)"
    }}
  ],
  "action_items": [
    {{
      "id": "AI-001",
      "description": "Action item description",
      "assignee": "Person responsible (TBD if unknown)",
      "deadline": "YYYY-MM-DD (convert relative dates to absolute)",
      "priority": "high | medium | low"
    }}
  ],
  "next_meeting": "Next meeting info or null"
}}

## Rules (from SDD specification)
1. summary must not exceed 100 words
2. Every action_item must have an assignee — use "TBD" if not mentioned
3. Extract at least 2 key_points
4. NEVER add content not discussed in the meeting
5. Convert relative dates ("next Tuesday") to absolute dates based on meeting date
6. Stay neutral and objective — no subjective commentary
"""),
    ("human", """Meeting transcript:
{transcript}

Meeting title: {meeting_title}
Participants: {participants}
Meeting date: {meeting_date}

Generate structured meeting minutes."""),
])


def generate_minutes(
    transcript: str,
    meeting_title: str = "Team Meeting",
    participants: list[str] = None,
    meeting_date: str = None,
) -> dict:
    """生成结构化会议纪要"""
    llm = get_llm()
    chain = MEETING_PROMPT | llm

    if meeting_date is None:
        meeting_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if participants is None:
        participants = ["(auto-detect from transcript)"]

    result = chain.invoke({
        "transcript": transcript[:6000],
        "meeting_title": meeting_title,
        "participants": ", ".join(participants),
        "meeting_date": meeting_date,
    })

    # 解析 JSON
    try:
        minutes = json.loads(result.content)
    except json.JSONDecodeError:
        if "```json" in result.content:
            start = result.content.index("```json") + 7
            end = result.content.index("```", start)
            minutes = json.loads(result.content[start:end])
        else:
            minutes = {"error": "Failed to parse", "raw": result.content}

    # SDD 质量检查
    minutes["quality_check"] = validate_minutes(minutes)
    return minutes


# ── SDD 闭环：质量评估（Copilot Step 3: 规范 → 验证代码） ────

def validate_minutes(minutes: dict) -> dict:
    """按 SDD 规范检查会议纪要质量"""
    checks = {}

    # Check 1: summary 不超过 100 字
    summary = minutes.get("summary", "")
    word_count = len(summary.split())
    checks["summary_length"] = {
        "pass": word_count <= 100,
        "detail": f"{word_count} words (max 100)",
    }

    # Check 2: action_items 都有 assignee
    actions = minutes.get("action_items", [])
    missing_assignee = [a["id"] for a in actions if not a.get("assignee")]
    checks["assignee_coverage"] = {
        "pass": len(missing_assignee) == 0,
        "detail": f"{len(missing_assignee)} items missing assignee" if missing_assignee else "All assigned",
    }

    # Check 3: 至少 2 个 key_points
    kp_count = len(minutes.get("key_points", []))
    checks["key_points_count"] = {
        "pass": kp_count >= 2,
        "detail": f"{kp_count} key points (min 2)",
    }

    # Check 4: deadline 是具体日期
    relative_dates = [a["id"] for a in actions
                      if a.get("deadline") and any(w in str(a["deadline"]).lower()
                                                    for w in ["next", "later", "soon", "tbd"])]
    checks["concrete_deadlines"] = {
        "pass": len(relative_dates) == 0,
        "detail": f"{len(relative_dates)} items with vague deadlines" if relative_dates else "All concrete",
    }

    checks["all_passed"] = all(c["pass"] for c in checks.values() if isinstance(c, dict))
    return checks


# ── 邮件草稿生成（Bonus 功能） ────────────────────────────────

EMAIL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Generate a concise follow-up email from meeting minutes.
Include: brief summary, action items with owners and deadlines, next meeting date.
Keep professional tone suitable for a financial services company.
Output plain text email (not JSON)."""),
    ("human", "Meeting minutes:\n{minutes_json}\n\nGenerate follow-up email."),
])


def generate_email(minutes: dict) -> str:
    """从会议纪要生成跟进邮件草稿"""
    llm = get_llm()
    chain = EMAIL_PROMPT | llm
    result = chain.invoke({"minutes_json": json.dumps(minutes, indent=2)})
    return result.content

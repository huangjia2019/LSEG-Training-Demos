"""
Workshop 3 — Copilot 驱动的 Agent 开发全流程
展示从 SDD 规范到可运行代码的完整 Copilot 工作流
"""
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from meeting_agent import generate_minutes, generate_email, validate_minutes

console = Console()

# ── 示例会议记录 ───────────────────────────────────────────────

SAMPLE_TRANSCRIPT = """
Meeting: Q1 Compliance System Review
Date: March 16, 2026
Participants: Lucy (Tech Lead), Angela (Compliance), David (Dev), Sarah (QA)

Lucy: Let's start with the status update on the AML monitoring system upgrade.

David: We've completed the real-time transaction screening module. It's passing all unit tests.
Currently processing about 50,000 transactions per hour in staging. But we're seeing some
false positives — about 15% of flagged transactions are actually clean.

Angela: 15% is too high. The compliance team is spending hours reviewing false alerts. We need
to get that below 5% before going live. Can we add more context to the screening rules?

David: Yes, I think if we add the customer transaction history as context, we can reduce
false positives significantly. I'll need about two weeks to implement that.

Lucy: Agreed. David, please prioritize the false positive reduction. Target: below 5%.
Deadline: end of March.

Sarah: On testing — I've finished the regression test suite for the new screening module.
But I still need to set up the performance test environment. Can IT provision the staging
servers by next Friday?

Lucy: I'll raise a ticket with IT. Sarah, please document the performance requirements
so IT knows what to provision.

Angela: One more thing — FCA is releasing updated guidelines on transaction monitoring next month.
We should review those as soon as they're published and assess impact on our system.

Lucy: Good point. Angela, can you set up a monitoring alert for the FCA publication?
And we should schedule a review session within a week of publication.

David: Also, I noticed our current ChromaDB deployment is running low on disk space.
We should plan a migration to a larger instance before it becomes critical.

Lucy: David, please create a ticket for that and estimate the effort. Let's discuss it
in next week's meeting.

Alright, I think that's everything. Next meeting: same time next Monday, March 23.
Thanks everyone.
"""


def run_demo():
    """演示完整的 Copilot → Agent 开发流程"""
    console.print(Panel(
        "[bold]Workshop 3: Copilot 驱动的 Agent 开发全流程[/bold]\n"
        "从 SDD 规范 → Copilot 生成代码 → 运行 Agent → 质量验证",
        title="🤖 LSEG Meeting Minutes Agent",
    ))

    # SDD Step 0
    console.print(Panel(
        "[bold blue]SDD Step 0: Specification as Copilot Context[/bold blue]\n\n"
        "We defined in meeting-agent-spec.md:\n"
        "  • Input: transcript text + metadata\n"
        "  • Output: structured JSON (summary, key_points, action_items)\n"
        "  • Quality: summary ≤100 words, all actions assigned, ≥2 topics\n\n"
        "Key insight: The clearer the spec, the better Copilot generates code.",
        title="📋 SDD Specification → Copilot",
    ))

    # Copilot 工作流演示
    console.print("\n[bold cyan]Copilot Workflow Demo[/bold cyan]")

    steps = [
        ("Step 1: Spec → Project Structure",
         "Copilot Chat: '@workspace 根据 meeting-agent-spec.md 规划代码结构'"),
        ("Step 2: Spec → System Prompt",
         "将规范中的 JSON schema 和 Rules 直接写入 System Prompt"),
        ("Step 3: Spec → Validation Code",
         "将规范中的质量标准转化为 validate_minutes() 函数"),
        ("Step 4: Run & Verify",
         "运行 Agent → 用规范自动检查输出质量（SDD 闭环）"),
    ]
    for title, desc in steps:
        console.print(f"  [bold]{title}[/bold]: {desc}")

    # 运行 Agent
    console.print(f"\n{'='*60}")
    console.print("[bold]Running Meeting Minutes Agent...[/bold]\n")

    try:
        minutes = generate_minutes(
            transcript=SAMPLE_TRANSCRIPT,
            meeting_title="Q1 Compliance System Review",
            participants=["Lucy", "Angela", "David", "Sarah"],
            meeting_date="2026-03-16",
        )
        display_minutes(minutes)

        # 生成邮件
        console.print("\n[bold]Generating follow-up email...[/bold]")
        email = generate_email(minutes)
        console.print(Panel(email, title="📧 Follow-up Email Draft"))

    except Exception as e:
        console.print(f"[yellow]API not available, showing mock result[/yellow]: {e}")
        display_mock_minutes()


def display_minutes(minutes: dict):
    """展示会议纪要"""
    console.print(Panel(
        f"[bold]Title:[/bold] {minutes.get('meeting_title', 'N/A')}\n"
        f"[bold]Date:[/bold] {minutes.get('date', 'N/A')}\n"
        f"[bold]Participants:[/bold] {', '.join(minutes.get('participants', []))}\n"
        f"[bold]Duration:[/bold] {minutes.get('duration_minutes', 'N/A')} min\n\n"
        f"[bold]Summary:[/bold]\n{minutes.get('summary', 'N/A')}",
        title="📝 Meeting Minutes",
    ))

    # Key Points
    if minutes.get("key_points"):
        table = Table(title="Key Points")
        table.add_column("Topic", style="cyan")
        table.add_column("Discussion")
        table.add_column("Decision", style="green")
        for kp in minutes["key_points"]:
            table.add_row(
                kp.get("topic", ""),
                kp.get("discussion", "")[:80] + "...",
                kp.get("decision") or "—",
            )
        console.print(table)

    # Action Items
    if minutes.get("action_items"):
        table = Table(title="Action Items")
        table.add_column("ID", style="bold")
        table.add_column("Description")
        table.add_column("Assignee", style="cyan")
        table.add_column("Deadline")
        table.add_column("Priority")
        for ai in minutes["action_items"]:
            color = {"high": "red", "medium": "yellow", "low": "green"}.get(ai.get("priority", ""), "")
            table.add_row(
                ai.get("id", ""),
                ai.get("description", ""),
                ai.get("assignee", "TBD"),
                ai.get("deadline", "TBD"),
                f"[{color}]{ai.get('priority', 'N/A')}[/{color}]" if color else ai.get("priority", ""),
            )
        console.print(table)

    # SDD Quality Check
    qc = minutes.get("quality_check", {})
    if qc:
        console.print(Panel(
            "\n".join([
                f"  {'✅' if v.get('pass') else '❌'} {k}: {v.get('detail', '')}"
                for k, v in qc.items()
                if isinstance(v, dict)
            ]),
            title="🔍 SDD Quality Check",
        ))


def display_mock_minutes():
    """Mock 结果（无 API 时）"""
    mock = {
        "meeting_title": "Q1 Compliance System Review",
        "date": "2026-03-16",
        "participants": ["Lucy", "Angela", "David", "Sarah"],
        "duration_minutes": 30,
        "summary": "Team reviewed AML monitoring system progress. Real-time screening module complete but has 15% false positive rate. Key decisions: reduce false positives to <5% by end of March, prepare for upcoming FCA guideline updates.",
        "key_points": [
            {
                "topic": "AML Monitoring System Upgrade",
                "discussion": "Real-time screening module completed, passing all unit tests, processing 50K transactions/hour. False positive rate at 15%, target is below 5%.",
                "decision": "David to add customer transaction history context to reduce false positives. Deadline: end of March."
            },
            {
                "topic": "Testing & Infrastructure",
                "discussion": "Regression test suite complete. Performance test environment needs provisioning from IT.",
                "decision": "Lucy to raise IT ticket. Sarah to document performance requirements."
            },
            {
                "topic": "FCA Regulatory Update",
                "discussion": "FCA releasing updated transaction monitoring guidelines next month.",
                "decision": "Angela to set up monitoring alert. Review session within one week of publication."
            },
            {
                "topic": "ChromaDB Migration",
                "discussion": "Current deployment running low on disk space.",
                "decision": "David to create ticket and estimate effort for next week's discussion."
            },
        ],
        "action_items": [
            {"id": "AI-001", "description": "Reduce false positive rate to <5% by adding transaction history context", "assignee": "David", "deadline": "2026-03-31", "priority": "high"},
            {"id": "AI-002", "description": "Raise IT ticket for staging server provisioning", "assignee": "Lucy", "deadline": "2026-03-17", "priority": "medium"},
            {"id": "AI-003", "description": "Document performance test requirements for IT", "assignee": "Sarah", "deadline": "2026-03-21", "priority": "medium"},
            {"id": "AI-004", "description": "Set up FCA publication monitoring alert", "assignee": "Angela", "deadline": "2026-03-20", "priority": "medium"},
            {"id": "AI-005", "description": "Create ticket for ChromaDB migration with effort estimate", "assignee": "David", "deadline": "2026-03-23", "priority": "low"},
        ],
        "next_meeting": "Monday, March 23, 2026 — same time",
    }

    mock["quality_check"] = validate_minutes(mock)
    display_minutes(mock)

    # Mock email
    console.print(Panel(
        "Subject: Meeting Minutes — Q1 Compliance System Review (Mar 16)\n\n"
        "Hi team,\n\n"
        "Here are the key takeaways from today's meeting:\n\n"
        "Summary: AML monitoring real-time screening is complete but needs false positive "
        "reduction from 15% to <5%. FCA guideline update expected next month.\n\n"
        "Action Items:\n"
        "  1. [HIGH] David: Reduce false positive rate to <5% — by Mar 31\n"
        "  2. [MED] Lucy: Raise IT ticket for staging servers — by Mar 17\n"
        "  3. [MED] Sarah: Document performance requirements — by Mar 21\n"
        "  4. [MED] Angela: Set up FCA monitoring alert — by Mar 20\n"
        "  5. [LOW] David: ChromaDB migration ticket — by Mar 23\n\n"
        "Next meeting: Monday, March 23, same time.\n\n"
        "Best regards",
        title="📧 Follow-up Email Draft (Mock)",
    ))


if __name__ == "__main__":
    run_demo()

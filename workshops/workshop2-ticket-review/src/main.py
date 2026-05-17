"""
Workshop 2 — 多 Agent 工单审查流水线：完整流程
SDD 驱动：规范定义 Agent 职责 → LangGraph 编排 → 质量检查 → 风险分层
"""
import json
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

console = Console()

# ── 示例工单数据 ───────────────────────────────────────────────

SAMPLE_TICKETS = [
    {
        "id": "good",
        "title": "Good ticket — complete information",
        "text": """
Title: Market data feed shows stale prices after reconnection
Priority: P2
Component: Market Data Service
Environment: Production, Linux CentOS 8, Java 17, Kafka 3.5

Steps to reproduce:
1. Disconnect the market data feed (simulate network partition)
2. Wait 30 seconds, then restore connectivity
3. Observe the price display for FTSE 100 constituents

Expected: Prices should update within 5 seconds of reconnection
Actual: Prices remain stale for 2-3 minutes. The feed shows "connected" status
but prices do not update until the service is manually restarted.

Logs attached: feed-reconnect-2026-03-15.log
Screenshot: stale-prices-dashboard.png
""",
    },
    {
        "id": "poor",
        "title": "Poor ticket — missing critical info",
        "text": """
Title: Something wrong with the reports
Priority: P3

The compliance report is broken. It doesn't work when I try to generate it
for some clients. Please fix ASAP.
""",
    },
    {
        "id": "duplicate",
        "title": "Potential duplicate ticket",
        "text": """
Title: Settlement report shows wrong currency conversion rates
Priority: P1
Component: Settlement Engine
Environment: Staging, Windows Server 2022

Steps to reproduce:
1. Run end-of-day settlement for portfolio containing JPY and EUR positions
2. Check the converted amounts in the settlement report

Expected: FX rates should match the closing rates from Reuters
Actual: The conversion uses rates from 24 hours ago, causing discrepancies
of up to 0.5% on large positions.

This is affecting client reconciliation and needs immediate fix.
""",
    },
]


def run_demo():
    """Demo 模式：使用预定义工单展示完整流水线"""
    console.print(Panel(
        "[bold]Workshop 2: 多 Agent 工单审查流水线[/bold]\n"
        "LangGraph 编排 3 个 Agent 协作审查工单质量",
        title="🔍 LSEG Ticket Review Pipeline",
    ))

    # SDD Step 0
    console.print(Panel(
        "[bold blue]SDD Step 0: Review Agent Specifications[/bold blue]\n\n"
        "Each agent has a clear specification:\n"
        "  • Agent 1 (Parser): raw text → structured JSON\n"
        "  • Agent 2 (Quality): structured ticket → quality score + issues\n"
        "  • Agent 3 (Knowledge): structured ticket → historical matches\n\n"
        "Communication protocol: JSON only (report-style, no raw data)\n"
        "Risk tiers: auto-pass (≥80) | needs-revision (60-79) | human-review (<60)",
        title="📋 SDD Specification",
    ))

    # 展示 LangGraph 架构
    tree = Tree("[bold]Ticket Review Graph[/bold]")
    parse = tree.add("📥 parse (Agent 1: Ticket Parser)")
    quality = parse.add("🔍 quality (Agent 2: Quality Inspector)")
    knowledge = parse.add("📚 knowledge (Agent 3: Knowledge Matcher)")
    merge = tree.add("🔀 merge (Result Aggregation)")
    merge.add("✅ END (auto-approved)")
    merge.add("👤 human_review → END (needs human)")
    console.print(Panel(tree, title="LangGraph State Machine"))

    for ticket in SAMPLE_TICKETS:
        console.print(f"\n{'='*60}")
        console.print(Panel(
            f"[bold]{ticket['title']}[/bold]\n\n{ticket['text'][:200]}...",
            title=f"📝 Test Ticket: {ticket['id']}",
        ))

        try:
            from graph import build_review_graph
            app = build_review_graph()
            result = app.invoke({
                "raw_ticket": ticket["text"],
                "parsed_ticket": {},
                "quality_report": {},
                "knowledge_matches": {},
                "final_verdict": "",
                "auto_comments": [],
                "auto_labels": [],
            })
            display_result(result)
        except Exception as e:
            console.print(f"[yellow]API not available, showing mock result[/yellow]: {e}")
            display_mock_result(ticket["id"])


def display_result(result: dict):
    """展示审查结果"""
    verdict = result.get("final_verdict", "unknown")
    color = {"approved": "green", "needs_revision": "yellow", "needs_human_review": "red"}.get(verdict, "white")

    # 质量报告
    qr = result.get("quality_report", {})
    table = Table(title="Quality Report")
    table.add_column("Score", style="bold")
    table.add_column("Issues")
    table.add_column("Severity Assessment")
    table.add_row(
        str(qr.get("quality_score", "N/A")),
        str(len(qr.get("issues", []))),
        f"{qr.get('severity_assessment', {}).get('claimed', '?')} → {qr.get('severity_assessment', {}).get('recommended', '?')}",
    )
    console.print(table)

    # 知识匹配
    km = result.get("knowledge_matches", {})
    if km.get("matches"):
        table = Table(title="Knowledge Matches")
        table.add_column("Historical ID")
        table.add_column("Similarity")
        table.add_column("Duplicate?")
        for m in km["matches"]:
            table.add_row(
                m.get("historical_id", ""),
                f"{m.get('similarity_score', 0):.2f}",
                "⚠ YES" if m.get("is_duplicate") else "No",
            )
        console.print(table)

    # 最终判定
    console.print(Panel(
        f"[{color} bold]Verdict: {verdict.upper()}[/{color} bold]\n\n"
        f"Auto-comments:\n" + "\n".join(f"  • {c}" for c in result.get("auto_comments", [])) + "\n\n"
        f"Auto-labels: {', '.join(result.get('auto_labels', []))}",
        title="📊 Final Review",
    ))


def display_mock_result(ticket_id: str):
    """Mock 结果展示（无 API 时使用）"""
    mocks = {
        "good": {
            "verdict": "approved",
            "score": 95,
            "comments": ["All fields complete", "No historical duplicates found"],
            "labels": [],
        },
        "poor": {
            "verdict": "needs_human_review",
            "score": 35,
            "comments": [
                "Missing reproduction steps → Please add step-by-step reproduction instructions",
                "Missing environment info → Specify OS, version, and deployment environment",
                "Missing expected behavior → Describe what should happen",
                "Severity P3 may be underrated → Description mentions 'broken' and 'ASAP'",
            ],
            "labels": ["needs-reproduction_steps", "needs-expected_behavior", "severity-reassessed"],
        },
        "duplicate": {
            "verdict": "needs_human_review",
            "score": 85,
            "comments": [
                "Potential duplicate of TICKET-1045 (currency conversion issue) — please confirm",
                "Severity reassessed: P1 matches the impact description",
            ],
            "labels": ["potential-duplicate"],
        },
    }
    m = mocks.get(ticket_id, mocks["good"])
    color = {"approved": "green", "needs_human_review": "red"}.get(m["verdict"], "yellow")
    console.print(Panel(
        f"[{color} bold]Verdict: {m['verdict'].upper()}[/{color} bold]  (Score: {m['score']})\n\n"
        f"Auto-comments:\n" + "\n".join(f"  • {c}" for c in m["comments"]) + "\n\n"
        f"Auto-labels: {', '.join(m['labels']) if m['labels'] else 'none'}",
        title="📊 Final Review (Mock)",
    ))


if __name__ == "__main__":
    run_demo()

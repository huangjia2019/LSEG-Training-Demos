"""
Workshop 2 — LangGraph 状态图编排
三个 Agent 的协作流水线：解析 → 并行（质检 + 知识匹配）→ 汇总 → 人工审批判断
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END

from agents.parser_agent import parse_ticket
from agents.quality_agent import inspect_quality
from agents.knowledge_agent import match_knowledge
from config import QUALITY_AUTO_PASS, QUALITY_NEEDS_REVISION


# ── 状态定义 ───────────────────────────────────────────────────

class TicketReviewState(TypedDict):
    """流水线状态：每个节点读写自己的字段"""
    raw_ticket: str                    # 原始工单文本
    parsed_ticket: dict                # Agent 1 输出
    quality_report: dict               # Agent 2 输出
    knowledge_matches: dict            # Agent 3 输出
    final_verdict: str                 # approved | needs_revision | needs_human_review
    auto_comments: list[str]           # 自动生成的审查意见
    auto_labels: list[str]             # 自动标签


# ── 节点函数 ───────────────────────────────────────────────────

def node_parse(state: TicketReviewState) -> dict:
    """节点 1: 工单解析"""
    parsed = parse_ticket(state["raw_ticket"])
    return {"parsed_ticket": parsed}


def node_quality(state: TicketReviewState) -> dict:
    """节点 2: 质量检测"""
    report = inspect_quality(state["parsed_ticket"])
    return {"quality_report": report}


def node_knowledge(state: TicketReviewState) -> dict:
    """节点 3: 知识库匹配"""
    matches = match_knowledge(state["parsed_ticket"])
    return {"knowledge_matches": matches}


def node_merge(state: TicketReviewState) -> dict:
    """节点 4: 结果汇总 + 风险分层判断（SDD 规范 §4）"""
    quality = state.get("quality_report", {})
    knowledge = state.get("knowledge_matches", {})

    score = quality.get("quality_score", 0)
    has_errors = any(i.get("severity") == "error" for i in quality.get("issues", []))
    is_duplicate = knowledge.get("potential_duplicate", False)
    severity_changed = (
        quality.get("severity_assessment", {}).get("claimed") !=
        quality.get("severity_assessment", {}).get("recommended")
    )

    # 自动生成审查意见
    comments = []
    labels = []

    for issue in quality.get("issues", []):
        comments.append(f"{issue.get('message', '')} → {issue.get('suggestion', '')}")
        if issue.get("severity") == "error":
            labels.append(f"needs-{issue.get('field', 'fix')}")

    if is_duplicate:
        dup_id = next(
            (m["historical_id"] for m in knowledge.get("matches", []) if m.get("is_duplicate")),
            "unknown"
        )
        comments.append(f"Potential duplicate of {dup_id} — please confirm")
        labels.append("potential-duplicate")

    if severity_changed:
        sa = quality.get("severity_assessment", {})
        comments.append(
            f"Severity reassessed: {sa.get('claimed')} → {sa.get('recommended')} ({sa.get('reason', '')})"
        )
        labels.append("severity-reassessed")

    # 风险分层决策（SDD 规范 §4）
    if score >= QUALITY_AUTO_PASS and not has_errors and not is_duplicate:
        verdict = "approved"
    elif score < QUALITY_NEEDS_REVISION or has_errors:
        verdict = "needs_human_review"
    else:
        verdict = "needs_revision"

    # P1 升级始终需要人工
    if quality.get("severity_assessment", {}).get("recommended") == "P1" and severity_changed:
        verdict = "needs_human_review"

    return {
        "final_verdict": verdict,
        "auto_comments": comments,
        "auto_labels": labels,
    }


# ── 条件路由 ───────────────────────────────────────────────────

def route_after_merge(state: TicketReviewState) -> str:
    """根据风险分层决定是否需要人工审批节点"""
    if state.get("final_verdict") == "needs_human_review":
        return "human_review"
    return "end"


def node_human_review(state: TicketReviewState) -> dict:
    """人工审批节点（Workshop 中模拟）"""
    # 在生产环境中，这里会发送通知给 Tech Lead 并等待响应
    # Workshop 中打印提示即可
    return {}  # 状态不变，由外部流程处理


# ── 构建 Graph ─────────────────────────────────────────────────

def build_review_graph() -> StateGraph:
    """构建工单审查流水线的 LangGraph 状态图"""
    graph = StateGraph(TicketReviewState)

    # 添加节点
    graph.add_node("parse", node_parse)
    graph.add_node("quality", node_quality)
    graph.add_node("knowledge", node_knowledge)
    graph.add_node("merge", node_merge)
    graph.add_node("human_review", node_human_review)

    # 定义边：解析 → 并行（质检 + 知识匹配）
    graph.set_entry_point("parse")
    graph.add_edge("parse", "quality")
    graph.add_edge("parse", "knowledge")

    # 并行结果 → 汇总
    graph.add_edge("quality", "merge")
    graph.add_edge("knowledge", "merge")

    # 汇总后条件路由
    graph.add_conditional_edges("merge", route_after_merge, {
        "human_review": "human_review",
        "end": END,
    })
    graph.add_edge("human_review", END)

    return graph.compile()

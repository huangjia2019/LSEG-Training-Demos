"""
Workshop 1 — 合规监管文档智能分析：完整流程
SDD 驱动：规范 → 解析 → 向量化 → 分析 → 质量检查 → 报告
"""
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from document_parser import load_document, split_documents
from rag_engine import build_vectorstore, search, load_vectorstore
from compliance_agent import analyze_compliance, quality_check, enrich_with_rag

console = Console()


def step0_show_spec():
    """SDD 第一步：展示规范文档"""
    spec_path = Path(__file__).parent.parent / "specs" / "compliance-spec.md"
    console.print(Panel(
        "[bold blue]SDD Step 0: Review Specification[/bold blue]\n\n"
        f"Spec file: {spec_path}\n"
        "Before writing any code, we defined:\n"
        "  • Input format (PDF/HTML/TXT)\n"
        "  • Output schema (JSON with changes, impact, actions)\n"
        "  • Quality rules (confidence threshold, citation required)\n"
        "  • Agent constraints (no fabrication, human review for high-impact)",
        title="📋 SDD Specification",
    ))


def step1_parse_document(path: str) -> list[dict]:
    """Step 1: 解析文档"""
    console.print(f"\n[bold]Step 1: Parsing document[/bold] — {path}")
    docs = load_document(path)
    chunks = split_documents(docs)
    console.print(f"  ✓ Loaded {len(docs)} pages, split into {len(chunks)} chunks")
    return chunks


def step2_build_rag(chunks: list[dict], collection: str = "compliance"):
    """Step 2: 构建 RAG 知识库"""
    console.print(f"\n[bold]Step 2: Building RAG knowledge base[/bold]")
    vs = build_vectorstore(chunks, collection)
    console.print(f"  ✓ Vectorstore ready ({collection})")
    return vs


def step3_analyze(new_text: str, baseline_text: str, scope: str) -> dict:
    """Step 3: 合规分析"""
    console.print(f"\n[bold]Step 3: Running compliance analysis[/bold] (scope: {scope})")

    # 从 RAG 获取相关内部知识
    rag_context = enrich_with_rag(f"{scope} compliance requirements")
    console.print(f"  → RAG context: {len(rag_context)} chars retrieved")

    report = analyze_compliance(new_text, baseline_text, scope, rag_context)
    console.print(f"  ✓ Analysis complete: {len(report.get('changes', []))} changes found")
    return report


def step4_quality_gate(report: dict):
    """Step 4 (SDD 闭环): 质量检查"""
    console.print(f"\n[bold]Step 4: SDD Quality Gate[/bold]")

    review_needed, reason = report.get("review_required", False), report.get("review_reason", "")

    table = Table(title="Quality Check Results")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")

    changes = report.get("changes", [])
    # 引用完整性
    cited = sum(1 for c in changes if c.get("source_reference"))
    table.add_row("Citation completeness", f"{cited}/{len(changes)} changes cited")

    # 置信度
    low_conf = sum(1 for c in changes if c.get("confidence", 0) < 0.8)
    status = f"[red]{low_conf} below threshold[/red]" if low_conf else "All above 0.8"
    table.add_row("Confidence threshold", status)

    # 高影响有行动建议
    high_no_action = sum(1 for c in changes
                         if c.get("impact_level") == "high" and not c.get("recommended_action"))
    status = f"[red]{high_no_action} missing[/red]" if high_no_action else "All covered"
    table.add_row("High-impact actions", status)

    console.print(table)

    if review_needed:
        console.print(f"\n[yellow]⚠ Human review required: {reason}[/yellow]")
    else:
        console.print(f"\n[green]✓ All quality checks passed[/green]")


def step5_output_report(report: dict):
    """Step 5: 输出报告"""
    console.print(f"\n[bold]Step 5: Generating report[/bold]")

    # 保存 JSON 报告
    output_path = Path("output") / f"{report.get('report_id', 'report')}.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"  ✓ Report saved: {output_path}")

    # 打印摘要
    console.print(Panel(
        f"[bold]Report ID:[/bold] {report.get('report_id')}\n"
        f"[bold]Summary:[/bold] {report.get('summary', 'N/A')}\n"
        f"[bold]Overall Impact:[/bold] {report.get('overall_impact', 'N/A')}\n"
        f"[bold]Changes Found:[/bold] {len(report.get('changes', []))}\n"
        f"[bold]Action Items:[/bold] {len(report.get('action_items', []))}\n"
        f"[bold]Review Required:[/bold] {'Yes' if report.get('review_required') else 'No'}",
        title="📊 Compliance Impact Report",
    ))

    # 打印行动项
    if report.get("action_items"):
        table = Table(title="Action Items")
        table.add_column("#", style="bold")
        table.add_column("Action")
        table.add_column("Timeline")
        table.add_column("Team")
        for item in report["action_items"]:
            table.add_row(
                str(item.get("priority", "")),
                item.get("action", ""),
                item.get("deadline_suggestion", ""),
                item.get("responsible_team", ""),
            )
        console.print(table)


# ── Demo 模式（无需真实 API） ──────────────────────────────────

def run_demo():
    """使用示例数据演示完整流程（课堂演示用）"""
    console.print(Panel(
        "[bold]Workshop 1: 合规监管文档智能分析[/bold]\n"
        "场景：MAS Notice 648 修订 — 反洗钱客户尽职调查门槛下调",
        title="🏦 LSEG Compliance Agent Workshop",
    ))

    step0_show_spec()

    # 模拟文档内容
    new_doc = """
MAS Notice 648 (Amendment No. 3) — March 2026

Section 3.2 Customer Due Diligence (CDD)
3.2.1 Financial institutions shall verify the source of funds for all transactions
exceeding SGD 5,000 (amended from SGD 20,000).

3.2.2 Enhanced Due Diligence (EDD) is now mandatory for:
(a) Politically Exposed Persons (PEPs) from jurisdictions rated "high-risk" by FATF
(b) All new corporate accounts with beneficial owners from non-cooperative jurisdictions
(c) Transactions involving virtual assets exceeding SGD 1,000

Section 4.1 Suspicious Transaction Reporting (STR)
4.1.1 The reporting window for suspicious transactions is reduced from 15 business days
to 5 business days from the date of detection.

4.1.2 Financial institutions must implement automated transaction monitoring systems
capable of real-time screening by January 2027.

Section 5.3 Record Keeping
5.3.1 All CDD records must be retained for a minimum of 7 years (amended from 5 years).
"""

    baseline_doc = """
MAS Notice 648 (Original) — 2020

Section 3.2 Customer Due Diligence (CDD)
3.2.1 Financial institutions shall verify the source of funds for all transactions
exceeding SGD 20,000.

Section 4.1 Suspicious Transaction Reporting (STR)
4.1.1 The reporting window for suspicious transactions is 15 business days
from the date of detection.

Section 5.3 Record Keeping
5.3.1 All CDD records must be retained for a minimum of 5 years.
"""

    # Step 1: 解析（使用内存中的文本，跳过文件加载）
    console.print(f"\n[bold]Step 1: Document parsed[/bold] (demo mode — using in-memory text)")
    console.print(f"  ✓ New document: {len(new_doc)} chars")
    console.print(f"  ✓ Baseline: {len(baseline_doc)} chars")

    # Step 2: RAG（跳过，demo 模式无需向量库）
    console.print(f"\n[bold]Step 2: RAG knowledge base[/bold] (skipped in demo mode)")

    # Step 3: 分析
    report = step3_analyze(new_doc, baseline_doc, scope="AML/KYC")

    # Step 4: 质量检查
    step4_quality_gate(report)

    # Step 5: 输出
    step5_output_report(report)


def run_full(new_doc_path: str, baseline_path: str = "", sop_path: str = "", scope: str = "General"):
    """完整流程（需要真实 API）"""
    step0_show_spec()

    # Step 1
    new_chunks = step1_parse_document(new_doc_path)
    new_text = "\n\n".join(c["page_content"] for c in new_chunks)

    baseline_text = ""
    if baseline_path:
        baseline_chunks = step1_parse_document(baseline_path)
        baseline_text = "\n\n".join(c["page_content"] for c in baseline_chunks)

    # Step 2: 如果有 SOP，建立 RAG
    if sop_path:
        sop_chunks = step1_parse_document(sop_path)
        step2_build_rag(sop_chunks, "company_sop")

    # Step 3
    report = step3_analyze(new_text, baseline_text, scope)

    # Step 4
    step4_quality_gate(report)

    # Step 5
    step5_output_report(report)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_full(
            new_doc_path=sys.argv[1],
            baseline_path=sys.argv[2] if len(sys.argv) > 2 else "",
            sop_path=sys.argv[3] if len(sys.argv) > 3 else "",
            scope=sys.argv[4] if len(sys.argv) > 4 else "General",
        )
    else:
        run_demo()

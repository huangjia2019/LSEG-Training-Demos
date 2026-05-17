#!/usr/bin/env python3
"""Build visual walkthrough pages and blueprint diagrams for the LSEG workshops."""
from __future__ import annotations

import html
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
VISUAL_ASSETS = ROOT / "assets" / "visual"
WORKSHOP_VISUAL = ROOT / "workshops" / "_visual"

BG = (7, 13, 27)
BG2 = (10, 22, 38)
PANEL = (18, 34, 58)
PANEL2 = (24, 45, 73)
TEXT = (239, 247, 255)
MUTED = (164, 183, 204)
DIM = (108, 129, 152)
CYAN = (33, 214, 255)
GREEN = (60, 222, 151)
ORANGE = (255, 169, 64)
PINK = (255, 112, 176)
PURPLE = (163, 132, 255)
YELLOW = (255, 221, 90)
RED = (255, 98, 98)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = [
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for name in names:
        path = Path(name)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


F = {
    "hero": _font(50, True),
    "title": _font(34, True),
    "subtitle": _font(25, False),
    "body": _font(22, False),
    "small": _font(18, False),
    "tiny": _font(14, False),
    "label": _font(18, True),
    "mono": _font(18, False),
}


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        test = word if not line else f"{line} {word}"
        if text_size(draw, test, font)[0] <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    width: int,
    line_gap: int = 6,
) -> int:
    x, y = xy
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def draw_wrapped_limited(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    width: int,
    max_lines: int,
    line_gap: int = 4,
) -> int:
    lines = wrap(draw, text, font, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".") + "..."
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def round_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill, outline, radius=24, width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], fill, width=5):
    draw.line((start, end), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 18
    for delta in (math.pi * 0.82, -math.pi * 0.82):
        p = (end[0] + length * math.cos(angle + delta), end[1] + length * math.sin(angle + delta))
        draw.line((end, p), fill=fill, width=width)


def chip(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color, max_w: int | None = None) -> int:
    font = F["tiny"]
    w, h = text_size(draw, label, font)
    if max_w and w + 26 > max_w:
        label = label[: max(8, int(max_w / 10))] + "..."
        w, h = text_size(draw, label, font)
    round_rect(draw, (x, y, x + w + 28, y + 32), fill=(13, 27, 45), outline=color, radius=16, width=2)
    draw.text((x + 14, y + 8), label, font=font, fill=TEXT)
    return x + w + 40


def draw_background(draw: ImageDraw.ImageDraw, w: int, h: int):
    for i in range(h):
        mix = i / h
        r = int(BG[0] * (1 - mix) + BG2[0] * mix)
        g = int(BG[1] * (1 - mix) + BG2[1] * mix)
        b = int(BG[2] * (1 - mix) + BG2[2] * mix)
        draw.line((0, i, w, i), fill=(r, g, b))
    for x in range(0, w, 72):
        draw.line((x, 0, x, h), fill=(18, 35, 56), width=1)
    for y in range(0, h, 72):
        draw.line((0, y, w, y), fill=(18, 35, 56), width=1)
    draw.ellipse((-220, -260, 540, 460), outline=(23, 132, 161), width=3)
    draw.ellipse((1290, 760, 2080, 1410), outline=(62, 156, 126), width=3)


CASES = {
    "workshop1": {
        "title": "Workshop 1 · Regulatory Document Agent",
        "subtitle": "Spec-driven compliance analysis: evidence, RAG, quality gates, and audit trace.",
        "file": "workshop1-pattern-blueprint.png",
        "accent": GREEN,
        "repo": "workshops/workshop1-compliance",
        "work_object": "Input evidence: MAS amendment, previous notice, internal AML/KYC SOP, and scope tag.",
        "command": "cd workshops/workshop1-compliance\npython3 -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\ncd src\npython main.py",
        "screenshot": "../../../assets/screenshots/workshop1-compliance-terminal.png",
        "stages": [
            ("01", "SDD Contract", "Input schema, output JSON, citation rule, confidence threshold.", "Spec as Contract", GREEN),
            ("02", "Document Intake", "Read MAS amendment, baseline notice, and internal AML/KYC SOP.", "Context Triage", CYAN),
            ("03", "Semantic Diff", "Turn long clauses into changed obligations and impact rows.", "Semantic Compaction", PURPLE),
            ("04", "Policy RAG", "Ground interpretation in internal policies and source references.", "RAG Pipeline", CYAN),
            ("05", "Impact Report", "Emit cited impact, action items, owner, due date, and severity.", "Prompt Chaining", ORANGE),
            ("06", "Quality Gate", "Block weak evidence, low confidence, or high-impact missing action.", "Approval Gate", YELLOW),
        ],
        "controls": [
            ("Evidence Contract", "Every change needs source, clause, version, and rationale."),
            ("Autonomy Boundary", "Low confidence and high impact trigger review instead of auto-action."),
            ("Observability", "The output keeps parsed changes, confidence, checks, and next actions visible."),
        ],
        "patterns": ["Context Triage", "Semantic Compaction", "RAG Pipeline", "Prompt Chaining", "Approval Gate", "Observability Harness"],
        "insight": "The finance value is not a fluent summary. It is a reviewable chain from document evidence to operational action.",
    },
    "workshop2": {
        "title": "Workshop 2 · Multi-Agent Ticket Review",
        "subtitle": "A structured state graph for parser, quality, knowledge, merge, and human review.",
        "file": "workshop2-pattern-blueprint.png",
        "accent": PINK,
        "repo": "workshops/workshop2-ticket-review",
        "work_object": "Input evidence: raw support ticket, component, priority, environment, and historical issue hints.",
        "command": "cd workshops/workshop2-ticket-review\npython3 -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\ncd src\npython main.py",
        "screenshot": "../../../assets/screenshots/workshop2-ticket-review-terminal.png",
        "stages": [
            ("01", "Raw Ticket", "Capture user text, metadata, priority, component, and environment.", "Context Triage", CYAN),
            ("02", "Parser Agent", "Extract structured JSON so later agents do not parse prose again.", "Tool Dispatch", GREEN),
            ("03", "Quality Agent", "Check reproduction steps, environment, expected behavior, and evidence.", "Adversarial Review", PINK),
            ("04", "Knowledge Agent", "Search historical issues and detect duplicates or known incidents.", "RAG Pipeline", CYAN),
            ("05", "Merge Node", "Join parallel findings into one risk-tiered decision state.", "Fan-out/Gather", PURPLE),
            ("06", "Human Review", "Route weak, duplicate, or high-priority cases to a reviewer.", "Approval Gate", YELLOW),
        ],
        "controls": [
            ("State Isolation", "Each role reads the fields it needs and returns one structured report."),
            ("Risk Routing", "The graph decides approved, needs revision, or human review."),
            ("Audit Trail", "Scores, duplicate evidence, and routing reason stay attached to the ticket."),
        ],
        "patterns": ["Handoff Chain", "Fan-out/Gather", "Adversarial Review", "RAG Pipeline", "Approval Gate", "Observability Harness"],
        "insight": "Multi-agent design only pays off when responsibilities, state, and review boundaries are explicit.",
    },
    "workshop3": {
        "title": "Workshop 3 · Copilot + SDD Meeting Agent",
        "subtitle": "One specification drives prompt, code, validation, and reusable delivery behavior.",
        "file": "workshop3-pattern-blueprint.png",
        "accent": YELLOW,
        "repo": "workshops/workshop3-copilot-demo",
        "work_object": "Input evidence: meeting transcript, output schema, quality rules, and follow-up email contract.",
        "command": "cd workshops/workshop3-copilot-demo\npython3 -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\ncd src\npython main.py",
        "screenshot": "../../../assets/screenshots/workshop3-copilot-terminal.png",
        "stages": [
            ("01", "Spec Context", "Meeting output schema, quality checks, and follow-up email rules.", "Spec as Contract", GREEN),
            ("02", "Copilot Plan", "Generate project structure from the spec instead of loose prompts.", "Plan-and-Execute", CYAN),
            ("03", "Prompt Chain", "Separate extraction, validation, and email generation prompts.", "Prompt Chaining", ORANGE),
            ("04", "Validation", "Use the same spec to check JSON fields, owners, dates, and length.", "Generator-Critic", PINK),
            ("05", "Skill Package", "Package prompt, schema, examples, and run path into reusable work.", "Skill Package", PURPLE),
            ("06", "Progressive Commit", "Move from mock run to model-backed run to team workflow.", "Progressive Commitment", YELLOW),
        ],
        "controls": [
            ("Spec Reuse", "The same document feeds Copilot, runtime prompts, tests, and review."),
            ("Quality Loop", "Validation is a first-class step, not a final eyeball check."),
            ("Delivery Boundary", "Start with mock path, then promote once outputs and checks are stable."),
        ],
        "patterns": ["Prompt Chaining", "Plan-and-Execute", "Generator-Critic", "Skill Package", "Progressive Commitment", "Guardrail Sandwich"],
        "insight": "SDD turns AI-assisted coding into governed system design: spec first, generated code second, validation always on.",
    },
}


DEMO_DATA = {
    "workshop1": {
        "title": "Interactive run · regulatory impact analysis",
        "scenarios": [
            {
                "label": "MAS AML/KYC amendment",
                "summary": "Lower CDD threshold, shorter STR window, internal SOP impact.",
                "steps": [
                    {
                        "name": "Load SDD contract",
                        "pattern": "Spec as Contract",
                        "log": "Loaded compliance-spec.md: inputs, output schema, citation rule, confidence threshold.",
                        "state": {"spec": "compliance-spec.md", "required_fields": ["changes", "impact", "actions", "quality"], "citation_required": True, "confidence_threshold": 0.8},
                        "output": "Contract accepted. The agent cannot emit uncited findings.",
                    },
                    {
                        "name": "Parse evidence",
                        "pattern": "Context Triage",
                        "log": "Parsed MAS amendment, baseline notice, and internal AML/KYC SOP as separate evidence streams.",
                        "state": {"new_doc_chars": 949, "baseline_chars": 429, "internal_policy": "company-sop-aml.txt", "scope": "AML/KYC"},
                        "output": "Evidence map created: new notice, baseline notice, internal SOP.",
                    },
                    {
                        "name": "Extract semantic diff",
                        "pattern": "Semantic Compaction",
                        "log": "Compressed long clauses into two material changes with clause anchors.",
                        "state": {"changes_found": 2, "changed_topics": ["CDD threshold", "STR reporting window"], "clauses": ["4.2", "7.1"]},
                        "output": "Two impact rows generated from changed clauses.",
                    },
                    {
                        "name": "Ground with policy",
                        "pattern": "RAG Pipeline",
                        "log": "Matched changes to AML SOP controls and implementation teams.",
                        "state": {"policy_matches": 3, "teams": ["Compliance Operations", "Engineering + Compliance"], "source_refs": 2},
                        "output": "Internal policy context attached to each impact row.",
                    },
                    {
                        "name": "Generate report",
                        "pattern": "Prompt Chaining",
                        "log": "Created structured impact report with actions, owners, dates, and rationale.",
                        "state": {"report_id": "CR-2026-0517-DEMO", "overall_impact": "high", "action_items": 2, "review_required": False},
                        "output": "Report ready: high impact, two action items, no open citation gaps.",
                    },
                    {
                        "name": "Apply quality gate",
                        "pattern": "Approval Gate",
                        "log": "Citation completeness 2/2, all confidence values above threshold, high-impact actions covered.",
                        "state": {"citation_completeness": "2/2", "confidence": ">=0.86", "gate": "PASS", "observability": ["citations", "confidence", "actions", "checks"]},
                        "output": "PASS: the report is reviewable and can move to compliance review workflow.",
                    },
                ],
                "final": {
                    "verdict": "PASS",
                    "headline": "Compliance impact report generated",
                    "cards": [
                        ["Changes", "2 material changes"],
                        ["Impact", "High"],
                        ["Actions", "Revise AML SOP; pilot RAG-backed review"],
                        ["Patterns", "SDD + RAG + Approval Gate"],
                    ],
                },
            }
        ],
    },
    "workshop2": {
        "title": "Interactive run · multi-agent ticket review",
        "scenarios": [
            {
                "label": "Good ticket",
                "summary": "Complete reproduction steps and no historical duplicate.",
                "final": {"verdict": "APPROVED", "headline": "Ticket can move automatically", "cards": [["Score", "95"], ["Route", "Auto-approved"], ["Labels", "none"], ["Review", "No human review"]]},
                "signals": {"quality_score": 95, "duplicate": False, "risk": "low"},
            },
            {
                "label": "Poor ticket",
                "summary": "Missing reproduction steps, environment, and expected behavior.",
                "final": {"verdict": "NEEDS_HUMAN_REVIEW", "headline": "Ticket needs clarification", "cards": [["Score", "35"], ["Route", "Human review"], ["Labels", "needs-reproduction_steps"], ["Review", "Required"]]},
                "signals": {"quality_score": 35, "duplicate": False, "risk": "high"},
            },
            {
                "label": "Potential duplicate",
                "summary": "Good structure, but similar to TICKET-1045 and marked P1.",
                "final": {"verdict": "NEEDS_HUMAN_REVIEW", "headline": "Duplicate risk blocks auto-close", "cards": [["Score", "85"], ["Route", "Human review"], ["Labels", "potential-duplicate"], ["Review", "Required"]]},
                "signals": {"quality_score": 85, "duplicate": True, "risk": "medium"},
            },
        ],
        "step_template": [
            ["Raw Ticket", "Context Triage", "Ticket text, priority, component, and environment are captured as the work object."],
            ["Parser Agent", "Tool Dispatch", "Parser turns prose into structured JSON fields."],
            ["Quality Agent", "Adversarial Review", "Quality role challenges completeness, priority, reproduction steps, and evidence."],
            ["Knowledge Agent", "RAG Pipeline", "Knowledge role searches historical tickets and known incident patterns."],
            ["Merge Node", "Fan-out/Gather", "Parallel findings merge into one decision state."],
            ["Human Review", "Approval Gate", "Risk tier decides auto-pass, revision, or human review."],
        ],
    },
    "workshop3": {
        "title": "Interactive run · Copilot + SDD meeting agent",
        "scenarios": [
            {
                "label": "Compliance review meeting",
                "summary": "Transcript contains AML monitoring actions, owners, and deadlines.",
                "steps": [
                    {
                        "name": "Load meeting-agent spec",
                        "pattern": "Spec as Contract",
                        "log": "Loaded schema: summary, key_points, action_items, follow-up email.",
                        "state": {"spec": "meeting-agent-spec.md", "summary_limit": "100 words", "min_key_points": 2, "actions_need_owner": True},
                        "output": "Copilot and runtime prompt now share one contract.",
                    },
                    {
                        "name": "Generate implementation plan",
                        "pattern": "Plan-and-Execute",
                        "log": "Planned functions: generate_minutes(), validate_minutes(), generate_email().",
                        "state": {"modules": ["meeting_agent.py", "main.py"], "functions": ["generate_minutes", "validate_minutes", "generate_email"]},
                        "output": "Project structure follows the spec instead of a loose prompt.",
                    },
                    {
                        "name": "Run prompt chain",
                        "pattern": "Prompt Chaining",
                        "log": "Extracted summary, key points, decisions, and action items from transcript.",
                        "state": {"participants": 4, "key_points": 4, "action_items": 5, "draft_email": True},
                        "output": "Meeting minutes JSON generated.",
                    },
                    {
                        "name": "Validate output",
                        "pattern": "Generator-Critic",
                        "log": "Checked summary length, owner coverage, topic count, and concrete deadlines.",
                        "state": {"summary_length": 33, "assignee_coverage": "all assigned", "concrete_deadlines": True, "quality_gate": "PASS"},
                        "output": "Quality check passes against the same SDD spec.",
                    },
                    {
                        "name": "Package reusable skill",
                        "pattern": "Skill Package",
                        "log": "Grouped prompt, schema, examples, validation, and run path as a reusable workflow.",
                        "state": {"package_parts": ["prompt", "schema", "examples", "validation", "run path"], "reuse": "team workflow"},
                        "output": "The work can be reused instead of copied as one-off prompt text.",
                    },
                    {
                        "name": "Progressively commit",
                        "pattern": "Progressive Commitment",
                        "log": "Mock path is stable; next promotion is model-backed run, then team rollout.",
                        "state": {"phase": "mock stable", "next": "model-backed run", "blast_radius": "limited"},
                        "output": "The workflow is ready for controlled promotion.",
                    },
                ],
                "final": {
                    "verdict": "PASS",
                    "headline": "Structured minutes and follow-up email generated",
                    "cards": [
                        ["Key points", "4"],
                        ["Action items", "5 assigned"],
                        ["Quality", "All checks pass"],
                        ["Patterns", "Prompt Chain + Critic + Skill Package"],
                    ],
                },
            }
        ],
    },
}


SHOWCASE_BLUEPRINTS = {
    "mas_doc": {
        "title": "Showcase · MAS Document Analysis Pipeline",
        "subtitle": "A five-step analyst workflow from revised notice to product impact and action report.",
        "file": "mas-document-analysis-blueprint.png",
        "accent": CYAN,
        "repo": "showcases/finance/demo-doc-analysis",
        "work_object": "Input evidence: revised MAS notice, previous baseline, section map, product catalogue, and compliance checklist.",
        "stages": [
            ("01", "Notice Intake", "Read revised regulation, normalize sections, and keep source anchors.", "Context Triage", CYAN),
            ("02", "Version Diff", "Compare old and new text and isolate material changes.", "Semantic Compaction", PURPLE),
            ("03", "Obligation Extract", "Turn changed clauses into obligations, owners, timelines, and severity.", "Prompt Chaining", ORANGE),
            ("04", "Product Map", "Connect obligations to affected products, teams, and controls.", "RAG Pipeline", GREEN),
            ("05", "Impact Report", "Create readiness score, risk matrix, and action register.", "Progress Tracking", YELLOW),
            ("06", "Review Loop", "Escalate ambiguous or high-impact findings to human review.", "Approval Gate", PINK),
        ],
        "controls": [
            ("Version Evidence", "Every impact row can point back to the changed clause and source version."),
            ("Business Mapping", "The useful unit is product impact, not document summary."),
            ("Progress Visibility", "Readiness score and action register turn analysis into follow-through."),
        ],
        "patterns": ["Context Triage", "Semantic Compaction", "RAG Pipeline", "Progress Tracking", "Approval Gate", "Observability Harness"],
        "insight": "Regulatory intelligence becomes useful when document change is translated into product-level obligations and accountable actions.",
    },
    "mas_compliance": {
        "title": "Showcase · MAS Compliance Analyst Agent",
        "subtitle": "A product-aware compliance workspace with rule retrieval, risk warnings, review gates, and evidence.",
        "file": "mas-compliance-analyst-blueprint.png",
        "accent": ORANGE,
        "repo": "showcases/finance/demo-MAS-analyst",
        "work_object": "Input evidence: product profile, customer/product constraints, MAS knowledge base, sales or workflow context.",
        "stages": [
            ("01", "Product Profile", "Read product category, channel, customer segment, and risk context.", "Context Triage", CYAN),
            ("02", "Rule Retrieval", "Retrieve bounded MAS requirements and internal policy snippets.", "RAG Pipeline", GREEN),
            ("03", "Tool Dispatch", "Call product checks, customer suitability checks, and task automation.", "Tool Dispatch", ORANGE),
            ("04", "Risk Scoring", "Convert rules and context into warnings, blockers, and review needs.", "Guardrail Sandwich", PINK),
            ("05", "Checklist Output", "Create product-specific compliance checklist and next actions.", "Skill Package", PURPLE),
            ("06", "Review Gate", "Escalate high-risk cases and preserve evidence for audit.", "Approval Gate", YELLOW),
        ],
        "controls": [
            ("Product Boundary", "The agent changes behavior by product type and customer context."),
            ("Risk Gate", "Warnings determine autonomy, documentation, and escalation path."),
            ("Evidence Log", "Rules, checks, generated actions, and review status remain inspectable."),
        ],
        "patterns": ["Tool Dispatch", "RAG Pipeline", "Guardrail Sandwich", "Approval Gate", "Progressive Commitment", "Observability Harness"],
        "insight": "A finance agent should behave less like a chat surface and more like a product-aware compliance router.",
    },
}


def draw_case_blueprint(case: dict):
    w, h = 1800, 1125
    im = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(im)
    draw_background(draw, w, h)
    accent = case["accent"]

    title_bottom = draw_wrapped(draw, (78, 54), case["title"], F["hero"], TEXT, 1210, 6)
    draw_wrapped(draw, (82, title_bottom + 8), case["subtitle"], F["subtitle"], MUTED, 1220, 8)
    round_rect(draw, (1340, 66, 1718, 156), fill=(12, 28, 48), outline=accent, radius=28, width=3)
    draw.text((1368, 92), "Pattern Blueprint", font=F["title"], fill=accent)

    x = 82
    for p in case["patterns"]:
        x = chip(draw, x, 210, p, accent)

    # Lanes
    round_rect(draw, (70, 280, 500, 860), fill=(12, 27, 47), outline=(46, 72, 103), radius=28, width=2)
    round_rect(draw, (540, 280, 1275, 860), fill=(11, 25, 43), outline=accent, radius=28, width=3)
    round_rect(draw, (1315, 280, 1730, 860), fill=(12, 27, 47), outline=(46, 72, 103), radius=28, width=2)
    draw.text((105, 315), "Financial work object", font=F["title"], fill=CYAN)
    draw_wrapped(draw, (108, 375), case["work_object"], F["body"], TEXT, 335, 8)
    draw.text((105, 650), "Run path", font=F["label"], fill=YELLOW)
    draw_wrapped(draw, (108, 686), case["repo"], F["mono"], MUTED, 345, 6)
    draw_wrapped(draw, (108, 726), "python src/main.py", F["mono"], ORANGE, 345, 6)

    draw.text((582, 315), "Agent pipeline", font=F["title"], fill=accent)
    positions = [
        (580, 378), (823, 378), (1066, 378),
        (580, 620), (823, 620), (1066, 620),
    ]
    for idx, (num, title, body, pattern, color) in enumerate(case["stages"]):
        x0, y0 = positions[idx]
        round_rect(draw, (x0, y0, x0 + 202, y0 + 188), fill=PANEL, outline=color, radius=18, width=3)
        draw.text((x0 + 18, y0 + 18), num, font=F["label"], fill=color)
        draw_wrapped(draw, (x0 + 18, y0 + 48), title, F["label"], TEXT, 154, 4)
        draw_wrapped_limited(draw, (x0 + 18, y0 + 91), body, F["tiny"], MUTED, 160, 3, 3)
        chip(draw, x0 + 18, y0 + 146, pattern, color, 160)
        if idx not in (2, 5):
            sx, sy = x0 + 202, y0 + 94
            nx, ny = positions[idx + 1]
            arrow(draw, (sx + 12, sy), (nx - 14, ny + 94), color, 4)
    arrow(draw, (1165, 580), (675, 608), accent, 4)

    draw.text((1350, 315), "Control plane", font=F["title"], fill=GREEN)
    y = 382
    for title, body in case["controls"]:
        round_rect(draw, (1350, y, 1695, y + 118), fill=PANEL2, outline=(56, 82, 112), radius=18, width=2)
        draw.text((1372, y + 18), title, font=F["label"], fill=GREEN)
        draw_wrapped(draw, (1372, y + 50), body, F["tiny"], MUTED, 292, 4)
        y += 142

    round_rect(draw, (70, 904, 1730, 1048), fill=(9, 20, 35), outline=accent, radius=28, width=3)
    draw.text((105, 936), "Design insight", font=F["title"], fill=accent)
    draw_wrapped(draw, (420, 935), case["insight"], F["subtitle"], TEXT, 1180, 10)
    draw.text((78, 1070), "Read left to right: evidence enters, state becomes structured, patterns control autonomy, output remains auditable.", font=F["small"], fill=DIM)
    VISUAL_ASSETS.mkdir(parents=True, exist_ok=True)
    im.save(VISUAL_ASSETS / case["file"])


def draw_ladder():
    w, h = 1800, 1125
    im = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(im)
    draw_background(draw, w, h)
    draw.text((78, 64), "Finance Agent Learning Arc", font=F["hero"], fill=TEXT)
    draw_wrapped(draw, (82, 138), "Two visual showcases plus three runnable workshops. Each step adds more pattern vocabulary and stronger design judgment.", F["subtitle"], MUTED, 1420, 8)
    steps = [
        ("Showcase A", "MAS Document Analysis", "Watch a full business pipeline: ingest, compare, extract, map, report.", CYAN),
        ("Lab 1", "Regulatory Agent", "Run a spec-driven compliance pipeline and identify evidence + gate patterns.", GREEN),
        ("Map", "28-pattern Lens", "Use the matrix to name perception, memory, action, collaboration, and governance decisions.", PURPLE),
        ("Lab 2", "Multi-Agent Ticket Review", "Stress-test topology: fan-out, handoff, isolation, review, risk routing.", PINK),
        ("Lab 3", "Copilot + SDD", "Close the loop: spec, generation, validation, skill packaging, progressive delivery.", YELLOW),
        ("Showcase B", "Compliance Analyst", "Read the product-mapping layer: controls, warnings, review gate, evidence.", ORANGE),
    ]
    y = 270
    prev_mid = None
    for i, (label, title, body, color) in enumerate(steps):
        x0 = 110 + (i % 3) * 545
        if i == 3:
            y = 645
        box = (x0, y, x0 + 465, y + 240)
        round_rect(draw, box, fill=PANEL, outline=color, radius=26, width=4)
        draw.text((x0 + 28, y + 24), label, font=F["label"], fill=color)
        draw_wrapped_limited(draw, (x0 + 28, y + 64), title, F["title"], TEXT, 390, 2, 5)
        draw_wrapped_limited(draw, (x0 + 28, y + 154), body, F["small"], MUTED, 390, 3, 5)
        mid = (x0 + 465, y + 120)
        if prev_mid and i not in (3,):
            arrow(draw, prev_mid, (x0 - 18, y + 120), color, 5)
        if i == 3:
            arrow(draw, (110 + 2 * 545 + 230, 270 + 260), (x0 + 230, y - 20), PURPLE, 5)
        prev_mid = mid
    round_rect(draw, (110, 930, 1690, 1038), fill=(9, 20, 35), outline=GREEN, radius=26, width=3)
    draw.text((142, 960), "Repeated design loop", font=F["title"], fill=GREEN)
    draw_wrapped(draw, (610, 960), "Sketch first design -> inspect demo evidence -> map patterns -> revise architecture -> decide what needs governance before production.", F["body"], TEXT, 990, 8)
    im.save(VISUAL_ASSETS / "workshop-ladder-blueprint.png")


CSS = """\
:root {
  color-scheme: dark;
  --bg: #07101e;
  --panel: #101f34;
  --panel-2: #172b46;
  --line: #33516f;
  --text: #f3f8ff;
  --muted: #a8bbd2;
  --cyan: #21d6ff;
  --green: #3cde97;
  --orange: #ffa940;
  --pink: #ff70b0;
  --purple: #a384ff;
  --yellow: #ffdd5a;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background:
    linear-gradient(145deg, rgba(33, 214, 255, 0.10), transparent 34%),
    radial-gradient(circle at 85% 10%, rgba(60, 222, 151, 0.12), transparent 30%),
    var(--bg);
  color: var(--text);
  line-height: 1.55;
}
a { color: var(--cyan); }
.lab-shell { max-width: 1180px; margin: 0 auto; padding: 40px 24px 64px; }
.lab-nav { display: flex; justify-content: space-between; gap: 16px; color: var(--muted); font-size: 14px; margin-bottom: 42px; }
.lab-hero { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 28px; align-items: stretch; margin-bottom: 32px; }
.hero-copy, .hero-panel, .section, .step-card, .pattern-card, .run-panel {
  background: rgba(16, 31, 52, 0.86);
  border: 1px solid var(--line);
  border-radius: 18px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25);
}
.hero-copy { padding: 34px; }
.eyebrow { color: var(--cyan); font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; font-size: 13px; }
h1 { font-size: clamp(34px, 5vw, 62px); line-height: 1.02; margin: 12px 0 18px; }
.lede { color: var(--muted); font-size: 19px; max-width: 760px; }
.hero-panel { padding: 24px; display: grid; gap: 14px; align-content: start; }
.metric { border-left: 3px solid var(--green); padding-left: 14px; }
.metric strong { display: block; color: var(--text); }
.metric span { color: var(--muted); font-size: 14px; }
.blueprint { margin: 32px 0; }
.blueprint img, .screenshot img { width: 100%; border: 1px solid var(--line); border-radius: 18px; background: #050b14; }
.section { padding: 28px; margin: 28px 0; }
h2 { margin: 0 0 18px; font-size: 28px; }
.step-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.step-card { padding: 18px; }
.step-number { color: var(--orange); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight: 800; }
.step-card h3 { margin: 8px 0; font-size: 18px; }
.step-card p { color: var(--muted); margin: 0 0 12px; font-size: 14px; }
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.chip { border: 1px solid var(--cyan); border-radius: 999px; color: var(--text); padding: 4px 10px; font-size: 12px; background: rgba(33, 214, 255, 0.08); }
.pattern-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.pattern-card { padding: 18px; border-radius: 14px; }
.pattern-card h3 { margin: 0 0 8px; color: var(--green); font-size: 16px; }
.pattern-card p { margin: 0; color: var(--muted); font-size: 14px; }
.run-panel { padding: 20px; background: #050b14; overflow-x: auto; }
pre { margin: 0; white-space: pre-wrap; color: var(--yellow); font-size: 14px; }
.insight { border-left: 4px solid var(--yellow); padding-left: 18px; color: var(--text); font-size: 18px; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: start; }
figcaption { color: var(--muted); font-size: 13px; margin-top: 8px; }
.section-heading { display: flex; align-items: center; justify-content: space-between; gap: 18px; margin-bottom: 16px; }
.section-heading h2 { margin-bottom: 0; }
.simulator { border-color: rgba(60, 222, 151, 0.65); background: rgba(8, 20, 35, 0.94); }
.sim-controls { display: flex; flex-wrap: wrap; gap: 10px; justify-content: flex-end; }
.sim-controls select,
.sim-controls button {
  background: #07101e;
  border: 1px solid var(--line);
  border-radius: 10px;
  color: var(--text);
  font: inherit;
  font-size: 14px;
  min-height: 40px;
  padding: 8px 12px;
}
.sim-controls button { cursor: pointer; font-weight: 800; }
.sim-controls button:first-of-type { border-color: var(--green); color: var(--green); }
.sim-controls button:hover { border-color: var(--cyan); color: var(--cyan); }
.sim-note { color: var(--muted); margin: 0 0 18px; }
.sim-note code { color: var(--yellow); }
.sim-grid { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr); gap: 18px; margin-top: 18px; }
.sim-grid > * { min-width: 0; }
.sim-grid h3 { color: var(--text); font-size: 17px; margin: 0 0 10px; }
.interactive-steps { display: grid; gap: 10px; }
.interactive-step {
  background: rgba(16, 31, 52, 0.9);
  border: 1px solid var(--line);
  border-radius: 14px;
  cursor: pointer;
  display: grid;
  gap: 4px;
  grid-template-columns: 40px minmax(0, 1fr) minmax(80px, auto);
  padding: 12px;
}
.interactive-step.done { border-color: var(--green); background: rgba(60, 222, 151, 0.09); }
.interactive-step.active { border-color: var(--yellow); box-shadow: 0 0 0 2px rgba(255, 221, 90, 0.16); }
.interactive-step .idx { color: var(--orange); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight: 900; }
.interactive-step .name { font-weight: 800; min-width: 0; }
.interactive-step .pattern { color: var(--cyan); font-size: 12px; justify-self: end; max-width: 100%; overflow-wrap: anywhere; text-align: right; }
.interactive-step .mini { color: var(--muted); font-size: 13px; grid-column: 2 / 4; min-width: 0; }
.state-view,
.terminal-log,
.output-view {
  background: #050b14;
  border: 1px solid var(--line);
  border-radius: 14px;
  min-height: 260px;
  padding: 16px;
}
.state-view { color: var(--green); font-size: 13px; overflow: auto; }
.terminal-log { color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; overflow: auto; }
.terminal-log div { margin-bottom: 8px; }
.terminal-log .active-line { color: var(--yellow); }
.output-view { display: grid; gap: 12px; }
.output-headline { color: var(--text); font-size: 18px; font-weight: 900; }
.verdict {
  border: 1px solid var(--green);
  border-radius: 999px;
  color: var(--green);
  display: inline-block;
  font-size: 12px;
  font-weight: 900;
  padding: 4px 10px;
  width: max-content;
}
.verdict.warn { border-color: var(--yellow); color: var(--yellow); }
.output-cards { display: grid; gap: 10px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
.output-card { background: rgba(23, 43, 70, 0.72); border: 1px solid var(--line); border-radius: 12px; padding: 12px; }
.output-card strong { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; }
.output-card span { color: var(--text); font-weight: 800; }
@media (max-width: 860px) {
  .lab-hero, .two-col, .step-grid, .pattern-grid, .sim-grid, .output-cards { grid-template-columns: 1fr; }
  .section-heading { align-items: stretch; flex-direction: column; }
  .sim-controls { justify-content: stretch; }
  .sim-controls select, .sim-controls button { flex: 1 1 auto; }
  .interactive-step { grid-template-columns: 36px minmax(0, 1fr); }
  .interactive-step .pattern { grid-column: 2; justify-self: start; text-align: left; }
  .interactive-step .mini { grid-column: 2; }
  .lab-shell { padding: 28px 16px 48px; }
}
"""


INTERACTIVE_JS = """\
(function () {
  const dataNode = document.getElementById("demo-data");
  if (!dataNode) return;

  const demo = JSON.parse(dataNode.textContent);
  const scenarioSelect = document.getElementById("scenario-select");
  const runButton = document.getElementById("run-demo");
  const nextButton = document.getElementById("next-step");
  const resetButton = document.getElementById("reset-demo");
  const stepsNode = document.getElementById("interactive-steps");
  const stateNode = document.getElementById("state-view");
  const logNode = document.getElementById("terminal-log");
  const outputNode = document.getElementById("output-view");

  let scenarioIndex = 0;
  let stepIndex = -1;
  let timer = null;

  function scenario() {
    return demo.scenarios[scenarioIndex];
  }

  function currentStep() {
    return scenario().steps[Math.max(0, stepIndex)] || null;
  }

  function stopTimer() {
    if (timer) window.clearInterval(timer);
    timer = null;
  }

  function setStep(nextIndex) {
    stopTimer();
    const max = scenario().steps.length - 1;
    stepIndex = Math.max(-1, Math.min(nextIndex, max));
    render();
  }

  function renderScenarioOptions() {
    scenarioSelect.innerHTML = demo.scenarios.map((item, idx) => {
      return `<option value="${idx}">${item.label}</option>`;
    }).join("");
  }

  function renderSteps() {
    stepsNode.innerHTML = scenario().steps.map((step, idx) => {
      const classes = ["interactive-step"];
      if (idx < stepIndex) classes.push("done");
      if (idx === stepIndex) classes.push("active");
      return `<button class="${classes.join(" ")}" type="button" data-step="${idx}">
        <span class="idx">${String(idx + 1).padStart(2, "0")}</span>
        <span class="name">${step.name}</span>
        <span class="pattern">${step.pattern}</span>
        <span class="mini">${step.output}</span>
      </button>`;
    }).join("");
    stepsNode.querySelectorAll("[data-step]").forEach((node) => {
      node.addEventListener("click", () => setStep(Number(node.dataset.step)));
    });
  }

  function renderState() {
    if (stepIndex < 0) {
      stateNode.textContent = JSON.stringify({
        scenario: scenario().label,
        status: "ready",
        instruction: "Click Run Demo or Next Step."
      }, null, 2);
      return;
    }
    stateNode.textContent = JSON.stringify({
      scenario: scenario().label,
      step: currentStep().name,
      pattern: currentStep().pattern,
      state: currentStep().state
    }, null, 2);
  }

  function renderLog() {
    if (stepIndex < 0) {
      logNode.innerHTML = `<div class="active-line">$ ${demo.title}</div><div>${scenario().summary}</div>`;
      return;
    }
    const rows = scenario().steps.slice(0, stepIndex + 1).map((step, idx) => {
      const cls = idx === stepIndex ? "active-line" : "";
      return `<div class="${cls}">[${String(idx + 1).padStart(2, "0")}] ${step.log}</div>`;
    });
    logNode.innerHTML = rows.join("");
    logNode.scrollTop = logNode.scrollHeight;
  }

  function renderOutput() {
    const finalReached = stepIndex === scenario().steps.length - 1;
    if (stepIndex < 0) {
      outputNode.innerHTML = `<div class="output-headline">Ready to run</div><p>${scenario().summary}</p>`;
      return;
    }
    const step = currentStep();
    const final = scenario().final;
    const verdict = finalReached ? final.verdict : "RUNNING";
    const warn = /REVIEW|WARN|RUNNING/.test(verdict) ? " warn" : "";
    const cards = (finalReached ? final.cards : [
      ["Active step", step.name],
      ["Pattern", step.pattern],
      ["Output", step.output],
      ["Next", stepIndex + 1 < scenario().steps.length ? scenario().steps[stepIndex + 1].name : "final"]
    ]).map(([key, value]) => {
      return `<div class="output-card"><strong>${key}</strong><span>${value}</span></div>`;
    }).join("");
    outputNode.innerHTML = `
      <span class="verdict${warn}">${verdict}</span>
      <div class="output-headline">${finalReached ? final.headline : step.output}</div>
      <div class="output-cards">${cards}</div>
    `;
  }

  function render() {
    renderSteps();
    renderState();
    renderLog();
    renderOutput();
    nextButton.disabled = stepIndex >= scenario().steps.length - 1;
  }

  function runDemo() {
    stopTimer();
    stepIndex = -1;
    render();
    timer = window.setInterval(() => {
      if (stepIndex >= scenario().steps.length - 1) {
        stopTimer();
        return;
      }
      stepIndex += 1;
      render();
    }, 850);
  }

  scenarioSelect.addEventListener("change", () => {
    scenarioIndex = Number(scenarioSelect.value);
    stepIndex = -1;
    stopTimer();
    render();
  });
  runButton.addEventListener("click", runDemo);
  nextButton.addEventListener("click", () => setStep(stepIndex + 1));
  resetButton.addEventListener("click", () => setStep(-1));

  renderScenarioOptions();
  render();
})();
"""


def stage_html(index: int, stage: tuple[str, str, str, str, tuple[int, int, int]]) -> str:
    num, title, body, pattern, _color = stage
    return f"""<article class="step-card" data-step-index="{index}">
  <div class="step-number">{html.escape(num)}</div>
  <h3>{html.escape(title)}</h3>
  <p>{html.escape(body)}</p>
  <span class="chip">{html.escape(pattern)}</span>
</article>"""


def pattern_html(case: dict) -> str:
    controls = []
    for title, body in case["controls"]:
        controls.append(f"""<article class="pattern-card"><h3>{html.escape(title)}</h3><p>{html.escape(body)}</p></article>""")
    return "\n".join(controls)


def build_demo_payload(case_key: str) -> dict:
    demo = json.loads(json.dumps(DEMO_DATA[case_key]))
    if case_key == "workshop2":
        template = demo.pop("step_template")
        for scenario in demo["scenarios"]:
            signals = scenario["signals"]
            steps = []
            for idx, (name, pattern, log) in enumerate(template, start=1):
                if idx == 1:
                    state = {"ticket_quality": scenario["label"], "risk_hint": signals["risk"], "raw_input": "support ticket text"}
                    output = scenario["summary"]
                elif idx == 2:
                    state = {"structured_fields": ["title", "priority", "component", "environment", "steps"], "json_contract": True}
                    output = "Parser report emitted as JSON."
                elif idx == 3:
                    state = {"quality_score": signals["quality_score"], "missing_fields": [] if signals["quality_score"] > 80 else ["reproduction_steps", "environment", "expected_behavior"]}
                    output = f"Quality score: {signals['quality_score']}."
                elif idx == 4:
                    state = {"historical_matches": ["TICKET-1045"] if signals["duplicate"] else [], "duplicate_risk": signals["duplicate"]}
                    output = "Knowledge report attached historical evidence."
                elif idx == 5:
                    route = "human_review" if scenario["final"]["verdict"] != "APPROVED" else "auto_approved"
                    state = {"merged_score": signals["quality_score"], "duplicate": signals["duplicate"], "route": route}
                    output = f"Merge node selected route: {route}."
                else:
                    state = {"gate": scenario["final"]["verdict"], "risk_tier": signals["risk"], "review_required": scenario["final"]["verdict"] != "APPROVED"}
                    output = scenario["final"]["headline"]
                steps.append({"name": name, "pattern": pattern, "log": log, "state": state, "output": output})
            scenario["steps"] = steps
            scenario.pop("signals", None)
    return demo


def write_visual_page(case_key: str, case: dict):
    mapping = {
        "workshop1": ROOT / "workshops" / "workshop1-compliance" / "visual" / "index.html",
        "workshop2": ROOT / "workshops" / "workshop2-ticket-review" / "visual" / "index.html",
        "workshop3": ROOT / "workshops" / "workshop3-copilot-demo" / "visual" / "index.html",
    }
    out = mapping[case_key]
    out.parent.mkdir(parents=True, exist_ok=True)
    steps = "\n".join(stage_html(i, s) for i, s in enumerate(case["stages"]))
    pattern_chips = "".join(f'<span class="chip">{html.escape(p)}</span>' for p in case["patterns"])
    demo_payload = json.dumps(build_demo_payload(case_key), ensure_ascii=False, indent=2)
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(case["title"])} · Visual Walkthrough</title>
  <link rel="stylesheet" href="../../_visual/blueprint.css">
</head>
<body>
  <main class="lab-shell">
    <nav class="lab-nav">
      <a href="../../../README.md">LSEG Training Demos</a>
      <span>{html.escape(case["repo"])}</span>
    </nav>
    <section class="lab-hero">
      <div class="hero-copy">
        <div class="eyebrow">Visual workshop walkthrough</div>
        <h1>{html.escape(case["title"])}</h1>
        <p class="lede">{html.escape(case["subtitle"])}</p>
        <div class="chip-row">{pattern_chips}</div>
      </div>
      <aside class="hero-panel">
        <div class="metric"><strong>Run first</strong><span>Use the CLI path to produce concrete output.</span></div>
        <div class="metric"><strong>Observe state</strong><span>Look for intermediate objects, checks, scores, and routing reasons.</span></div>
        <div class="metric"><strong>Map patterns</strong><span>Use the chips as the first pattern-selection vocabulary.</span></div>
      </aside>
    </section>

    <section class="blueprint">
      <img src="../../../assets/visual/{html.escape(case["file"])}" alt="{html.escape(case["title"])} blueprint">
    </section>

    <section class="section simulator">
      <div class="section-heading">
        <div>
          <div class="eyebrow">Interactive pattern simulator</div>
          <h2>Run the architecture in the browser</h2>
        </div>
        <div class="sim-controls">
          <select id="scenario-select" aria-label="Scenario"></select>
          <button id="run-demo" type="button">Run Demo</button>
          <button id="next-step" type="button">Next Step</button>
          <button id="reset-demo" type="button">Reset</button>
        </div>
      </div>
      <p class="sim-note">This browser demo does not replace <code>python src/main.py</code>. It makes the same pipeline observable: each click updates state, output, quality gate, and pattern mapping.</p>
      <div class="sim-grid">
        <div>
          <h3>Live pipeline</h3>
          <div id="interactive-steps" class="interactive-steps"></div>
        </div>
        <div>
          <h3>State inspector</h3>
          <pre id="state-view" class="state-view"></pre>
        </div>
      </div>
      <div class="sim-grid">
        <div>
          <h3>Execution log</h3>
          <div id="terminal-log" class="terminal-log"></div>
        </div>
        <div>
          <h3>Current output</h3>
          <div id="output-view" class="output-view"></div>
        </div>
      </div>
    </section>

    <section class="section">
      <h2>Step-by-step architecture</h2>
      <div class="step-grid">
        {steps}
      </div>
    </section>

    <section class="section two-col">
      <div>
        <h2>Run</h2>
        <div class="run-panel"><pre>{html.escape(case["command"])}</pre></div>
      </div>
      <figure class="screenshot">
        <img src="{html.escape(case["screenshot"])}" alt="{html.escape(case["title"])} terminal screenshot">
        <figcaption>Terminal output is the concrete evidence; the blueprint explains why the architecture is shaped this way.</figcaption>
      </figure>
    </section>

    <section class="section">
      <h2>Control-plane reading</h2>
      <div class="pattern-grid">
        {pattern_html(case)}
      </div>
    </section>

    <section class="section">
      <h2>Design insight</h2>
      <p class="insight">{html.escape(case["insight"])}</p>
    </section>
  </main>
  <script id="demo-data" type="application/json">{demo_payload.replace("</", "<\\/")}</script>
  <script src="../../_visual/interactive.js"></script>
</body>
</html>
"""
    out.write_text(content, encoding="utf-8")


def write_css():
    WORKSHOP_VISUAL.mkdir(parents=True, exist_ok=True)
    (WORKSHOP_VISUAL / "blueprint.css").write_text(CSS, encoding="utf-8")
    (WORKSHOP_VISUAL / "interactive.js").write_text(INTERACTIVE_JS, encoding="utf-8")


def main():
    VISUAL_ASSETS.mkdir(parents=True, exist_ok=True)
    draw_ladder()
    for key, case in CASES.items():
        draw_case_blueprint(case)
        write_visual_page(key, case)
    for case in SHOWCASE_BLUEPRINTS.values():
        draw_case_blueprint(case)
    write_css()
    print(f"Built visual assets in {VISUAL_ASSETS}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build visual walkthrough pages and blueprint diagrams for the LSEG workshops."""
from __future__ import annotations

import html
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
@media (max-width: 860px) {
  .lab-hero, .two-col, .step-grid, .pattern-grid { grid-template-columns: 1fr; }
  .lab-shell { padding: 28px 16px 48px; }
}
"""


def stage_html(stage: tuple[str, str, str, str, tuple[int, int, int]]) -> str:
    num, title, body, pattern, _color = stage
    return f"""<article class="step-card">
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


def write_visual_page(case_key: str, case: dict):
    mapping = {
        "workshop1": ROOT / "workshops" / "workshop1-compliance" / "visual" / "index.html",
        "workshop2": ROOT / "workshops" / "workshop2-ticket-review" / "visual" / "index.html",
        "workshop3": ROOT / "workshops" / "workshop3-copilot-demo" / "visual" / "index.html",
    }
    out = mapping[case_key]
    out.parent.mkdir(parents=True, exist_ok=True)
    steps = "\n".join(stage_html(s) for s in case["stages"])
    pattern_chips = "".join(f'<span class="chip">{html.escape(p)}</span>' for p in case["patterns"])
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
</body>
</html>
"""
    out.write_text(content, encoding="utf-8")


def write_css():
    WORKSHOP_VISUAL.mkdir(parents=True, exist_ok=True)
    (WORKSHOP_VISUAL / "blueprint.css").write_text(CSS, encoding="utf-8")


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

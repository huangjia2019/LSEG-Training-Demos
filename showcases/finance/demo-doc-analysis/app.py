"""
MAS Document Analysis Pipeline — Demo
A Streamlit demo showing how an AI Agent pipeline transforms
regulatory document analysis for a compliance analyst (Sarah Chen).

5-step interactive pipeline:
1. Download & Read  →  2. Compare Versions  →  3. Extract Obligations
4. Map to Products  →  5. Generate Report
"""

import time
import streamlit as st
from mas_documents import SARAH_PROFILE, FAA_N16_CURRENT, FAA_N16_UPDATED, BANK_PRODUCTS
from pipeline_data import (
    STEP1_PARSE_RESULT,
    STEP2_DIFF_RESULT,
    STEP3_OBLIGATIONS,
    STEP4_PRODUCT_MAP,
    STEP5_REPORT,
)

# ── Page Config ──
st.set_page_config(
    page_title="MAS Doc Analysis Pipeline",
    page_icon="📄",
    layout="wide",
)

# ── Custom CSS ──
st.markdown("""
<style>
    .step-badge {
        display: inline-flex; align-items: center; justify-content: center;
        width: 38px; height: 38px; border-radius: 50%; font-weight: bold;
        font-size: 16px; margin: 0 auto;
    }
    .step-completed { background-color: #2f9e44; color: white; }
    .step-current { background-color: #1971c2; color: white; box-shadow: 0 0 0 3px #a5d8ff; }
    .step-locked { background-color: #dee2e6; color: #868e96; }
    .step-label { font-size: 11px; color: #495057; text-align: center; margin-top: 4px; }

    .diff-added { background-color: #d3f9d8; padding: 8px 12px; border-left: 4px solid #2f9e44;
                  border-radius: 4px; margin: 6px 0; }
    .diff-modified { background-color: #fff3bf; padding: 8px 12px; border-left: 4px solid #f08c00;
                     border-radius: 4px; margin: 6px 0; }
    .diff-removed { background-color: #ffe3e3; padding: 8px 12px; border-left: 4px solid #e03131;
                    border-radius: 4px; margin: 6px 0; }

    .severity-critical { color: #e03131; font-weight: bold; }
    .severity-high { color: #e8590c; font-weight: bold; }
    .severity-medium { color: #f08c00; font-weight: bold; }
    .severity-low { color: #2f9e44; font-weight: bold; }

    .impact-high { background-color: #ffe3e3; color: #c92a2a; padding: 4px 10px;
                   border-radius: 4px; font-weight: bold; font-size: 13px; }
    .impact-medium { background-color: #fff3bf; color: #e67700; padding: 4px 10px;
                     border-radius: 4px; font-weight: bold; font-size: 13px; }
    .impact-low { background-color: #d3f9d8; color: #2b8a3e; padding: 4px 10px;
                  border-radius: 4px; font-weight: bold; font-size: 13px; }
    .impact-none { background-color: #f1f3f5; color: #868e96; padding: 4px 10px;
                   border-radius: 4px; font-size: 13px; }

    .quote-box { background-color: #e8f0fe; padding: 16px; border-radius: 8px;
                 border-left: 4px solid #1971c2; font-style: italic; color: #1b3a5c;
                 margin: 12px 0; }
    .alert-box { background-color: #fff3bf; padding: 12px 16px; border-radius: 8px;
                 border-left: 4px solid #f08c00; margin: 8px 0; }
    .success-box { background-color: #d3f9d8; padding: 12px 16px; border-radius: 8px;
                   border-left: 4px solid #2f9e44; margin: 8px 0; }
    .metric-card { text-align: center; padding: 16px; border-radius: 8px;
                   background-color: #f8f9fa; border: 1px solid #dee2e6; }
    .section-text { font-family: 'Georgia', serif; font-size: 14px; line-height: 1.7;
                    color: #343a40; padding: 12px; background: #f8f9fa; border-radius: 6px; }

    .doc-panel { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px;
                 padding: 16px; max-height: 600px; overflow-y: auto; }
    .doc-panel-header { font-size: 13px; color: #868e96; font-weight: bold;
                        text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
    .doc-panel-section { font-family: 'Georgia', serif; font-size: 13px; line-height: 1.8;
                         color: #343a40; white-space: pre-wrap; }
    .doc-highlight { background-color: #fff3bf; border-left: 3px solid #f08c00;
                     padding: 2px 6px; border-radius: 3px; }
    .doc-highlight-new { background-color: #d3f9d8; border-left: 3px solid #2f9e44;
                         padding: 2px 6px; border-radius: 3px; }
    .doc-highlight-removed { background-color: #ffe3e3; border-left: 3px solid #e03131;
                             padding: 2px 6px; border-radius: 3px; }
    .ref-btn { cursor: pointer; }
    .doc-panel-empty { color: #adb5bd; text-align: center; padding: 40px 20px;
                       font-style: italic; }
</style>
""", unsafe_allow_html=True)

# ── Session State ──
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "step_completed" not in st.session_state:
    st.session_state.step_completed = {i: False for i in range(1, 6)}
if "step_processing" not in st.session_state:
    st.session_state.step_processing = {i: False for i in range(1, 6)}


if "selected_change" not in st.session_state:
    st.session_state.selected_change = None
if "selected_obligation" not in st.session_state:
    st.session_state.selected_obligation = None
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None


def _parse_section_ref(ref: str) -> list[str]:
    """Parse a section reference like '§4.4 / Annex B' into base section numbers ['4', 'Annex B']."""
    import re
    parts = [p.strip() for p in ref.replace("/", ",").split(",")]
    result = []
    for p in parts:
        p = p.lstrip("§").strip()
        if p.startswith("Annex"):
            result.append(p.split("§")[0].split(" §")[0].strip())
        else:
            m = re.match(r"(\d+)", p)
            if m:
                result.append(m.group(1))
    return result


def _find_sections(section_ref: str, doc=None):
    """Find document section(s) matching a section reference."""
    if doc is None:
        doc = FAA_N16_UPDATED
    keys = _parse_section_ref(section_ref)
    matches = []
    for sec in doc["sections"]:
        for k in keys:
            if sec["section_number"] == k:
                matches.append(sec)
    return matches


def _highlight_in_text(full_text: str, snippet: str, css_class: str = "doc-highlight") -> str:
    """Highlight a snippet within the full section text using HTML."""
    import html as html_mod
    safe_text = html_mod.escape(full_text)
    safe_snippet = html_mod.escape(snippet)
    if safe_snippet and safe_snippet in safe_text:
        highlighted = f'<span class="{css_class}">{safe_snippet}</span>'
        return safe_text.replace(safe_snippet, highlighted, 1)
    return safe_text


def render_doc_reference(section_ref: str, highlight_text: str = None,
                         css_class: str = "doc-highlight",
                         old_doc=False, label: str = None):
    """Render a document reference panel showing the source section with optional highlight."""
    doc = FAA_N16_CURRENT if old_doc else FAA_N16_UPDATED
    sections = _find_sections(section_ref, doc)
    version_tag = "v2024-01" if old_doc else "v2026-03 (Revised)"

    if not sections:
        st.markdown(f'<div class="doc-panel-empty">Section {section_ref} not found</div>',
                    unsafe_allow_html=True)
        return

    for sec in sections:
        if label:
            st.markdown(f'<div class="doc-panel-header">📄 {label}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="doc-panel-header">📄 §{sec["section_number"]} — '
                f'{sec["heading"]} ({version_tag})</div>',
                unsafe_allow_html=True)

        if highlight_text:
            rendered = _highlight_in_text(sec["text"], highlight_text, css_class)
        else:
            import html as html_mod
            rendered = html_mod.escape(sec["text"])

        st.markdown(
            f'<div class="doc-panel"><div class="doc-panel-section">{rendered}</div></div>',
            unsafe_allow_html=True)


def advance_to(step):
    st.session_state.current_step = step


def complete_step(step):
    st.session_state.step_completed[step] = True
    if step < 5:
        st.session_state.current_step = step + 1


def reset_pipeline():
    st.session_state.current_step = 0
    st.session_state.step_completed = {i: False for i in range(1, 6)}
    st.session_state.step_processing = {i: False for i in range(1, 6)}


# ── Sidebar: Demo Context Panel ──
with st.sidebar:
    st.title("📄 Doc Analysis Pipeline")
    st.caption("AI Agent Compliance Platform — Demo")
    st.divider()

    # ── MAS Document (the trigger) ──
    st.subheader("📜 MAS Document")
    st.markdown(f"**{FAA_N16_UPDATED['notice_number']}** (Revised)")
    st.markdown(f"_{FAA_N16_UPDATED['title']}_")
    st.markdown(f"Effective: {FAA_N16_UPDATED['effective_date']}")
    st.markdown(f"Pages: {FAA_N16_UPDATED['total_pages']} | "
                f"Sections: {len([sec for sec in FAA_N16_UPDATED['sections'] if not sec['section_number'].startswith('Annex')])} + "
                f"{len([sec for sec in FAA_N16_UPDATED['sections'] if sec['section_number'].startswith('Annex')])} annexes")
    st.link_button(
        "🔗 View on MAS website",
        "https://www.mas.gov.sg/regulation/notices/notice-faa-n16",
        use_container_width=True,
    )
    with st.expander("📖 Document sections"):
        for sec in FAA_N16_UPDATED["sections"]:
            is_new = sec["section_number"] in ("Annex B", "Annex C")
            new_tag = " 🆕" if is_new else ""
            st.caption(f"§{sec['section_number']} — {sec['heading']}{new_tag}")

    st.markdown(f"**Supersedes:** {FAA_N16_CURRENT['notice_number']} "
                f"(v{FAA_N16_CURRENT['version']}, {FAA_N16_CURRENT['effective_date']})")
    st.divider()

    # ── Bank Product Portfolio ──
    st.subheader("🏦 Bank Products")
    st.caption("Horizon Bank Singapore — Product Portfolio")
    for prod in BANK_PRODUCTS:
        risk_icon = {"Low": "🟢", "Medium": "🟡", "Medium-High": "🟠", "High": "🔴"}.get(prod["risk_level"], "⚪")
        with st.expander(f"{risk_icon} {prod['name']}"):
            st.markdown(f"**Type:** {prod['type']}")
            st.markdown(f"**Department:** {prod['department']}")
            st.markdown(f"**Risk Level:** {prod['risk_level']}")
            st.markdown(f"**Status:** {prod['current_status']}")
            st.markdown(f"**Revenue:** {prod['annual_revenue']}")
            st.caption(prod["description"])
    st.divider()

    # ── Analyst Profile ──
    st.subheader("👩‍💼 Analyst")
    st.markdown(f"**{SARAH_PROFILE['name']}** — {SARAH_PROFILE['title']}")
    st.markdown(f"{SARAH_PROFILE['department']}")
    st.caption(f"{SARAH_PROFILE['bank']} | {SARAH_PROFILE['experience']}")
    st.divider()

    # ── Pipeline Progress ──
    st.subheader("⚙️ Pipeline Progress")
    step_names = ["Download & Read", "Compare Versions", "Extract Obligations",
                  "Map to Products", "Generate Report"]
    for i, name in enumerate(step_names, 1):
        if st.session_state.step_completed.get(i):
            st.markdown(f"✅ Step {i}: {name}")
        elif st.session_state.current_step == i:
            st.markdown(f"🔵 Step {i}: **{name}** ← current")
        else:
            st.markdown(f"⬜ Step {i}: {name}")

    if st.session_state.current_step > 0:
        completed = sum(1 for v in st.session_state.step_completed.values() if v)
        st.progress(completed / 5, text=f"{completed}/5 steps completed")

    st.divider()
    if st.button("🔄 Reset Pipeline", use_container_width=True):
        reset_pipeline()
        st.rerun()



# ── Step Indicator Bar ──
def render_step_indicator():
    step_names = ["Download\n& Read", "Compare\nVersions", "Extract\nObligations",
                  "Map to\nProducts", "Generate\nReport"]
    cols = st.columns(5)
    for i, (col, name) in enumerate(zip(cols, step_names), 1):
        with col:
            if st.session_state.step_completed.get(i):
                cls = "step-completed"
                icon = "✓"
            elif st.session_state.current_step == i:
                cls = "step-current"
                icon = str(i)
            else:
                cls = "step-locked"
                icon = str(i)
            st.markdown(
                f'<div style="text-align:center">'
                f'<div class="step-badge {cls}">{icon}</div>'
                f'<div class="step-label">{name}</div></div>',
                unsafe_allow_html=True
            )


# ── Main Content ──
st.title("📄 MAS Regulatory Document Analysis")
st.markdown(
    "Demonstrating how an AI Agent pipeline transforms **regulatory document analysis** "
    "from a 3-day manual process into a 50-minute review workflow."
)

render_step_indicator()
st.divider()

# ═══════════════════════════════════════════
# LANDING — Before pipeline starts
# ═══════════════════════════════════════════

if st.session_state.current_step == 0:
    st.header("Sarah's Challenge")
    st.markdown(
        f'<div class="quote-box" style="font-size:16px">'
        f'"{SARAH_PROFILE["trigger"]}"</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current Manual Process")
        manual_steps = [
            ("1. Download & Read", "4-6 hours", "Read all 47 pages of dense legal text"),
            ("2. Compare Versions", "3-4 hours", "Side-by-side PDF comparison"),
            ("3. Extract Obligations", "2-3 hours", "Find shall/must/required clauses"),
            ("4. Map to Products", "4-6 hours", "Email dept heads, wait for replies"),
            ("5. Write Report", "3-4 hours", "Compile impact assessment"),
        ]
        for name, time_est, desc in manual_steps:
            st.markdown(f"**{name}** — _{time_est}_")
            st.caption(desc)
        st.markdown("---")
        st.markdown("**Total: 16-23 hours (2-3 days)**")
        st.error("Risk: ~40% probability of missing clauses in annexes")

    with col2:
        st.subheader("With AI Agent Pipeline")
        ai_steps = [
            ("1. Download & Read", "0 min", "Auto-detected and parsed over weekend"),
            ("2. Compare Versions", "5 min review", "Semantic clause-level diff"),
            ("3. Extract Obligations", "10 min review", "NER + LLM extraction, 93%+ accuracy"),
            ("4. Map to Products", "15 min review", "Knowledge graph auto-mapping"),
            ("5. Generate Report", "20 min editing", "Draft with full citations"),
        ]
        for name, time_est, desc in ai_steps:
            st.markdown(f"**{name}** — _{time_est}_")
            st.caption(desc)
        st.markdown("---")
        st.markdown("**Total: 50 minutes**")
        st.success(">93% recall — near-zero miss rate")

    st.markdown("")
    if st.button("▶️ Start Pipeline Demo", type="primary", use_container_width=True):
        advance_to(1)
        st.rerun()

# ═══════════════════════════════════════════
# STEP 1: Download & Read
# ═══════════════════════════════════════════

elif st.session_state.current_step == 1:
    st.header("Step 1: Download & Read — Document Ingestion Agent")

    with st.spinner("🌐 Agent is monitoring MAS website... detecting new publication..."):
        time.sleep(2.0)
    with st.spinner("📥 Downloading MAS Notice FAA-N16 (Revised)..."):
        time.sleep(1.5)
    with st.spinner("🔍 Parsing document structure..."):
        time.sleep(2.0)

    st.success("Document ingested and parsed successfully!")

    # Metadata
    r = STEP1_PARSE_RESULT
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pages", r["total_pages"])
    col2.metric("Sections", f'{r["total_sections"]} + {r["total_annexes"]} annexes')
    col3.metric("Clauses Detected", r["total_clauses"])
    col4.metric("Word Count", f'{r["word_count"]:,}')

    st.markdown("#### Document Metadata")
    meta_cols = st.columns(2)
    with meta_cols[0]:
        st.markdown(f"**Notice:** {r['notice_number']} — {r['title']}")
        st.markdown(f"**Issuing Authority:** {r['issuing_authority']}")
        st.markdown(f"**Effective Date:** {r['effective_date']}")
        st.markdown(f"**Supersedes:** {r['supersedes']}")
    with meta_cols[1]:
        st.markdown(f"**Detected:** {r['detected_at']}")
        st.markdown(f"**Format:** {r['format']}, {r['total_pages']} pages")
        st.markdown(f"**Tables:** {r['total_tables']} | **Figures:** {r['total_figures']}")
        st.markdown(f"**Applicability:** {r['applicability']}")

    st.markdown("#### Parsed Document Structure")
    for sec in r["sections_summary"]:
        with st.expander(f"§{sec['number']} — {sec['heading']}  ({sec['clauses']} clauses, pp. {sec['pages']})"):
            # Show actual text from the new document
            matching = [s for s in FAA_N16_UPDATED["sections"]
                        if s["section_number"] == sec["number"]]
            if matching:
                st.markdown(f'<div class="section-text">{matching[0]["text"]}</div>',
                            unsafe_allow_html=True)
            else:
                st.caption("(Section content available in full document)")

    st.markdown("")
    st.markdown(
        '<div class="success-box"><strong>Sarah\'s time: 0 minutes</strong> — '
        'the document was detected and parsed over the weekend. '
        'She sees this when she logs in Monday morning.</div>',
        unsafe_allow_html=True
    )

    st.markdown("")
    if st.button("✅ Mark as Reviewed → Proceed to Step 2", type="primary", use_container_width=True):
        complete_step(1)
        st.rerun()

# ═══════════════════════════════════════════
# STEP 2: Compare Versions
# ═══════════════════════════════════════════

elif st.session_state.current_step == 2:
    st.header("Step 2: Compare — Version Comparison Agent")

    with st.spinner("📊 Retrieving previous version from knowledge base..."):
        time.sleep(1.5)
    with st.spinner("🔍 Performing clause-level semantic comparison..."):
        time.sleep(3.0)

    st.success("Version comparison complete!")

    diff = STEP2_DIFF_RESULT
    s = diff["summary"]

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🟢 Added", s["added"], help="New clauses/sections")
    col2.metric("🟡 Modified", s["modified"], help="Changed clauses")
    col3.metric("🔴 Removed", s["removed"], help="Deleted clauses")
    col4.metric("⚪ Unchanged", s["unchanged"], help="No substantive change")

    st.markdown(f"**Comparing:** {diff['old_version']} → {diff['new_version']}")

    # Filter
    change_filter = st.multiselect(
        "Filter by change type:",
        ["ADDED", "MODIFIED", "REMOVED"],
        default=["ADDED", "MODIFIED", "REMOVED"],
    )

    # ── Two-column layout: changes list (left) + document reference (right) ──
    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.markdown("#### Changes Detected")
        st.caption("Click any change to view its source in the document →")
        for idx, change in enumerate(diff["changes"]):
            if change["change_type"] not in change_filter:
                continue

            ct = change["change_type"]
            css_class = {"ADDED": "diff-added", "MODIFIED": "diff-modified", "REMOVED": "diff-removed"}.get(ct, "")
            sig_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(change["significance"], "")

            is_selected = st.session_state.selected_change == idx
            label = (f"{'🟢' if ct == 'ADDED' else '🟡' if ct == 'MODIFIED' else '🔴'} "
                     f"{ct} — {change['section']} {change['heading']}  "
                     f"[{sig_icon} {change['significance']}]"
                     f"{'  ◀' if is_selected else ''}")

            with st.expander(label, expanded=is_selected):
                st.markdown(f'<div class="{css_class}"><strong>AI Summary:</strong> {change["ai_summary"]}</div>',
                            unsafe_allow_html=True)

                if ct == "MODIFIED":
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Previous version:**")
                        st.code(change["old_text"], language=None)
                    with c2:
                        st.markdown("**New version:**")
                        st.code(change["new_text"], language=None)
                elif ct == "ADDED":
                    st.markdown("**New text:**")
                    st.code(change["new_text"], language=None)

                if st.button("📄 Locate in Document", key=f"ref_change_{idx}"):
                    st.session_state.selected_change = idx
                    st.rerun()

        # Removed items
        if "REMOVED" in change_filter and diff.get("removed_items"):
            for item in diff["removed_items"]:
                st.markdown(
                    f'<div class="diff-removed"><strong>REMOVED:</strong> {item["description"]}<br>'
                    f'<em>{item["ai_summary"]}</em></div>',
                    unsafe_allow_html=True
                )

    with right_col:
        st.markdown("#### 📄 Document Reference")
        sel = st.session_state.selected_change
        if sel is not None and 0 <= sel < len(diff["changes"]):
            change = diff["changes"][sel]
            ct = change["change_type"]

            if ct == "MODIFIED":
                # Show old version with removed text, then new version with added text
                st.markdown("**Old Version (v2024-01):**")
                render_doc_reference(
                    change["section"],
                    highlight_text=change["old_text"],
                    css_class="doc-highlight-removed",
                    old_doc=True,
                    label=f"§{change['section']} — {change['heading']} (v2024-01)"
                )
                st.markdown("")
                st.markdown("**New Version (v2026-03):**")
                render_doc_reference(
                    change["section"],
                    highlight_text=change["new_text"],
                    css_class="doc-highlight-new",
                    label=f"§{change['section']} — {change['heading']} (v2026-03)"
                )
            elif ct == "ADDED":
                render_doc_reference(
                    change["section"],
                    highlight_text=change["new_text"],
                    css_class="doc-highlight-new",
                )
            else:
                render_doc_reference(change["section"])
        else:
            st.markdown(
                '<div class="doc-panel"><div class="doc-panel-empty">'
                '← Click "Locate in Document" on any change to view the source section here'
                '</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("")
    st.markdown(
        '<div class="success-box"><strong>Sarah\'s time: 5 minutes</strong> — '
        'review the change summary. The semantic diff handled section restructuring automatically.</div>',
        unsafe_allow_html=True
    )

    st.markdown("")
    if st.button("✅ Mark as Reviewed → Proceed to Step 3", type="primary", use_container_width=True):
        complete_step(2)
        st.rerun()

# ═══════════════════════════════════════════
# STEP 3: Extract Obligations
# ═══════════════════════════════════════════

elif st.session_state.current_step == 3:
    st.header("Step 3: Extract — Obligation Extraction Agent")

    with st.spinner("🔍 Scanning all clauses for mandatory language (shall/must/required)..."):
        time.sleep(2.5)
    with st.spinner("🏷️ Classifying and categorizing obligations..."):
        time.sleep(2.0)

    obligations = STEP3_OBLIGATIONS
    new_count = sum(1 for o in obligations if o["is_new"])
    critical_count = sum(1 for o in obligations if o["severity"] == "CRITICAL")

    st.success(f"Extracted {len(obligations)} obligations — {new_count} new, {critical_count} critical")

    # Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total", len(obligations))
    col2.metric("🆕 New", new_count)
    col3.metric("🔴 Critical", critical_count)
    col4.metric("🟠 High", sum(1 for o in obligations if o["severity"] == "HIGH"))
    col5.metric("🟡 Medium", sum(1 for o in obligations if o["severity"] == "MEDIUM"))

    # Filters
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        cat_filter = st.multiselect(
            "Filter by category:",
            sorted(set(o["category"] for o in obligations)),
            default=sorted(set(o["category"] for o in obligations)),
        )
    with fcol2:
        sev_filter = st.multiselect(
            "Filter by severity:",
            ["CRITICAL", "HIGH", "MEDIUM"],
            default=["CRITICAL", "HIGH", "MEDIUM"],
        )
    with fcol3:
        new_only = st.checkbox("Show only NEW/changed obligations")

    # ── Two-column layout: obligations list (left) + document reference (right) ──
    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.markdown("#### Extracted Obligations")
        st.caption("Click any obligation to view its source in the document →")
        for o in obligations:
            if o["category"] not in cat_filter:
                continue
            if o["severity"] not in sev_filter:
                continue
            if new_only and not o["is_new"] and "change_note" not in o:
                continue

            sev_cls = f"severity-{o['severity'].lower()}"
            new_badge = ' <span style="background:#d3f9d8;color:#2b8a3e;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:bold">NEW</span>' if o["is_new"] else ""
            changed_badge = f' <span style="background:#fff3bf;color:#e67700;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:bold">CHANGED</span>' if "change_note" in o and not o["is_new"] else ""
            selected_marker = " ◀" if st.session_state.selected_obligation == o["id"] else ""

            with st.container():
                st.markdown(
                    f'**#{o["id"]}** | {o["section_ref"]} | '
                    f'<span class="{sev_cls}">{o["severity"]}</span> | '
                    f'`{o["category"]}` | `{o["obligation_type"]}`{new_badge}{changed_badge}{selected_marker}',
                    unsafe_allow_html=True
                )

                # Highlight keywords in text
                text = o["text"]
                for kw in ["shall", "must", "required", "shall not"]:
                    text = text.replace(kw, f"**{kw}**")
                st.markdown(f"> {text}")

                if "change_note" in o:
                    st.caption(f"📝 Change: {o['change_note']}")

                if st.button("📄 Locate in Document", key=f"ref_obl_{o['id']}"):
                    st.session_state.selected_obligation = o["id"]
                    st.rerun()

                st.markdown("---")

    with right_col:
        st.markdown("#### 📄 Document Reference")
        sel_obl_id = st.session_state.selected_obligation
        sel_obl = next((o for o in obligations if o["id"] == sel_obl_id), None) if sel_obl_id else None
        if sel_obl:
            render_doc_reference(
                sel_obl["section_ref"],
                highlight_text=sel_obl["text"],
                css_class="doc-highlight",
            )
            if "change_note" in sel_obl:
                st.markdown("")
                st.info(f"📝 **Change:** {sel_obl['change_note']}")
        else:
            st.markdown(
                '<div class="doc-panel"><div class="doc-panel-empty">'
                '← Click "Locate in Document" on any obligation to view the source section here'
                '</div></div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="alert-box"><strong>Accuracy:</strong> 93%+ precision, 94%+ recall '
        '(benchmarked against legal expert annotations). '
        'Not just keyword matching — understands context.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="success-box"><strong>Sarah\'s time: 10 minutes</strong> — '
        'review and validate the extracted obligations. She can edit any item.</div>',
        unsafe_allow_html=True
    )

    st.markdown("")
    if st.button("✅ Mark as Reviewed → Proceed to Step 4", type="primary", use_container_width=True):
        complete_step(3)
        st.rerun()

# ═══════════════════════════════════════════
# STEP 4: Map to Products
# ═══════════════════════════════════════════

elif st.session_state.current_step == 4:
    st.header("Step 4: Map — Impact Mapping Agent")

    with st.spinner("🗂️ Loading bank product portfolio..."):
        time.sleep(1.5)
    with st.spinner("🔗 Mapping obligations to products via knowledge graph..."):
        time.sleep(3.0)

    st.success("Impact mapping complete!")

    # Impact overview
    st.markdown("#### Impact Summary")
    overview_cols = st.columns(len(STEP4_PRODUCT_MAP))
    for col, pm in zip(overview_cols, STEP4_PRODUCT_MAP):
        with col:
            impact_cls = f"impact-{pm['impact_level'].lower()}"
            st.markdown(
                f'<div class="metric-card">'
                f'<strong>{pm["product"]}</strong><br><br>'
                f'<span class="{impact_cls}">{pm["impact_level"]} IMPACT</span><br><br>'
                f'{len(pm["applicable_obligations"])} obligations apply'
                f'</div>',
                unsafe_allow_html=True
            )

    # ── Two-column layout: product details (left) + document reference (right) ──
    left_col, right_col = st.columns([3, 2])

    obligations = STEP3_OBLIGATIONS

    with left_col:
        st.markdown("#### Product Detail")
        st.caption("Click any product to view its key regulatory references →")

        for pidx, pm in enumerate(STEP4_PRODUCT_MAP):
            is_selected = st.session_state.selected_product == pidx
            impact_cls = f"impact-{pm['impact_level'].lower()}"
            with st.expander(
                f"{'🔴' if pm['impact_level'] == 'HIGH' else '🟡' if pm['impact_level'] == 'MEDIUM' else '🟢'} "
                f"{pm['product']} — {pm['impact_level']} IMPACT"
                f"{'  ◀' if is_selected else ''}",
                expanded=is_selected or pm["impact_level"] == "HIGH",
            ):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Key Changes Affecting This Product:**")
                    for change in pm["key_changes"]:
                        st.markdown(f"- {change}")

                    st.markdown("**Affected Departments:**")
                    st.markdown(", ".join(pm["affected_departments"]))

                with c2:
                    st.markdown("**Compliance Gaps Identified:**")
                    for gap in pm["gaps"]:
                        st.markdown(f"- ⚠️ {gap}")

                    st.markdown(f"**Compliance Deadline:** {pm['deadline']}")

                # Show applicable obligation IDs
                obl_ids = pm["applicable_obligations"]
                st.caption(f"Applicable obligations: {', '.join(f'#{oid}' for oid in obl_ids)}")

                if st.button("📄 View Regulatory Sources", key=f"ref_prod_{pidx}"):
                    st.session_state.selected_product = pidx
                    st.rerun()

    with right_col:
        st.markdown("#### 📄 Reference Panel")
        sel_pidx = st.session_state.selected_product
        if sel_pidx is not None and 0 <= sel_pidx < len(STEP4_PRODUCT_MAP):
            pm = STEP4_PRODUCT_MAP[sel_pidx]

            # ── Product Metadata / Profile ──
            # Find the matching BANK_PRODUCTS entry
            bank_prod = next((p for p in BANK_PRODUCTS if p["name"] == pm["product"]), None)
            if bank_prod and "regulatory_profile" in bank_prod:
                rp = bank_prod["regulatory_profile"]
                st.markdown(f"##### 🏦 Product Profile")
                st.markdown(
                    f'<div class="doc-panel">'
                    f'<div class="doc-panel-header">Product Metadata — {bank_prod["name"]}</div>'
                    f'<strong>Classification:</strong> {rp["product_classification"]}<br>'
                    f'<strong>MAS Code:</strong> {rp["mas_product_code"]}<br>'
                    f'<strong>Risk Level:</strong> {bank_prod["risk_level"]}<br>'
                    f'<strong>Status:</strong> {bank_prod["current_status"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Prospectus excerpt
                with st.expander("📋 Product Description (from prospectus)"):
                    st.markdown(f'<div class="section-text">{rp["prospectus_excerpt"]}</div>',
                                unsafe_allow_html=True)

                # Risk features
                with st.expander("⚠️ Risk Features"):
                    for feat in rp["risk_features"]:
                        st.markdown(f"- {feat}")

                # Regulatory triggers — WHY this product is affected
                with st.expander("🔗 Why This Product Is Affected", expanded=True):
                    for trigger in rp["regulatory_triggers"]:
                        st.markdown(f"- {trigger}")

                # Current documents
                with st.expander("📁 Current Compliance Documents"):
                    for doc_name in rp["current_documents"]:
                        st.markdown(f"- 📄 {doc_name}")

            st.markdown("")

            # ── Regulatory Document References ──
            st.markdown(f"##### 📜 Regulatory Source Sections")
            shown_sections = set()
            for oid in pm["applicable_obligations"]:
                obl = next((o for o in obligations if o["id"] == oid), None)
                if obl:
                    base_keys = tuple(_parse_section_ref(obl["section_ref"]))
                    if base_keys not in shown_sections:
                        shown_sections.add(base_keys)
                        css = "doc-highlight-new" if obl["is_new"] else "doc-highlight"
                        render_doc_reference(
                            obl["section_ref"],
                            highlight_text=obl["text"],
                            css_class=css,
                        )
                        if obl["is_new"]:
                            st.caption(f"🆕 New obligation #{obl['id']}")
                        elif "change_note" in obl:
                            st.caption(f"📝 Changed: {obl['change_note']}")
                        st.markdown("")
                    if len(shown_sections) >= 4:
                        remaining = len(pm["applicable_obligations"]) - sum(
                            1 for oid2 in pm["applicable_obligations"]
                            if tuple(_parse_section_ref(
                                next((o for o in obligations if o["id"] == oid2),
                                     {"section_ref": ""})["section_ref"]
                            )) in shown_sections
                        )
                        if remaining > 0:
                            st.caption(f"... and {remaining} more obligations from other sections")
                        break
        else:
            st.markdown(
                '<div class="doc-panel"><div class="doc-panel-empty">'
                '← Click "View Regulatory Sources" on any product to see product profile '
                'and relevant regulatory sections here'
                '</div></div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="success-box"><strong>Sarah\'s time: 15 minutes</strong> — '
        'review mappings and adjust where her institutional knowledge adds nuance.</div>',
        unsafe_allow_html=True
    )

    st.markdown("")
    if st.button("✅ Mark as Reviewed → Proceed to Step 5", type="primary", use_container_width=True):
        complete_step(4)
        st.rerun()

# ═══════════════════════════════════════════
# STEP 5: Generate Report
# ═══════════════════════════════════════════

elif st.session_state.current_step == 5:
    st.header("Step 5: Report — Impact Assessment Generator")

    with st.spinner("📝 Generating impact assessment report with citations..."):
        time.sleep(3.0)

    report = STEP5_REPORT

    st.success("Impact assessment report generated!")

    # Executive Summary
    st.markdown("### Executive Summary")
    st.markdown(
        f'<div class="quote-box" style="font-style:normal">{report["executive_summary"]}</div>',
        unsafe_allow_html=True
    )

    # Compliance Readiness
    st.markdown("### Compliance Readiness Score")
    score = report["compliance_readiness_score"]
    score_color = "🔴" if score < 50 else "🟡" if score < 75 else "🟢"
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric(f"{score_color} Score", f"{score}/100")
    with col2:
        st.progress(score / 100, text=f"Current readiness: {score}% — action required to reach full compliance by 1 Oct 2026")

    # Risk Matrix
    st.markdown("### Risk Heat Map by Product")
    risk_data = []
    for rm in report["risk_matrix"]:
        row = [rm["product"]]
        for key in ["suitability", "disclosure", "training", "record_keeping", "overall"]:
            val = rm[key]
            row.append(val)
        risk_data.append(row)

    # Render as colored table
    header = "| Product | Suitability | Disclosure | Training | Records | Overall |\n|---|---|---|---|---|---|\n"
    rows = ""
    for row in risk_data:
        cells = [row[0]]
        for val in row[1:]:
            cells.append(f"**{val}**" if val in ["HIGH", "CRITICAL"] else val)
        rows += "| " + " | ".join(cells) + " |\n"
    st.markdown(header + rows)

    # Action Items
    st.markdown("### Priority Action Items")
    for item in report["action_items"]:
        priority_icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}.get(item["priority"], "⚪")
        with st.container():
            cols = st.columns([0.5, 3, 1.5, 1, 1])
            cols[0].markdown(f"**{priority_icon} {item['priority']}**")
            cols[1].markdown(item["action"])
            cols[2].markdown(f"_{item['owner']}_")
            cols[3].markdown(item["deadline"])
            cols[4].markdown(item["cost_estimate"])
        st.markdown("---")

    st.markdown(f"**Total Estimated Cost:** {report['total_cost_estimate']}")

    # Next Steps
    st.markdown("### Recommended Next Steps")
    for i, step in enumerate(report["next_steps"], 1):
        st.markdown(f"**{i}.** {step}")

    # Download button
    report_text = f"""# {report['title']}
**Bank:** {report['bank']}
**Prepared by:** {report['prepared_by']}
**Date:** {report['date']}

## Executive Summary
{report['executive_summary']}

## Compliance Readiness Score: {score}/100

## Action Items
"""
    for item in report["action_items"]:
        report_text += f"- [{item['priority']}] {item['action']} — Owner: {item['owner']} — Deadline: {item['deadline']}\n"

    report_text += f"\n## Total Estimated Cost: {report['total_cost_estimate']}\n"

    st.download_button(
        "📥 Download Report (Markdown)",
        report_text,
        file_name="FAA-N16_Impact_Assessment_2026.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown(
        '<div class="success-box"><strong>Sarah\'s time: 20 minutes</strong> — '
        'review the report, edit key sections, and submit to management. '
        'Every claim is cited to a specific clause.</div>',
        unsafe_allow_html=True
    )

    st.markdown("")
    complete_step(5)

    st.balloons()

    # Final summary
    st.markdown("---")
    st.markdown("### Pipeline Complete!")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Manual process:** 16-23 hours (2-3 days)")
        st.markdown("**AI pipeline:** 50 minutes")
        st.markdown("**Speed improvement:** 10x faster")
    with col2:
        st.markdown("**Manual miss rate:** ~40% in annexes")
        st.markdown("**AI recall:** >93%")
        st.markdown("**Report quality:** Fully cited, audit-ready")

    st.markdown(
        '<div class="quote-box" style="text-align:center;font-size:18px;font-style:normal">'
        '<strong>Sarah submits Monday afternoon. Not Wednesday.</strong><br>'
        'The AI does the processing. Sarah does the thinking.</div>',
        unsafe_allow_html=True
    )

    if st.button("🔄 Run Pipeline Again", use_container_width=True):
        reset_pipeline()
        st.rerun()

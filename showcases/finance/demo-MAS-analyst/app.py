"""
MAS Compliance Analyst Agent - Demo V1
A simple Streamlit demo showing how an AI Agent can assist
compliance analysts at Singapore banks regulated by MAS.
"""

import time
import streamlit as st
from mas_knowledge import (
    MAS_REGULATIONS,
    ANALYST_TASKS,
    DEMO_SCENARIO,
    MAS_SEARCH_RESULTS,
    PRODUCT_COMPLIANCE_MAP,
)

# --- Page Config ---
st.set_page_config(
    page_title="MAS Compliance Agent",
    page_icon="🏛️",
    layout="wide",
)

# --- Custom CSS ---
st.markdown(
    """
<style>
    .severity-critical { color: #ff0000; font-weight: bold; }
    .severity-high { color: #ff4500; font-weight: bold; }
    .severity-medium { color: #ff8c00; font-weight: bold; }
    .verdict-blocked { background-color: #ffcccc; padding: 10px; border-radius: 5px; border-left: 4px solid #ff0000; }
    .verdict-warning { background-color: #fff3cd; padding: 10px; border-radius: 5px; border-left: 4px solid #ff8c00; }
    .verdict-pass { background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 4px solid #28a745; }
    .step-box { background-color: #f0f2f6; padding: 15px; border-radius: 8px; margin: 10px 0; }
    .metric-card { text-align: center; padding: 15px; border-radius: 8px; }
</style>
""",
    unsafe_allow_html=True,
)

# --- Sidebar ---
with st.sidebar:
    st.title("🏛️ MAS Compliance Agent")
    st.caption("V1 Demo — AI-Powered Regulatory Compliance")
    st.divider()

    st.subheader("🏦 Bank Profile")
    st.markdown(f"**{DEMO_SCENARIO['bank_name']}**")
    st.markdown(DEMO_SCENARIO["description"])
    st.divider()

    st.subheader("📦 Products")
    for p in DEMO_SCENARIO["products"]:
        risk_color = {"Low": "🟢", "Medium-High": "🟡", "High": "🔴"}
        color = risk_color.get(p["risk_level"], "⚪")
        st.markdown(f"{color} **{p['name']}**")
        st.caption(f"{p['type']} | Risk: {p['risk_level']}")

    st.divider()
    st.caption("Built for A*Star RegTech Demo")
    st.caption("Powered by AI Agent Architecture")

# --- Main Content ---
st.title("🤖 MAS Compliance Analyst Agent")
st.markdown(
    "Demonstrating how an AI Agent can automate the work of a **Regulatory Compliance Manager** "
    "at a Singapore bank, based on [MAS regulations](https://www.mas.gov.sg/regulation)."
)

# --- Tab Layout ---
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📋 Pipeline Demo",
        "🔍 Compliance Check",
        "📊 Analyst Tasks",
        "📖 Knowledge Base",
    ]
)

# =============================================
# TAB 1: Pipeline Demo
# =============================================
with tab1:
    st.header("Agent Pipeline: Product Compliance Analysis")
    st.markdown(
        "Select a banking product below, then click **Run Pipeline** to see the agent "
        "retrieve relevant MAS regulations, generate compliance guidelines, assess business impact, and flag specific risks."
    )

    # Product selection
    product_options = list(PRODUCT_COMPLIANCE_MAP.keys())
    selected_pipeline_product = st.selectbox(
        "🏦 Select a Banking Product / Business Scenario",
        product_options,
        key="pipeline_product",
    )
    product_data = PRODUCT_COMPLIANCE_MAP[selected_pipeline_product]
    st.caption(product_data["description"])

    if st.button("▶️ Run Pipeline", type="primary", key="run_pipeline"):
        regs = product_data["relevant_regulations"]
        guidelines = product_data["compliance_guidelines"]
        impacts = product_data["business_impact"]
        risks = product_data["risk_warnings"]

        # Step 1: Search MAS regulations for this product
        st.subheader(f"Step 1: 🌐 Searching MAS Regulations for「{selected_pipeline_product}」")
        with st.spinner("Agent is searching MAS website for relevant regulations..."):
            time.sleep(3.5)

        st.success(f"Found {len(regs)} directly relevant MAS regulations")
        for reg in regs:
            with st.expander(f"📜 **{reg['id']}** — {reg['title']}", expanded=True):
                st.markdown(f"**Why this matters for {selected_pipeline_product}:**")
                st.markdown(f"> {reg['relevance']}")
                st.markdown(f"🔗 [View on MAS website]({reg['url']})")

        st.divider()

        # Step 2: Generate Compliance Guidelines
        st.subheader("Step 2: 📋 Generating Product-Specific Compliance Guidelines")
        with st.spinner("Agent is analyzing regulations and generating compliance checklist..."):
            time.sleep(4.0)

        st.success(f"Generated {len(guidelines)} compliance requirements for this product")
        st.markdown("**Your team must follow these steps before/during each sale:**")
        for i, guideline in enumerate(guidelines, 1):
            st.markdown(f"**{i}.** {guideline}")

        st.divider()

        # Step 3: Business Impact Assessment
        st.subheader("Step 3: 💼 Assessing Business Impact")
        with st.spinner("Agent is evaluating how these regulations affect your business operations..."):
            time.sleep(3.5)

        st.success("Business impact assessment complete")
        st.markdown("**How these regulations affect your day-to-day operations:**")
        for impact in impacts:
            st.markdown(f"- {impact}")

        st.divider()

        # Step 4: Risk Warnings
        st.subheader("Step 4: ⚠️ Specific Risk Warnings & Red Flags")
        with st.spinner("Agent is identifying high-risk scenarios and common violations..."):
            time.sleep(4.0)

        critical_count = sum(1 for r in risks if "CRITICAL" in r)
        high_count = sum(1 for r in risks if "HIGH" in r)
        medium_count = sum(1 for r in risks if "MEDIUM" in r)

        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 Critical / High", critical_count + high_count)
        col2.metric("🟡 Medium", medium_count)
        col3.metric("Total Risks", len(risks))

        st.markdown("**These are the specific scenarios your compliance team must watch for:**")
        for risk in risks:
            if "CRITICAL" in risk or "HIGH" in risk:
                st.markdown(
                    f'<div class="verdict-blocked" style="margin-bottom:8px">{risk}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="verdict-warning" style="margin-bottom:8px">{risk}</div>',
                    unsafe_allow_html=True,
                )

        st.divider()

        # Step 5: Summary Report
        st.subheader("Step 5: 📊 Compliance Summary Report")
        with st.spinner("Agent is generating final report..."):
            time.sleep(2.5)

        st.markdown(
            f"""
### 📋 Compliance Report — {selected_pipeline_product}
**Bank:** {DEMO_SCENARIO['bank_name']}

| Metric | Value |
|--------|-------|
| MAS Regulations Applicable | {len(regs)} |
| Compliance Steps Required | {len(guidelines)} |
| Business Impact Items | {len(impacts)} |
| Risk Warnings | {len(risks)} |
| Critical/High Risks | {critical_count + high_count} |

**Next Steps:**
1. Distribute this compliance checklist to all relationship managers handling {selected_pipeline_product}
2. Schedule training session on the {len(regs)} applicable MAS regulations within 2 weeks
3. Update internal SOPs to incorporate the {len(guidelines)} compliance steps
4. Set up monitoring dashboards for the {critical_count + high_count} critical/high risk scenarios
"""
        )

        st.balloons()

    else:
        st.info("👆 Select a product and click **Run Pipeline** to start the compliance analysis")

# =============================================
# TAB 2: Compliance Check (Interactive)
# =============================================
with tab2:
    st.header("🔍 Interactive Compliance Check")
    st.markdown(
        "Simulate a compliance check for a financial product sale scenario."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Profile")
        age = st.slider("Customer Age", 18, 90, 45)
        income = st.number_input(
            "Monthly Income (SGD)", min_value=0, value=5000, step=500
        )
        risk_appetite = st.selectbox(
            "Risk Appetite", ["Conservative", "Moderate", "Aggressive"]
        )
        experience = st.selectbox(
            "Investment Experience",
            ["None", "Basic (FD/Savings only)", "Intermediate", "Experienced"],
        )
        has_debt = st.checkbox("Has significant outstanding debt")
        debt_amount = 0
        if has_debt:
            debt_amount = st.number_input(
                "Total Debt (SGD)", min_value=0, value=50000, step=5000
            )

    with col2:
        st.subheader("Product Selection")
        product_names = [p["name"] for p in DEMO_SCENARIO["products"]]
        selected_product = st.selectbox("Select Product", product_names)
        product = next(
            p for p in DEMO_SCENARIO["products"] if p["name"] == selected_product
        )

        st.markdown(f"**Type:** {product['type']}")
        st.markdown(f"**Risk Level:** {product['risk_level']}")
        st.markdown(f"**Description:** {product['description']}")

        st.subheader("Sales Context")
        verbal_claim = st.text_input(
            "Representative's verbal claim (optional)",
            placeholder="e.g., 'guaranteed 8% returns'",
        )

    if st.button("🔍 Run Compliance Check", type="primary"):
        st.divider()
        st.subheader("📋 Compliance Check Results")

        with st.spinner("Agent is analyzing customer profile and checking regulations..."):
            time.sleep(3.0)

        issues = []

        # Rule 1: Age + Risk mismatch
        if age >= 65 and product["risk_level"] in ["Medium-High", "High"]:
            issues.append(
                {
                    "regulation": "FAA-N16 (Suitability)",
                    "issue": f"Customer age ({age}) indicates senior/retiree. {product['risk_level']} risk product is likely unsuitable.",
                    "severity": "HIGH",
                    "action": "Consider lower-risk alternatives. Conduct enhanced suitability assessment.",
                }
            )

        # Rule 2: Conservative + High risk
        if risk_appetite == "Conservative" and product["risk_level"] in [
            "Medium-High",
            "High",
        ]:
            issues.append(
                {
                    "regulation": "FAA-N16 (Suitability)",
                    "issue": f"Product risk ({product['risk_level']}) exceeds customer's risk appetite ({risk_appetite}).",
                    "severity": "HIGH",
                    "action": "DO NOT recommend. Product-customer risk mismatch.",
                }
            )

        # Rule 3: No experience + SIP
        if (
            experience in ["None", "Basic (FD/Savings only)"]
            and product["type"] == "Specified Investment Product (SIP)"
        ):
            issues.append(
                {
                    "regulation": "SFA04-N12 (CAR Requirement)",
                    "issue": f"Customer has limited experience ('{experience}') for a Specified Investment Product.",
                    "severity": "MEDIUM",
                    "action": "Customer must pass Customer Account Review (CAR) before purchase.",
                }
            )

        # Rule 4: High debt + investment
        if has_debt and debt_amount > income * 12:
            issues.append(
                {
                    "regulation": "FAA-N16 (Financial Situation)",
                    "issue": f"Customer debt (SGD {debt_amount:,}) exceeds annual income. Investment may not be suitable.",
                    "severity": "HIGH",
                    "action": "Assess debt obligations before recommending investment products.",
                }
            )
        elif has_debt and debt_amount > income * 6:
            issues.append(
                {
                    "regulation": "FAA-G11 Outcome 4",
                    "issue": f"Customer has significant debt (SGD {debt_amount:,}). Suitability assessment required.",
                    "severity": "MEDIUM",
                    "action": "Document rationale if proceeding with recommendation.",
                }
            )

        # Rule 5: Misleading claims
        misleading_keywords = [
            "guaranteed",
            "sure win",
            "no risk",
            "confirm profit",
            "100%",
        ]
        if verbal_claim and any(
            kw in verbal_claim.lower() for kw in misleading_keywords
        ):
            if product["risk_level"] != "Low":
                issues.append(
                    {
                        "regulation": "FAA-G11 Outcome 3 (Fair Dealing)",
                        "issue": f"Potentially misleading verbal claim: '{verbal_claim}' for a {product['risk_level']} risk product.",
                        "severity": "CRITICAL",
                        "action": "HALT SALE. Correct misleading information immediately. Retrain representative.",
                    }
                )

        # Rule 6: Low income + High risk
        if income < 3000 and product["risk_level"] in ["Medium-High", "High"]:
            issues.append(
                {
                    "regulation": "FAA-N16 (Financial Situation)",
                    "issue": f"Low income (SGD {income:,}/month) may not support {product['risk_level']} risk investment.",
                    "severity": "MEDIUM",
                    "action": "Ensure customer has adequate emergency funds before investing.",
                }
            )

        # Display results
        if not issues:
            st.markdown(
                '<div class="verdict-pass"><strong>✅ PASS</strong> — No compliance issues detected. '
                "Proceed with standard documentation requirements.</div>",
                unsafe_allow_html=True,
            )
            st.markdown("**Required actions:**")
            st.markdown("- Provide Product Highlights Sheet (PHS)")
            st.markdown("- Document basis for recommendation")
            st.markdown("- Obtain customer acknowledgment")
        else:
            has_critical = any(i["severity"] == "CRITICAL" for i in issues)
            has_high = any(i["severity"] == "HIGH" for i in issues)

            if has_critical:
                verdict = "BLOCKED"
                verdict_class = "verdict-blocked"
                verdict_text = "🚫 BLOCKED — Critical compliance violation detected. Sale must not proceed."
            elif has_high:
                verdict = "BLOCKED"
                verdict_class = "verdict-blocked"
                verdict_text = "🚫 BLOCKED — High severity compliance issues. Sale should not proceed without remediation."
            else:
                verdict = "WARNING"
                verdict_class = "verdict-warning"
                verdict_text = "⚠️ WARNING — Compliance issues found. Additional steps required before proceeding."

            st.markdown(
                f'<div class="{verdict_class}"><strong>{verdict_text}</strong></div>',
                unsafe_allow_html=True,
            )
            st.markdown("")

            for issue in issues:
                severity_colors = {
                    "CRITICAL": "🔴",
                    "HIGH": "🟠",
                    "MEDIUM": "🟡",
                }
                icon = severity_colors.get(issue["severity"], "⚪")
                st.markdown(f"#### {icon} {issue['severity']}: {issue['regulation']}")
                st.markdown(f"**Issue:** {issue['issue']}")
                st.markdown(f"**Required Action:** {issue['action']}")
                st.markdown("---")

# =============================================
# TAB 3: Analyst Tasks
# =============================================
with tab3:
    st.header("📊 Compliance Analyst Tasks — AI Automation Potential")
    st.markdown(
        "Based on the **Regulatory Compliance Manager** job description, "
        "here's how an AI Agent can automate or assist with each responsibility."
    )

    # Summary metrics
    very_high = sum(1 for t in ANALYST_TASKS if t["automation_level"] == "Very High")
    high = sum(1 for t in ANALYST_TASKS if t["automation_level"] == "High")
    medium = sum(1 for t in ANALYST_TASKS if t["automation_level"] == "Medium")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks", len(ANALYST_TASKS))
    col2.metric("🟢 Very High Automation", very_high)
    col3.metric("🔵 High Automation", high)
    col4.metric("🟡 Medium Automation", medium)

    st.divider()

    for task in ANALYST_TASKS:
        automation_colors = {
            "Very High": "🟢",
            "High": "🔵",
            "Medium": "🟡",
        }
        icon = automation_colors.get(task["automation_level"], "⚪")

        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {task['id']}: {task['task']}")
                st.markdown(f"**Current (Manual):** {task['description']}")
                st.markdown(f"**🤖 With AI Agent:** {task['agent_capability']}")
                st.markdown(
                    f"**Regulations:** {', '.join(task['related_regulations'])}"
                )
            with col2:
                st.markdown(f"### {icon}")
                st.markdown(f"**{task['automation_level']}**")
                st.markdown("Automation Potential")
            st.divider()

# =============================================
# TAB 4: Knowledge Base
# =============================================
with tab4:
    st.header("📖 MAS Regulation Knowledge Base")
    st.markdown(
        "Agent's internal knowledge base of MAS regulations relevant to financial product sales compliance."
    )

    for reg in MAS_REGULATIONS:
        with st.expander(f"📜 {reg['id']} — {reg['title']}", expanded=False):
            st.markdown(f"**Category:** {reg['category']}")
            st.markdown(f"**Source:** [{reg['source']}]({reg['source']})")
            st.markdown(f"**Summary:** {reg['summary']}")

            st.markdown("#### ✅ Key Requirements")
            for req in reg["key_requirements"]:
                st.markdown(f"- {req}")

            st.markdown("#### ⚠️ Risk Scenarios")
            for risk in reg["risk_scenarios"]:
                st.markdown(f"- 🔸 {risk}")

"""
Pipeline Data — Pre-computed simulated AI outputs for the 5-step document analysis pipeline.
Each step's output is hardcoded to demonstrate what the AI agents would produce.
"""

# ════════════════════════════════════════════════════════════════
# STEP 1: Document Ingestion — Parse Result
# ════════════════════════════════════════════════════════════════

STEP1_PARSE_RESULT = {
    "source_url": "https://www.mas.gov.sg/regulation/notices/notice-faa-n16",
    "notice_number": "FAA-N16",
    "title": "Notice on Recommendations on Investment Products (Revised)",
    "issuing_authority": "Monetary Authority of Singapore",
    "effective_date": "1 October 2026",
    "publication_date": "14 March 2026",
    "detected_at": "Friday 14 March 2026, 22:15 SGT",
    "format": "Native PDF",
    "total_pages": 47,
    "total_sections": 8,
    "total_annexes": 3,
    "total_clauses": 52,
    "total_tables": 12,
    "total_figures": 2,
    "word_count": 18_420,
    "applicability": "Licensed financial advisers and exempt financial advisers",
    "document_type": "Regulatory Notice (Revised)",
    "supersedes": "FAA-N16 (Version 2024-01, effective 1 January 2024)",
    "sections_summary": [
        {"number": "1", "heading": "Scope and Application", "clauses": 3, "pages": "1-2"},
        {"number": "2", "heading": "Definitions", "clauses": 4, "pages": "2-4"},
        {"number": "3", "heading": "General Obligations", "clauses": 4, "pages": "4-8"},
        {"number": "4", "heading": "Customer Knowledge Assessment (CKA)", "clauses": 6, "pages": "8-15"},
        {"number": "5", "heading": "Product Highlights Sheet (PHS)", "clauses": 4, "pages": "15-20"},
        {"number": "6", "heading": "Disclosure Requirements", "clauses": 4, "pages": "20-28"},
        {"number": "7", "heading": "Record-Keeping", "clauses": 4, "pages": "28-33"},
        {"number": "8", "heading": "Supervisory and Compliance Obligations", "clauses": 4, "pages": "33-38"},
        {"number": "Annex A", "heading": "Prescribed Format for PHS", "clauses": 6, "pages": "39-42"},
        {"number": "Annex B", "heading": "Product Knowledge Assessment (PKA) Requirements", "clauses": 4, "pages": "43-45"},
        {"number": "Annex C", "heading": "Digital Advisory Channel Requirements", "clauses": 4, "pages": "45-47"},
    ],
}

# ════════════════════════════════════════════════════════════════
# STEP 2: Version Comparison — Diff Result
# ════════════════════════════════════════════════════════════════

STEP2_DIFF_RESULT = {
    "old_version": "FAA-N16 (2024-01)",
    "new_version": "FAA-N16 (2026-03)",
    "summary": {
        "added": 3,
        "modified": 8,
        "removed": 1,
        "restructured": 0,
        "unchanged": 5,
    },
    "changes": [
        {
            "section": "§1.3",
            "heading": "Scope and Application",
            "change_type": "ADDED",
            "significance": "HIGH",
            "old_text": "(Not present in previous version)",
            "new_text": (
                "This Notice shall also apply to recommendations made through digital "
                "advisory channels, including robo-advisory platforms and AI-assisted "
                "recommendation systems."
            ),
            "ai_summary": (
                "NEW: Scope explicitly extended to digital advisory channels. "
                "All robo-advisory and AI-assisted recommendation systems now fall under FAA-N16. "
                "Banks operating digital platforms must ensure full compliance."
            ),
        },
        {
            "section": "§2.4",
            "heading": "Definitions",
            "change_type": "ADDED",
            "significance": "MEDIUM",
            "old_text": "(Not present in previous version)",
            "new_text": (
                "'Digital Advisory Channel' means any electronic platform or system "
                "through which investment recommendations are generated, communicated, "
                "or facilitated, whether fully automated or human-assisted."
            ),
            "ai_summary": (
                "NEW: Formal definition of 'Digital Advisory Channel' added. "
                "Broad definition covers fully automated and human-assisted platforms."
            ),
        },
        {
            "section": "§3.3",
            "heading": "General Obligations — Record Retention",
            "change_type": "MODIFIED",
            "significance": "HIGH",
            "old_text": "...retained for a minimum period of 5 years from the date of the recommendation.",
            "new_text": "...retained for a minimum period of 7 years from the date of the recommendation.",
            "ai_summary": (
                "CHANGED: Record retention period increased from 5 years to 7 years. "
                "Impacts all documentation and archival systems. IT systems may need reconfiguration."
            ),
        },
        {
            "section": "§3.4",
            "heading": "General Obligations — Digital Channels",
            "change_type": "ADDED",
            "significance": "HIGH",
            "old_text": "(Not present in previous version)",
            "new_text": (
                "Where a recommendation is made through a digital advisory channel, "
                "the financial adviser shall ensure that the algorithmic recommendation "
                "process is subject to the same suitability standards as human advisers."
            ),
            "ai_summary": (
                "NEW: Algorithmic recommendations must meet same suitability standards as human advisers. "
                "Robo-advisory platforms need suitability validation."
            ),
        },
        {
            "section": "§4.1(b)",
            "heading": "CKA — Complex Products Enhancement",
            "change_type": "ADDED",
            "significance": "HIGH",
            "old_text": "(Not present in previous version)",
            "new_text": (
                "For complex products, the CKA shall additionally assess the customer's "
                "understanding of derivative instruments, leverage, and structured payoff mechanisms."
            ),
            "ai_summary": (
                "NEW: Enhanced CKA requirements for complex products. "
                "Must now assess customer understanding of derivatives, leverage, and structured payoffs. "
                "CKA forms and processes need updating."
            ),
        },
        {
            "section": "§4.2",
            "heading": "CKA — Written Acknowledgment",
            "change_type": "MODIFIED",
            "significance": "MEDIUM",
            "old_text": "...must inform the customer that the product may not be suitable and provide additional risk disclosures.",
            "new_text": "...must inform the customer that the product may not be suitable and shall obtain written acknowledgment of enhanced risk disclosures from the customer.",
            "ai_summary": (
                "CHANGED: Now requires written acknowledgment (not just verbal disclosure) "
                "when customer fails CKA. New form/process needed."
            ),
        },
        {
            "section": "§4.4 / Annex B",
            "heading": "Product Knowledge Assessment (PKA)",
            "change_type": "ADDED",
            "significance": "HIGH",
            "old_text": "(Not present in previous version — entirely new requirement)",
            "new_text": (
                "A financial adviser shall conduct a Product Knowledge Assessment (PKA) "
                "for all structured products, ensuring that the recommending representative "
                "has completed product-specific training and demonstrated competency."
            ),
            "ai_summary": (
                "NEW: Entirely new PKA requirement. Representatives must pass product-specific "
                "assessment (minimum 80%) before recommending structured products. "
                "Annual renewal required. This is a major new compliance obligation — "
                "requires new training program, assessment system, and tracking."
            ),
        },
        {
            "section": "§5.2",
            "heading": "PHS — Risk Indicator Format",
            "change_type": "MODIFIED",
            "significance": "MEDIUM",
            "old_text": "...shall clearly state the key features, risks, and costs of the product.",
            "new_text": (
                "...shall clearly state the key features, risks, and costs of the product, "
                "including a standardized risk indicator using the prescribed color-coded "
                "label system (green, amber, red)."
            ),
            "ai_summary": (
                "CHANGED: PHS now requires standardized color-coded risk labels (green/amber/red). "
                "All PHS templates need updating."
            ),
        },
        {
            "section": "§5.4",
            "heading": "PHS — Digital Format",
            "change_type": "ADDED",
            "significance": "MEDIUM",
            "old_text": "(Not present in previous version)",
            "new_text": (
                "For digital advisory channels, the PHS must be presented in an interactive "
                "format that requires the customer to acknowledge each key risk before proceeding."
            ),
            "ai_summary": (
                "NEW: Digital PHS must be interactive with per-risk acknowledgment. "
                "Digital platforms need UI changes."
            ),
        },
        {
            "section": "§6.3",
            "heading": "Disclosure — Cooling-Off Period",
            "change_type": "MODIFIED",
            "significance": "HIGH",
            "old_text": "...shall inform the customer of any cooling-off period applicable to the product and the conditions for exercising the right to cancel.",
            "new_text": (
                "...shall inform the customer of the cooling-off period of not less than "
                "7 calendar days applicable to the product and the conditions for exercising "
                "the right to cancel, including that cancellation may be exercised "
                "unconditionally during this period."
            ),
            "ai_summary": (
                "CHANGED: Cooling-off period now explicitly mandated as minimum 7 calendar days "
                "with unconditional cancellation right. Must be clearly communicated. "
                "Sales scripts and training materials need updating."
            ),
        },
        {
            "section": "§6.4",
            "heading": "Disclosure — Scenario Analysis",
            "change_type": "ADDED",
            "significance": "HIGH",
            "old_text": "(Not present in previous version)",
            "new_text": (
                "For structured products, the financial adviser shall provide scenario "
                "analysis showing potential outcomes under adverse, base, and favorable "
                "market conditions."
            ),
            "ai_summary": (
                "NEW: Mandatory scenario analysis for structured products. "
                "Must show adverse/base/favorable outcomes. Requires new analytical tools and templates."
            ),
        },
        {
            "section": "§7.2",
            "heading": "Record-Keeping — Retention Period",
            "change_type": "MODIFIED",
            "significance": "HIGH",
            "old_text": "Records shall be kept for a minimum of 5 years...",
            "new_text": "Records shall be kept for a minimum of 7 years...",
            "ai_summary": (
                "CHANGED: Record retention extended from 5 to 7 years (consistent with §3.3). "
                "Archival and data retention policies need updating."
            ),
        },
        {
            "section": "§7.4",
            "heading": "Record-Keeping — Digital Audit Trail",
            "change_type": "ADDED",
            "significance": "HIGH",
            "old_text": "(Not present in previous version)",
            "new_text": (
                "For recommendations made through digital advisory channels, a complete "
                "audit trail of the algorithmic decision process shall be maintained."
            ),
            "ai_summary": (
                "NEW: Complete audit trail required for algorithmic recommendations. "
                "Must include model version, inputs, calculations, and outputs. "
                "Significant IT infrastructure requirement."
            ),
        },
        {
            "section": "§8.2",
            "heading": "Compliance Review Frequency",
            "change_type": "MODIFIED",
            "significance": "MEDIUM",
            "old_text": "...at a minimum on an annual basis.",
            "new_text": "...at a minimum on a semi-annual basis.",
            "ai_summary": (
                "CHANGED: Compliance review frequency doubled from annual to semi-annual. "
                "Compliance team workload increases."
            ),
        },
        {
            "section": "§8.3",
            "heading": "Breach Reporting Timeline",
            "change_type": "MODIFIED",
            "significance": "HIGH",
            "old_text": "...reported to MAS within 14 calendar days of discovery.",
            "new_text": "...reported to MAS within 7 calendar days of discovery.",
            "ai_summary": (
                "CHANGED: Breach reporting deadline halved from 14 days to 7 days. "
                "Incident response procedures need acceleration."
            ),
        },
        {
            "section": "§8.4",
            "heading": "Designated Compliance Officer",
            "change_type": "ADDED",
            "significance": "MEDIUM",
            "old_text": "(Not present in previous version)",
            "new_text": (
                "The financial adviser shall appoint a designated compliance officer "
                "responsible for overseeing compliance with this Notice."
            ),
            "ai_summary": (
                "NEW: Must appoint a designated compliance officer for FAA-N16 oversight. "
                "May require organizational changes."
            ),
        },
        {
            "section": "Annex B",
            "heading": "PKA Requirements (Entire Annex)",
            "change_type": "ADDED",
            "significance": "HIGH",
            "old_text": "(Annex did not exist in previous version)",
            "new_text": "New annex detailing PKA requirements — see §4.4 for primary obligation.",
            "ai_summary": (
                "NEW: Entire Annex B is new — Product Knowledge Assessment requirements. "
                "80% minimum score, annual renewal, authorization suspension for non-renewal. "
                "Major training infrastructure investment needed."
            ),
        },
        {
            "section": "Annex C",
            "heading": "Digital Advisory Channel Requirements (Entire Annex)",
            "change_type": "ADDED",
            "significance": "HIGH",
            "old_text": "(Annex did not exist in previous version)",
            "new_text": "New annex detailing requirements for digital advisory channels.",
            "ai_summary": (
                "NEW: Entire Annex C is new — covers algorithm validation, disclosure requirements, "
                "human adviser access, and record-keeping for digital channels."
            ),
        },
    ],
    "removed_items": [
        {
            "description": "Legacy paper-only submission option for CKA results (previously in §4.2 footnote)",
            "significance": "LOW",
            "ai_summary": "REMOVED: Paper-only CKA submission discontinued. All submissions must be electronic.",
        },
    ],
}

# ════════════════════════════════════════════════════════════════
# STEP 3: Obligation Extraction
# ════════════════════════════════════════════════════════════════

STEP3_OBLIGATIONS = [
    {
        "id": 1,
        "section_ref": "§1.3",
        "text": "This Notice shall also apply to recommendations made through digital advisory channels, including robo-advisory platforms and AI-assisted recommendation systems.",
        "obligation_type": "Mandatory",
        "category": "Scope",
        "severity": "HIGH",
        "is_new": True,
        "keywords": ["shall apply", "digital advisory channels"],
    },
    {
        "id": 2,
        "section_ref": "§3.1",
        "text": "A licensed financial adviser shall ensure that any recommendation made to a customer is suitable, having regard to the customer's investment objectives, financial situation, and particular needs.",
        "obligation_type": "Mandatory",
        "category": "Suitability",
        "severity": "CRITICAL",
        "is_new": False,
        "keywords": ["shall ensure", "suitable"],
    },
    {
        "id": 3,
        "section_ref": "§3.2",
        "text": "The financial adviser must have a reasonable basis for making any recommendation to the customer.",
        "obligation_type": "Mandatory",
        "category": "Suitability",
        "severity": "CRITICAL",
        "is_new": False,
        "keywords": ["must have", "reasonable basis"],
    },
    {
        "id": 4,
        "section_ref": "§3.3",
        "text": "All recommendations shall be documented and retained for a minimum period of 7 years from the date of the recommendation.",
        "obligation_type": "Mandatory",
        "category": "Record-Keeping",
        "severity": "HIGH",
        "is_new": False,
        "keywords": ["shall be documented", "7 years"],
        "change_note": "Retention period increased from 5 to 7 years",
    },
    {
        "id": 5,
        "section_ref": "§3.4",
        "text": "Where a recommendation is made through a digital advisory channel, the financial adviser shall ensure that the algorithmic recommendation process is subject to the same suitability standards as human advisers.",
        "obligation_type": "Mandatory",
        "category": "Digital Advisory",
        "severity": "HIGH",
        "is_new": True,
        "keywords": ["shall ensure", "algorithmic", "same suitability standards"],
    },
    {
        "id": 6,
        "section_ref": "§4.1",
        "text": "A financial adviser shall conduct a Customer Knowledge Assessment before recommending any specified investment product to a customer.",
        "obligation_type": "Mandatory",
        "category": "Suitability",
        "severity": "CRITICAL",
        "is_new": False,
        "keywords": ["shall conduct", "CKA"],
    },
    {
        "id": 7,
        "section_ref": "§4.1(b)",
        "text": "For complex products, the CKA shall additionally assess the customer's understanding of derivative instruments, leverage, and structured payoff mechanisms.",
        "obligation_type": "Mandatory",
        "category": "Suitability",
        "severity": "HIGH",
        "is_new": True,
        "keywords": ["shall additionally assess", "derivative instruments", "leverage"],
    },
    {
        "id": 8,
        "section_ref": "§4.2",
        "text": "Where a customer does not pass the CKA, the financial adviser must inform the customer and shall obtain written acknowledgment of enhanced risk disclosures.",
        "obligation_type": "Mandatory",
        "category": "Disclosure",
        "severity": "HIGH",
        "is_new": False,
        "keywords": ["must inform", "shall obtain", "written acknowledgment"],
        "change_note": "Now requires written acknowledgment (was verbal)",
    },
    {
        "id": 9,
        "section_ref": "§4.3",
        "text": "A financial adviser shall not recommend a complex product to a Selected Client unless the client passes the CKA and the adviser has conducted an enhanced suitability assessment.",
        "obligation_type": "Prohibitive",
        "category": "Suitability",
        "severity": "CRITICAL",
        "is_new": False,
        "keywords": ["shall not recommend", "Selected Client", "enhanced suitability"],
    },
    {
        "id": 10,
        "section_ref": "§4.4",
        "text": "A financial adviser shall conduct a Product Knowledge Assessment (PKA) for all structured products, ensuring that the recommending representative has completed product-specific training and demonstrated competency.",
        "obligation_type": "Mandatory",
        "category": "Training",
        "severity": "HIGH",
        "is_new": True,
        "keywords": ["shall conduct", "PKA", "structured products", "competency"],
    },
    {
        "id": 11,
        "section_ref": "§5.1",
        "text": "Before recommending any investment product, the financial adviser must provide the customer with a Product Highlights Sheet.",
        "obligation_type": "Mandatory",
        "category": "Disclosure",
        "severity": "HIGH",
        "is_new": False,
        "keywords": ["must provide", "PHS"],
    },
    {
        "id": 12,
        "section_ref": "§5.2",
        "text": "The PHS must be in the prescribed format and shall clearly state the key features, risks, and costs, including a standardized risk indicator using the prescribed color-coded label system.",
        "obligation_type": "Mandatory",
        "category": "Disclosure",
        "severity": "HIGH",
        "is_new": False,
        "keywords": ["must be", "prescribed format", "color-coded label"],
        "change_note": "Now requires standardized color-coded risk labels",
    },
    {
        "id": 13,
        "section_ref": "§5.4",
        "text": "For digital advisory channels, the PHS must be presented in an interactive format that requires the customer to acknowledge each key risk before proceeding.",
        "obligation_type": "Mandatory",
        "category": "Digital Advisory",
        "severity": "MEDIUM",
        "is_new": True,
        "keywords": ["must be presented", "interactive format", "acknowledge"],
    },
    {
        "id": 14,
        "section_ref": "§6.1",
        "text": "The financial adviser shall disclose to the customer all material information relating to the recommended product, including risk level, fees and charges, and any conflicts of interest.",
        "obligation_type": "Mandatory",
        "category": "Disclosure",
        "severity": "CRITICAL",
        "is_new": False,
        "keywords": ["shall disclose", "material information"],
    },
    {
        "id": 15,
        "section_ref": "§6.2",
        "text": "All fees and charges, including management fees, distribution fees, and early redemption penalties, must be clearly explained to the customer before any transaction is executed.",
        "obligation_type": "Mandatory",
        "category": "Disclosure",
        "severity": "HIGH",
        "is_new": False,
        "keywords": ["must be clearly explained", "fees and charges"],
    },
    {
        "id": 16,
        "section_ref": "§6.3",
        "text": "The financial adviser shall inform the customer of the cooling-off period of not less than 7 calendar days and that cancellation may be exercised unconditionally during this period.",
        "obligation_type": "Mandatory",
        "category": "T&C",
        "severity": "CRITICAL",
        "is_new": False,
        "keywords": ["shall inform", "cooling-off period", "7 calendar days", "unconditionally"],
        "change_note": "Now explicitly mandates 7-day minimum and unconditional cancellation",
    },
    {
        "id": 17,
        "section_ref": "§6.4",
        "text": "For structured products, the financial adviser shall provide scenario analysis showing potential outcomes under adverse, base, and favorable market conditions.",
        "obligation_type": "Mandatory",
        "category": "Disclosure",
        "severity": "HIGH",
        "is_new": True,
        "keywords": ["shall provide", "scenario analysis", "adverse", "base", "favorable"],
    },
    {
        "id": 18,
        "section_ref": "§7.2",
        "text": "Records shall be kept for a minimum of 7 years from the date of the recommendation or the termination of the product, whichever is later.",
        "obligation_type": "Mandatory",
        "category": "Record-Keeping",
        "severity": "HIGH",
        "is_new": False,
        "keywords": ["shall be kept", "7 years"],
        "change_note": "Retention extended from 5 to 7 years",
    },
    {
        "id": 19,
        "section_ref": "§7.4",
        "text": "For recommendations made through digital advisory channels, a complete audit trail of the algorithmic decision process shall be maintained, including model inputs, intermediate calculations, and the final recommendation.",
        "obligation_type": "Mandatory",
        "category": "Digital Advisory",
        "severity": "HIGH",
        "is_new": True,
        "keywords": ["shall be maintained", "audit trail", "algorithmic"],
    },
    {
        "id": 20,
        "section_ref": "§8.2",
        "text": "The financial adviser must conduct periodic reviews of its compliance with this Notice, at a minimum on a semi-annual basis.",
        "obligation_type": "Mandatory",
        "category": "Compliance",
        "severity": "MEDIUM",
        "is_new": False,
        "keywords": ["must conduct", "semi-annual"],
        "change_note": "Frequency increased from annual to semi-annual",
    },
    {
        "id": 21,
        "section_ref": "§8.3",
        "text": "Any material breach of this Notice shall be reported to MAS within 7 calendar days of discovery.",
        "obligation_type": "Mandatory",
        "category": "Compliance",
        "severity": "CRITICAL",
        "is_new": False,
        "keywords": ["shall be reported", "7 calendar days"],
        "change_note": "Reporting deadline halved from 14 to 7 days",
    },
    {
        "id": 22,
        "section_ref": "§8.4",
        "text": "The financial adviser shall appoint a designated compliance officer responsible for overseeing compliance with this Notice.",
        "obligation_type": "Mandatory",
        "category": "Compliance",
        "severity": "MEDIUM",
        "is_new": True,
        "keywords": ["shall appoint", "designated compliance officer"],
    },
    {
        "id": 23,
        "section_ref": "Annex B §3",
        "text": "Representatives must achieve a minimum score of 80% on the PKA before being authorized to recommend the relevant product.",
        "obligation_type": "Mandatory",
        "category": "Training",
        "severity": "HIGH",
        "is_new": True,
        "keywords": ["must achieve", "80%", "PKA"],
    },
    {
        "id": 24,
        "section_ref": "Annex B §4",
        "text": "The PKA must be renewed annually, and representatives who fail to renew shall have their authorization suspended.",
        "obligation_type": "Mandatory",
        "category": "Training",
        "severity": "HIGH",
        "is_new": True,
        "keywords": ["must be renewed", "annually", "authorization suspended"],
    },
    {
        "id": 25,
        "section_ref": "Annex C §1",
        "text": "Financial advisers operating digital advisory channels shall ensure that the recommendation algorithm is validated by an independent party at least annually.",
        "obligation_type": "Mandatory",
        "category": "Digital Advisory",
        "severity": "HIGH",
        "is_new": True,
        "keywords": ["shall ensure", "algorithm", "validated", "independent party"],
    },
    {
        "id": 26,
        "section_ref": "Annex C §3",
        "text": "Customers using digital advisory channels shall have access to a human adviser upon request at any point during the recommendation process.",
        "obligation_type": "Mandatory",
        "category": "Digital Advisory",
        "severity": "MEDIUM",
        "is_new": True,
        "keywords": ["shall have access", "human adviser"],
    },
]

# ════════════════════════════════════════════════════════════════
# STEP 4: Product Impact Mapping
# ════════════════════════════════════════════════════════════════

STEP4_PRODUCT_MAP = [
    {
        "product": "Enhanced Yield Structured Deposit",
        "impact_level": "HIGH",
        "applicable_obligations": [2, 3, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 23, 24],
        "key_changes": [
            "NEW: PKA required for all representatives selling this product (§4.4, Annex B)",
            "NEW: Mandatory scenario analysis — adverse/base/favorable outcomes (§6.4)",
            "CHANGED: Enhanced CKA now tests derivatives and structured payoff understanding (§4.1b)",
            "CHANGED: Cooling-off now explicitly 7 days unconditional (§6.3)",
            "CHANGED: PHS needs color-coded risk labels (§5.2)",
        ],
        "affected_departments": ["Wealth Management", "Compliance", "IT", "Training"],
        "gaps": [
            "No PKA system exists — need to build assessment and tracking",
            "Scenario analysis templates not yet developed",
            "CKA forms need updating for derivatives/leverage questions",
            "Sales scripts need cooling-off period language update",
        ],
        "deadline": "1 October 2026",
    },
    {
        "product": "Global Equity OTC Derivative",
        "impact_level": "HIGH",
        "applicable_obligations": [2, 3, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 23, 24],
        "key_changes": [
            "NEW: PKA required — representatives must score 80%+ (§4.4, Annex B)",
            "NEW: Scenario analysis mandatory for this product type (§6.4)",
            "CHANGED: CKA enhanced for derivatives understanding (§4.1b)",
            "CHANGED: PHS format update with color-coded labels (§5.2)",
            "CHANGED: Record retention 5→7 years (§7.2)",
        ],
        "affected_departments": ["Treasury & Markets", "Compliance", "IT", "Training"],
        "gaps": [
            "PKA assessment needs product-specific content for OTC derivatives",
            "Scenario analysis tooling does not exist",
            "Current record retention is 5 years — data migration needed",
            "CKA forms lack derivatives/leverage assessment",
        ],
        "deadline": "1 October 2026",
    },
    {
        "product": "Asia Pacific Growth Fund",
        "impact_level": "MEDIUM",
        "applicable_obligations": [2, 3, 6, 8, 11, 12, 14, 15, 16, 18, 20],
        "key_changes": [
            "CHANGED: CKA written acknowledgment now required for failed CKA (§4.2)",
            "CHANGED: Record retention 5→7 years (§3.3, §7.2)",
            "CHANGED: PHS needs color-coded risk labels (§5.2)",
            "CHANGED: Compliance review now semi-annual (§8.2)",
        ],
        "affected_departments": ["Retail Banking", "Compliance"],
        "gaps": [
            "CKA acknowledgment form needs updating",
            "Data retention policy needs extension",
            "PHS template update needed",
            "Compliance review calendar needs adjustment",
        ],
        "deadline": "1 October 2026",
    },
    {
        "product": "Term Life Insurance (Investment-Linked)",
        "impact_level": "MEDIUM",
        "applicable_obligations": [2, 3, 6, 8, 11, 12, 14, 15, 16, 18, 20],
        "key_changes": [
            "CHANGED: Record retention 5→7 years (§3.3, §7.2)",
            "CHANGED: Cooling-off explicitly 7 days unconditional (§6.3)",
            "CHANGED: PHS color-coded labels (§5.2)",
            "CHANGED: Compliance review semi-annual (§8.2)",
        ],
        "affected_departments": ["Insurance", "Compliance", "Training"],
        "gaps": [
            "Sales scripts need cooling-off language update",
            "PHS template redesign",
            "Data retention extension",
        ],
        "deadline": "1 October 2026",
    },
    {
        "product": "Fixed Deposit (12-month)",
        "impact_level": "LOW",
        "applicable_obligations": [2, 3, 14, 18],
        "key_changes": [
            "CHANGED: Record retention 5→7 years (§7.2)",
            "Minimal impact — not a specified investment product",
        ],
        "affected_departments": ["Retail Banking"],
        "gaps": [
            "Data retention policy update only",
        ],
        "deadline": "1 October 2026",
    },
]

# ════════════════════════════════════════════════════════════════
# STEP 5: Impact Assessment Report
# ════════════════════════════════════════════════════════════════

STEP5_REPORT = {
    "title": "Impact Assessment Report — MAS Notice FAA-N16 (Revised March 2026)",
    "bank": "Horizon Bank Singapore",
    "prepared_by": "AI Agent Compliance Platform (reviewed by Sarah Chen)",
    "date": "17 March 2026",
    "executive_summary": (
        "MAS has issued a revised Notice FAA-N16 effective 1 October 2026, introducing "
        "significant changes to investment product recommendation requirements. The revision "
        "adds 3 entirely new sections (Digital Advisory Channels, Product Knowledge Assessment, "
        "and enhanced CKA requirements), modifies 8 existing clauses (notably extending record "
        "retention from 5 to 7 years, doubling compliance review frequency, and halving breach "
        "reporting timelines), and removes 1 legacy provision. "
        "Of 26 extracted obligations, 12 are new or materially changed. "
        "Impact is HIGH for Structured Deposits and OTC Derivatives, MEDIUM for Investment Funds "
        "and ILPs, and LOW for Fixed Deposits. Immediate action is required on PKA implementation "
        "and CKA form updates. Estimated compliance cost: S$180,000-250,000."
    ),
    "compliance_readiness_score": 62,
    "risk_matrix": [
        {"product": "Enhanced Yield Structured Deposit", "suitability": "HIGH", "disclosure": "HIGH", "training": "HIGH", "record_keeping": "MEDIUM", "overall": "HIGH"},
        {"product": "Global Equity OTC Derivative", "suitability": "HIGH", "disclosure": "HIGH", "training": "HIGH", "record_keeping": "HIGH", "overall": "HIGH"},
        {"product": "Asia Pacific Growth Fund", "suitability": "MEDIUM", "disclosure": "MEDIUM", "training": "LOW", "record_keeping": "MEDIUM", "overall": "MEDIUM"},
        {"product": "Term Life Insurance (ILP)", "suitability": "MEDIUM", "disclosure": "MEDIUM", "training": "LOW", "record_keeping": "MEDIUM", "overall": "MEDIUM"},
        {"product": "Fixed Deposit (12-month)", "suitability": "LOW", "disclosure": "LOW", "training": "NONE", "record_keeping": "LOW", "overall": "LOW"},
    ],
    "action_items": [
        {
            "priority": "P0",
            "action": "Design and implement Product Knowledge Assessment (PKA) system",
            "owner": "Training Dept + IT",
            "deadline": "1 August 2026",
            "status": "Not Started",
            "cost_estimate": "S$45,000",
        },
        {
            "priority": "P0",
            "action": "Update CKA forms to include derivatives/leverage assessment for complex products",
            "owner": "Compliance",
            "deadline": "1 July 2026",
            "status": "Not Started",
            "cost_estimate": "S$15,000",
        },
        {
            "priority": "P0",
            "action": "Develop scenario analysis templates and tools for structured products",
            "owner": "Risk + IT",
            "deadline": "1 August 2026",
            "status": "Not Started",
            "cost_estimate": "S$35,000",
        },
        {
            "priority": "P1",
            "action": "Update all PHS templates with color-coded risk labels",
            "owner": "Product + Compliance",
            "deadline": "1 September 2026",
            "status": "Not Started",
            "cost_estimate": "S$20,000",
        },
        {
            "priority": "P1",
            "action": "Extend data retention from 5 to 7 years across all systems",
            "owner": "IT",
            "deadline": "1 September 2026",
            "status": "Not Started",
            "cost_estimate": "S$30,000",
        },
        {
            "priority": "P1",
            "action": "Update sales scripts with cooling-off period language (7 days, unconditional)",
            "owner": "Sales + Compliance",
            "deadline": "1 August 2026",
            "status": "Not Started",
            "cost_estimate": "S$5,000",
        },
        {
            "priority": "P1",
            "action": "Revise incident response procedures for 7-day breach reporting",
            "owner": "Compliance + Legal",
            "deadline": "1 July 2026",
            "status": "Not Started",
            "cost_estimate": "S$8,000",
        },
        {
            "priority": "P2",
            "action": "Adjust compliance review calendar from annual to semi-annual",
            "owner": "Compliance",
            "deadline": "1 September 2026",
            "status": "Not Started",
            "cost_estimate": "S$5,000",
        },
        {
            "priority": "P2",
            "action": "Appoint designated compliance officer for FAA-N16",
            "owner": "Head of Compliance",
            "deadline": "1 July 2026",
            "status": "Not Started",
            "cost_estimate": "S$0 (internal appointment)",
        },
        {
            "priority": "P2",
            "action": "Conduct gap assessment for digital advisory channel requirements (if applicable)",
            "owner": "Digital Banking + Compliance",
            "deadline": "1 August 2026",
            "status": "Not Started",
            "cost_estimate": "S$15,000",
        },
    ],
    "total_cost_estimate": "S$178,000 - S$250,000",
    "next_steps": [
        "Present this report to Senior Management by 19 March 2026",
        "Schedule kickoff meetings with affected departments by 24 March 2026",
        "Submit implementation plan to MAS by 30 April 2026",
        "Begin P0 action items immediately — target completion by August 2026",
        "Schedule mid-point review for June 2026",
    ],
}

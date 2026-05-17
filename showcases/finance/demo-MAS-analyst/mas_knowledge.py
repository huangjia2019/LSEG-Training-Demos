"""
MAS Regulation Knowledge Base (V1 - Hardcoded excerpts)
In V2+, this will be replaced by real MAS website scraping + vector DB retrieval.
"""

# Simulated MAS regulation documents relevant to financial product sales
MAS_REGULATIONS = [
    {
        "id": "MAS-FAA-N16",
        "title": "MAS Notice on Recommendation of Investment Products (FAA-N16)",
        "source": "https://www.mas.gov.sg/regulation/notices/notice-faa-n16",
        "category": "Fair Dealing / Suitability",
        "summary": "Financial advisers must ensure suitability of product recommendations based on customer's financial objectives, risk tolerance, and financial situation.",
        "key_requirements": [
            "Conduct a Customer Knowledge Assessment (CKA) before recommending investment products",
            "Assess customer's risk tolerance, investment horizon, and financial situation",
            "Products recommended must match customer's risk profile",
            "Maintain records of basis for each recommendation for at least 5 years",
            "Provide a written basis for recommendation to the customer",
        ],
        "risk_scenarios": [
            "Recommending high-risk structured products to a retiree with low risk appetite",
            "Selling complex derivatives to a customer who failed the CKA",
            "Not documenting the rationale for product recommendation",
        ],
    },
    {
        "id": "MAS-FAA-G11",
        "title": "MAS Guidelines on Fair Dealing (FAA-G11)",
        "source": "https://www.mas.gov.sg/regulation/guidelines/guidelines-on-fair-dealing---board-and-senior-management-responsibilities-for-delivering-fair-dealing-outcomes-to-customers",
        "category": "Fair Dealing / Consumer Protection",
        "summary": "Board and senior management must deliver 5 fair dealing outcomes to customers throughout the product lifecycle.",
        "key_requirements": [
            "Outcome 1: Customers have confidence the FI treats them fairly",
            "Outcome 2: Products and services are suitable for the target customer segments",
            "Outcome 3: Customers receive clear, relevant, and timely information to make informed decisions",
            "Outcome 4: Financial advisers provide suitable advice taking into account customers' circumstances",
            "Outcome 5: Customers receive quality advice and appropriate after-sales service",
        ],
        "risk_scenarios": [
            "Marketing high-yield products to elderly customers without emphasizing risks",
            "Using jargon-heavy product descriptions that customers cannot understand",
            "Failing to follow up with customers after product purchase",
        ],
    },
    {
        "id": "MAS-SFA04-N12",
        "title": "MAS Notice on Sale of Investment Products (SFA04-N12)",
        "source": "https://www.mas.gov.sg/regulation/notices/notice-sfa-04-n12",
        "category": "Product Sales Conduct",
        "summary": "Requirements for the sale of investment products including specified investment products (SIPs) and excluded investment products (EIPs).",
        "key_requirements": [
            "Classify products as Specified Investment Products (SIP) or Excluded Investment Products (EIP)",
            "Customers must pass Customer Account Review (CAR) for SIPs",
            "Provide Product Highlights Sheet (PHS) before or at point of sale",
            "Ensure adequate product training for representatives",
            "Record-keeping of all sales transactions and customer interactions",
        ],
        "risk_scenarios": [
            "Selling Specified Investment Products to customers who have not passed the CAR",
            "Not providing the Product Highlights Sheet before sale completion",
            "Representatives selling products they have not been trained on",
        ],
    },
    {
        "id": "MAS-TCA",
        "title": "MAS Guidelines on Technology and Cyber Risk Management (TRM)",
        "source": "https://www.mas.gov.sg/regulation/notices/fsm-n30-trm",
        "category": "Technology Risk",
        "summary": "Guidelines for FIs on managing technology and cyber risks in digital banking and financial services.",
        "key_requirements": [
            "Implement strong customer authentication for digital transactions",
            "Ensure data protection and privacy in all digital channels",
            "Maintain audit trails for all digital transactions",
            "Conduct regular vulnerability assessments and penetration testing",
            "Incident reporting within 1 hour for major security breaches",
        ],
        "risk_scenarios": [
            "Digital product sales without adequate authentication",
            "Customer data leakage through insecure APIs",
            "No audit trail for online product recommendations",
        ],
    },
    {
        "id": "MAS-AML-CFT",
        "title": "MAS Notice on Prevention of Money Laundering and Countering the Financing of Terrorism",
        "source": "https://www.mas.gov.sg/regulation/notices/notice-626",
        "category": "AML/CFT",
        "summary": "Requirements for customer due diligence, ongoing monitoring, and suspicious transaction reporting.",
        "key_requirements": [
            "Perform Customer Due Diligence (CDD) at onboarding",
            "Enhanced Due Diligence (EDD) for high-risk customers (PEPs, high-risk jurisdictions)",
            "Ongoing transaction monitoring for suspicious activities",
            "File Suspicious Transaction Reports (STR) to STRO within prescribed timelines",
            "Periodic review of customer risk profiles",
            "Screen customers against sanctions lists and PEP databases",
        ],
        "risk_scenarios": [
            "Onboarding a customer without proper identity verification",
            "Missing suspicious transaction patterns due to inadequate monitoring",
            "Delayed filing of STR beyond regulatory timelines",
        ],
    },
    {
        "id": "MAS-OUTSOURCING",
        "title": "MAS Guidelines on Outsourcing (MAS-G06)",
        "source": "https://www.mas.gov.sg/regulation/guidelines/guidelines-on-outsourcing-banks",
        "category": "Outsourcing Risk",
        "summary": "Requirements for managing risks associated with outsourcing arrangements by financial institutions.",
        "key_requirements": [
            "Board oversight of all material outsourcing arrangements",
            "Risk assessment before entering outsourcing arrangements",
            "Due diligence on service providers",
            "MAS notification for material outsourcing arrangements",
            "Maintain access to data and audit rights over outsourced functions",
            "Business continuity planning for outsourced services",
        ],
        "risk_scenarios": [
            "Using a cloud provider without proper risk assessment",
            "No exit strategy for critical outsourced compliance functions",
            "Failure to notify MAS of material outsourcing",
        ],
    },
]

# Compliance analyst tasks derived from the JD
ANALYST_TASKS = [
    {
        "id": "T1",
        "task": "Regulatory Advisory on Product Development",
        "description": "Provide end-to-end regulatory compliance advice to business, legal, and product teams on new product initiatives and changes to existing offerings.",
        "related_regulations": ["MAS-FAA-N16", "MAS-FAA-G11", "MAS-SFA04-N12"],
        "agent_capability": "Auto-scan new product proposals against MAS regulatory requirements and flag compliance gaps before launch.",
        "automation_level": "High",
    },
    {
        "id": "T2",
        "task": "MAS Regulation Interpretation & Application",
        "description": "Interpret MAS regulations (Payment Services Act, SFA, FAA, Banking Act) and apply them pragmatically to product design and operational processes.",
        "related_regulations": ["MAS-FAA-N16", "MAS-FAA-G11", "MAS-SFA04-N12"],
        "agent_capability": "Parse and summarize new/updated MAS regulations, extract actionable requirements, and map them to existing business processes.",
        "automation_level": "High",
    },
    {
        "id": "T3",
        "task": "Customer Due Diligence & Monitoring",
        "description": "Conduct due diligence on customers from onboarding, including ongoing monitoring and periodic review.",
        "related_regulations": ["MAS-AML-CFT"],
        "agent_capability": "Automated CDD checks, risk scoring, PEP/sanctions screening, and anomaly detection in transaction patterns.",
        "automation_level": "Very High",
    },
    {
        "id": "T4",
        "task": "AML Compliance & STR Filing",
        "description": "Ensure timely preparation and submission of suspicious activity reports in adherence to regulatory standards.",
        "related_regulations": ["MAS-AML-CFT"],
        "agent_capability": "AI-powered transaction monitoring, automated STR draft generation, and timeline tracking for filing deadlines.",
        "automation_level": "High",
    },
    {
        "id": "T5",
        "task": "Internal Policy & Control Framework",
        "description": "Lead implementation of internal policies, controls, and frameworks aligned with Singapore regulatory requirements.",
        "related_regulations": ["MAS-FAA-G11", "MAS-AML-CFT", "MAS-TCA"],
        "agent_capability": "Auto-generate policy templates based on MAS guidelines, track policy review cycles, and identify gaps against regulatory updates.",
        "automation_level": "Medium",
    },
    {
        "id": "T6",
        "task": "Outsourcing Compliance",
        "description": "Support outsourcing arrangements including regulatory notifications, due diligence, and ongoing oversight under MAS outsourcing guidelines.",
        "related_regulations": ["MAS-OUTSOURCING"],
        "agent_capability": "Automated vendor risk assessment, MAS notification tracking, and outsourcing agreement compliance review.",
        "automation_level": "Medium",
    },
    {
        "id": "T7",
        "task": "Compliance Training & Awareness",
        "description": "Conduct internal training to build compliance awareness and capability within the business.",
        "related_regulations": ["MAS-FAA-G11", "MAS-FAA-N16", "MAS-SFA04-N12"],
        "agent_capability": "AI-generated training content from latest regulations, interactive Q&A chatbot for compliance queries, and training completion tracking.",
        "automation_level": "Very High",
    },
    {
        "id": "T8",
        "task": "Regulatory Change Monitoring",
        "description": "Stay ahead of emerging regulatory trends through industry events, working groups, and MAS consultations.",
        "related_regulations": ["MAS-FAA-N16", "MAS-FAA-G11", "MAS-SFA04-N12", "MAS-AML-CFT", "MAS-TCA", "MAS-OUTSOURCING"],
        "agent_capability": "Auto-monitor MAS website for new consultations, circulars, and regulatory updates. Summarize changes and assess impact on current operations.",
        "automation_level": "Very High",
    },
]

# ============================================================
# Product-Regulation mapping for Pipeline Demo
# Each product maps to: relevant regulations, compliance guidelines,
# business impact, and specific risk warnings
# ============================================================
PRODUCT_COMPLIANCE_MAP = {
    "Unit Trust / Mutual Fund": {
        "description": "Selling unit trusts (e.g. equity funds, bond funds, balanced funds) to retail customers through the bank's wealth management channel.",
        "relevant_regulations": [
            {
                "id": "FAA-N16",
                "title": "Notice on Recommendations on Investment Products",
                "url": "https://www.mas.gov.sg/regulation/notices/notice-faa-n16",
                "relevance": "Governs how financial advisers must assess suitability before recommending any investment product, including unit trusts.",
            },
            {
                "id": "SFA04-N12",
                "title": "Notice on Sale of Investment Products",
                "url": "https://www.mas.gov.sg/regulation/notices/notice-sfa-04-n12",
                "relevance": "Unit trusts classified as Specified Investment Products (SIP) require Customer Account Review (CAR) and Product Highlights Sheet (PHS).",
            },
            {
                "id": "FSG-G04 (Fair Dealing)",
                "title": "Guidelines on Fair Dealing",
                "url": "https://www.mas.gov.sg/regulation/guidelines/guidelines-on-fair-dealing---board-and-senior-management-responsibilities-for-delivering-fair-dealing-outcomes-to-customers",
                "relevance": "Board must ensure fund products are designed and marketed for suitable customer segments (Outcome 2), and clear fee/risk disclosures are provided (Outcome 3).",
            },
        ],
        "compliance_guidelines": [
            "Conduct Customer Knowledge Assessment (CKA) — customer must demonstrate understanding of fund risks before purchase",
            "Perform Customer Account Review (CAR) for SIP-classified funds — assess financial situation, investment experience, and objectives",
            "Provide Product Highlights Sheet (PHS) before or at point of sale — must include fund strategy, fees, risks, and past performance",
            "Document the basis of recommendation in writing and retain for at least 5 years",
            "Ensure representative holds valid CMFAS Module 5/9/9A certification for fund distribution",
        ],
        "business_impact": [
            "Sales cycle lengthened by ~15-20 mins per customer for mandatory CKA + CAR process",
            "Representatives cannot recommend SIP funds to customers who fail CAR — limits eligible customer base",
            "All fund marketing materials must go through compliance review before distribution",
            "Fee disclosure requirements may lead to customer pushback — train reps on transparent communication",
            "Non-compliance penalties: MAS can impose fines up to SGD 1M, revoke FA licence, or issue public reprimands",
        ],
        "risk_warnings": [
            "🔴 HIGH: Recommending high-risk equity funds to elderly/conservative customers without documenting suitability rationale → FAA-N16 breach",
            "🔴 HIGH: Selling SIP funds without completing CAR → SFA04-N12 breach, potential forced reversal of transaction",
            "🟡 MEDIUM: Rep verbally promises 'guaranteed returns' on a non-guaranteed fund → FSG-G04 Outcome 3 violation (misleading information)",
            "🟡 MEDIUM: Not providing PHS or providing it only after sale → SFA04-N12 procedural breach",
            "🟠 MEDIUM: Churning — frequent switching between funds to generate commissions → FAA-N16 suitability + FSG-G04 Outcome 1 (fair dealing)",
        ],
    },
    "Life Insurance (Investment-Linked)": {
        "description": "Distributing investment-linked insurance policies (ILPs) through the bank's bancassurance channel. ILPs combine insurance coverage with investment components linked to sub-funds.",
        "relevant_regulations": [
            {
                "id": "FAA-N16",
                "title": "Notice on Recommendations on Investment Products",
                "url": "https://www.mas.gov.sg/regulation/notices/notice-faa-n16",
                "relevance": "ILPs are investment products — reps must conduct needs analysis covering both protection and investment needs before recommending.",
            },
            {
                "id": "FSG-G04 (Fair Dealing)",
                "title": "Guidelines on Fair Dealing",
                "url": "https://www.mas.gov.sg/regulation/guidelines/guidelines-on-fair-dealing---board-and-senior-management-responsibilities-for-delivering-fair-dealing-outcomes-to-customers",
                "relevance": "Customers must clearly understand that ILP returns are not guaranteed, early surrender charges apply, and insurance coverage details.",
            },
            {
                "id": "MAS Notice 307",
                "title": "MAS Notice 307 — Insurance Intermediaries",
                "url": "https://www.mas.gov.sg/regulation/notices/notice-307",
                "relevance": "Specific requirements for insurance intermediaries distributing life policies, including bancassurance arrangements.",
            },
        ],
        "compliance_guidelines": [
            "Conduct Financial Needs Analysis (FNA) — must assess both insurance protection gap AND investment needs",
            "Provide Benefit Illustration (BI) showing projected returns at 3.25% and 4.75% investment rates of return",
            "Disclose all fees clearly: distribution cost, fund management charges, insurance charges, surrender penalties",
            "14-day free-look period — inform customer of right to cancel within 14 days of receiving policy documents",
            "Replacement policy rules: if customer is switching from existing policy, rep must complete replacement form and justify why new policy is better",
        ],
        "business_impact": [
            "Bancassurance sales require dual licensing — rep needs both CMFAS and insurance-related certifications",
            "FNA adds ~30 mins to each sales interaction — impacts productivity KPIs for relationship managers",
            "14-day free-look period means revenue recognition is delayed and cancellation rates must be tracked",
            "Replacement policy scrutiny may slow cross-selling from competitor products",
            "MAS has imposed penalties of SGD 100K–1M on banks for ILP mis-selling in past enforcement actions",
        ],
        "risk_warnings": [
            "🔴 HIGH: Selling ILPs primarily as investment vehicles without adequate insurance coverage analysis → FAA-N16 needs analysis failure",
            "🔴 HIGH: Not disclosing surrender penalties — customer discovers 5-year lock-in only when trying to exit → FSG-G04 Outcome 3 breach",
            "🟡 MEDIUM: Replacing a customer's existing whole-life policy with an ILP without proper justification → Replacement policy rules violation",
            "🟡 MEDIUM: Rep projects unrealistic investment returns verbally while BI shows lower numbers → misleading representation",
            "🟠 MEDIUM: Targeting elderly customers for long-tenor ILPs (15-25 years) that exceed their life expectancy planning horizon",
        ],
    },
    "Remittance / Cross-Border Transfer": {
        "description": "Processing cross-border remittance transactions for retail and SME customers, including wire transfers, online remittances, and correspondent banking payments.",
        "relevant_regulations": [
            {
                "id": "MAS Notice 626",
                "title": "Prevention of Money Laundering and Countering the Financing of Terrorism — Banks",
                "url": "https://www.mas.gov.sg/regulation/notices/notice-626",
                "relevance": "Core AML/CFT obligations: Customer Due Diligence, transaction monitoring, sanctions screening, and STR filing for all banking transactions including remittances.",
            },
            {
                "id": "MAS Notice PSN02",
                "title": "Prevention of Money Laundering and CFT — Payment Service Providers",
                "url": "https://www.mas.gov.sg/regulation/notices/psn02",
                "relevance": "If remittance is provided under Payment Services Act licence, additional AML/CFT requirements specific to payment service providers apply.",
            },
            {
                "id": "FATF Travel Rule",
                "title": "MAS Notice on Cross-Border Wire Transfers (aligned with FATF Recommendation 16)",
                "url": "https://www.mas.gov.sg/regulation/notices/notice-626",
                "relevance": "Originator and beneficiary information must accompany all cross-border wire transfers above SGD 1,500 — the 'Travel Rule'.",
            },
        ],
        "compliance_guidelines": [
            "Perform Customer Due Diligence (CDD) at onboarding — verify identity with NRIC/passport, proof of address, source of funds",
            "Enhanced Due Diligence (EDD) for: PEPs, customers from high-risk jurisdictions (FATF grey/black list), unusual transaction patterns",
            "Screen all parties (sender, beneficiary, intermediary banks) against UN/OFAC/MAS sanctions lists before processing",
            "Travel Rule: include full originator info (name, account, address) and beneficiary info for transfers ≥ SGD 1,500",
            "File Suspicious Transaction Report (STR) to STRO within 1 business day if suspicious activity detected — do NOT tip off the customer",
            "Ongoing monitoring: flag transactions to high-risk jurisdictions, structuring patterns (multiple transfers just below thresholds), and sudden changes in remittance behavior",
        ],
        "business_impact": [
            "CDD/EDD processes add friction to customer onboarding — average 2-5 business days for enhanced checks",
            "Sanctions screening can delay or block legitimate transactions — need clear escalation and release process",
            "STR filing obligation is strict — failure to file can result in criminal prosecution of compliance officers",
            "Correspondent banking relationships increasingly require compliance attestations — impacts which corridors the bank can serve",
            "MAS penalties for AML failures are severe: SGD 1M+ fines, public censure, potential licence conditions or revocation",
        ],
        "risk_warnings": [
            "🔴 CRITICAL: Processing remittance to sanctioned country/entity without proper screening → sanctions violation, potential criminal liability",
            "🔴 HIGH: Customer sending frequent large remittances with no clear economic rationale and bank fails to file STR → MAS Notice 626 breach",
            "🔴 HIGH: Incomplete originator/beneficiary information on cross-border transfer → Travel Rule violation, correspondent bank may reject or report",
            "🟡 MEDIUM: Customer uses multiple accounts or branches to structure remittances below reporting threshold → structuring/smurfing red flag",
            "🟡 MEDIUM: Onboarding remittance-heavy customer (e.g. MSB) without adequate source-of-funds documentation → CDD failure",
        ],
    },
}

# Demo scenario: Bank selling financial products - compliance check
DEMO_SCENARIO = {
    "bank_name": "SouthStar Bank",
    "description": "A mid-sized digital bank in Singapore offering savings accounts, fixed deposits, wealth management products, and personal loans through both branch and digital channels.",
    "products": [
        {
            "name": "WealthGrow Structured Deposit",
            "type": "Specified Investment Product (SIP)",
            "risk_level": "Medium-High",
            "description": "A 3-year structured deposit linked to equity index performance, with partial principal protection.",
        },
        {
            "name": "SmartSave Fixed Deposit",
            "type": "Excluded Investment Product (EIP)",
            "risk_level": "Low",
            "description": "Standard fixed deposit with guaranteed returns, SDIC insured up to $100,000.",
        },
        {
            "name": "GlobalFund Portfolio",
            "type": "Specified Investment Product (SIP)",
            "risk_level": "High",
            "description": "A diversified fund investing in global equities, bonds, and alternative assets.",
        },
    ],
    "compliance_checks": [
        {
            "check_id": "CC-001",
            "scenario": "Selling WealthGrow Structured Deposit to a 72-year-old retiree",
            "customer_profile": {
                "age": 72,
                "occupation": "Retired teacher",
                "income": "SGD 2,500/month (pension)",
                "risk_appetite": "Conservative",
                "investment_experience": "Basic savings and FD only",
                "financial_goal": "Capital preservation for retirement",
            },
            "violations": [
                {
                    "regulation": "FAA-N16 (Suitability)",
                    "issue": "Product risk level (Medium-High) exceeds customer's risk appetite (Conservative)",
                    "severity": "HIGH",
                    "action": "DO NOT recommend this product. Suggest SmartSave Fixed Deposit instead.",
                },
                {
                    "regulation": "FAA-G11 Outcome 4",
                    "issue": "Advice not suitable for customer's circumstances - retiree with limited income should not be in illiquid 3-year product",
                    "severity": "HIGH",
                    "action": "Assess customer's liquidity needs before any recommendation.",
                },
                {
                    "regulation": "SFA04-N12",
                    "issue": "Customer unlikely to pass Customer Account Review (CAR) for SIP given limited investment experience",
                    "severity": "MEDIUM",
                    "action": "Conduct CAR assessment. If failed, product cannot be sold.",
                },
            ],
            "verdict": "BLOCKED",
            "verdict_reason": "Multiple suitability violations. This sale should not proceed.",
        },
        {
            "check_id": "CC-002",
            "scenario": "Selling GlobalFund Portfolio to a customer with outstanding debts",
            "customer_profile": {
                "age": 35,
                "occupation": "Sales manager",
                "income": "SGD 6,000/month",
                "risk_appetite": "Moderate",
                "investment_experience": "Has traded stocks before",
                "financial_goal": "Wealth growth",
                "debt_status": "SGD 80,000 outstanding personal loan + credit card debt of SGD 15,000",
            },
            "violations": [
                {
                    "regulation": "FAA-N16 (Suitability)",
                    "issue": "Customer's financial situation (high debt-to-income ratio) makes high-risk investment unsuitable",
                    "severity": "HIGH",
                    "action": "Assess total debt obligations vs disposable income before recommending investment products.",
                },
                {
                    "regulation": "FAA-G11 Outcome 2",
                    "issue": "High-risk fund not suitable for customer segment with significant debt obligations",
                    "severity": "MEDIUM",
                    "action": "Consider lower-risk alternatives or smaller investment amounts.",
                },
            ],
            "verdict": "WARNING",
            "verdict_reason": "Proceed with caution. Detailed financial assessment required. Consider lower-risk alternatives.",
        },
        {
            "check_id": "CC-003",
            "scenario": "Representative uses misleading sales tactics during product pitch",
            "customer_profile": {
                "age": 45,
                "occupation": "Business owner",
                "income": "SGD 15,000/month",
                "risk_appetite": "Aggressive",
                "investment_experience": "Experienced investor",
                "financial_goal": "High returns",
            },
            "violations": [
                {
                    "regulation": "FAA-G11 Outcome 3",
                    "issue": "Representative said 'guaranteed 8% returns' for a non-guaranteed structured product",
                    "severity": "CRITICAL",
                    "action": "Immediate remediation required. Correct misleading information. Retrain representative.",
                },
                {
                    "regulation": "FAA-G11 Outcome 1",
                    "issue": "Misleading claims erode customer trust and violate fair dealing principles",
                    "severity": "HIGH",
                    "action": "Review all sales materials. Ensure no misleading performance projections.",
                },
                {
                    "regulation": "SFA04-N12",
                    "issue": "Product Highlights Sheet must clearly state risks - verbal misrepresentation contradicts written disclosures",
                    "severity": "HIGH",
                    "action": "Ensure verbal representations are consistent with PHS. Record sales conversations for audit.",
                },
            ],
            "verdict": "BLOCKED",
            "verdict_reason": "Critical compliance violation. Sale must be halted. Mandatory representative retraining required.",
        },
    ],
}

# Simulated MAS website search results
MAS_SEARCH_RESULTS = [
    {
        "title": "Notice FAA-N16 on Recommendations on Investment Products",
        "url": "https://www.mas.gov.sg/regulation/notices/notice-faa-n16",
        "snippet": "This Notice sets out the requirements on the making of recommendations on investment products by licensed financial advisers and exempt financial advisers...",
        "date": "Last updated: 15 Jan 2025",
    },
    {
        "title": "Guidelines on Fair Dealing – Board and Senior Management Responsibilities",
        "url": "https://www.mas.gov.sg/regulation/guidelines/guidelines-on-fair-dealing---board-and-senior-management-responsibilities-for-delivering-fair-dealing-outcomes-to-customers",
        "snippet": "These Guidelines set out MAS' expectations on the delivery of fair dealing outcomes to customers by financial institutions...",
        "date": "Last updated: 3 Apr 2024",
    },
    {
        "title": "Notice SFA04-N12 on Sale of Investment Products",
        "url": "https://www.mas.gov.sg/regulation/notices/notice-sfa-04-n12",
        "snippet": "This Notice applies to capital markets services licence holders who deal in securities or trade in futures contracts...",
        "date": "Last updated: 28 Nov 2024",
    },
    {
        "title": "Notice on Prevention of Money Laundering and Countering Terrorism Financing",
        "url": "https://www.mas.gov.sg/regulation/notices/notice-626",
        "snippet": "This Notice sets out the requirements for financial institutions to prevent money laundering and terrorist financing...",
        "date": "Last updated: 1 Jul 2024",
    },
    {
        "title": "Guidelines on Outsourcing (MAS-G06)",
        "url": "https://www.mas.gov.sg/regulation/guidelines/guidelines-on-outsourcing-banks",
        "snippet": "These guidelines set out the risk management practices expected of financial institutions when they outsource...",
        "date": "Last updated: 5 Oct 2024",
    },
]

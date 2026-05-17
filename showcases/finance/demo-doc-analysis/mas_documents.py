"""
MAS Document Data — Source material for the document analysis pipeline demo.
Contains Sarah's persona, MAS FAA-N16 document versions, and bank product portfolio.
"""

# ── Sarah Chen's Persona ──
SARAH_PROFILE = {
    "name": "Sarah Chen",
    "title": "Compliance Analyst",
    "department": "Regulatory Affairs Division",
    "bank": "Horizon Bank Singapore (MAS-regulated)",
    "experience": "6 years in compliance",
    "trigger": (
        "MAS published a revised Notice FAA-N16 "
        "(Recommendations on Investment Products) over the weekend. "
        "47 pages. Manager wants an impact assessment by Wednesday."
    ),
    "pain_points": [
        "80% of time spent on manual document processing",
        "Reading PDFs, comparing versions side-by-side in Word",
        "Copy-pasting clauses into Excel spreadsheets",
        "Emailing department heads and waiting days for replies",
        "High risk of missing clauses buried in annexes",
    ],
}

# ── MAS FAA-N16 — Current (Old) Version ──
FAA_N16_CURRENT = {
    "notice_number": "FAA-N16",
    "title": "Notice on Recommendations on Investment Products",
    "issuing_authority": "Monetary Authority of Singapore",
    "effective_date": "1 January 2024",
    "version": "2024-01",
    "total_pages": 42,
    "sections": [
        {
            "section_number": "1",
            "heading": "Scope and Application",
            "text": (
                "1.1 This Notice is issued pursuant to section 58 of the Financial Advisers Act "
                "(Cap. 110) and applies to all licensed financial advisers and exempt financial "
                "advisers when making recommendations on investment products to customers.\n\n"
                "1.2 For the purposes of this Notice, 'investment products' shall include any "
                "securities, collective investment schemes, life policies, and structured deposits "
                "as defined under the Securities and Futures Act."
            ),
        },
        {
            "section_number": "2",
            "heading": "Definitions",
            "text": (
                "2.1 'Customer Knowledge Assessment' (CKA) means an assessment conducted to "
                "determine whether a customer has the relevant knowledge and experience to "
                "understand the risks of a specified investment product.\n\n"
                "2.2 'Selected Client' means a customer who is 62 years of age or older, or "
                "who does not possess the relevant educational qualifications as prescribed.\n\n"
                "2.3 'Complex Product' means a product whose terms, features and risks are "
                "not reasonably likely to be understood by a retail customer."
            ),
        },
        {
            "section_number": "3",
            "heading": "General Obligations",
            "text": (
                "3.1 A licensed financial adviser shall ensure that any recommendation made "
                "to a customer is suitable, having regard to the customer's investment objectives, "
                "financial situation, and particular needs.\n\n"
                "3.2 The financial adviser must have a reasonable basis for making any "
                "recommendation to the customer, based on information obtained through "
                "the fact-finding process.\n\n"
                "3.3 All recommendations shall be documented and retained for a minimum "
                "period of 5 years from the date of the recommendation."
            ),
        },
        {
            "section_number": "4",
            "heading": "Customer Knowledge Assessment (CKA)",
            "text": (
                "4.1 A financial adviser shall conduct a Customer Knowledge Assessment before "
                "recommending any specified investment product to a customer.\n\n"
                "4.1(a) The CKA must assess the customer's educational qualifications, "
                "investment experience, and work experience relevant to the product.\n\n"
                "4.2 Where a customer does not pass the CKA, the financial adviser must "
                "inform the customer that the product may not be suitable and provide "
                "additional risk disclosures.\n\n"
                "4.3 A financial adviser shall not recommend a complex product to a "
                "Selected Client unless the client passes the CKA and the adviser has "
                "conducted an enhanced suitability assessment."
            ),
        },
        {
            "section_number": "5",
            "heading": "Product Highlights Sheet (PHS)",
            "text": (
                "5.1 Before recommending any investment product, the financial adviser must "
                "provide the customer with a Product Highlights Sheet.\n\n"
                "5.2 The PHS must be in the prescribed format and shall clearly state the "
                "key features, risks, and costs of the product.\n\n"
                "5.3 For products with a risk rating of 'Medium-High' or above, the PHS "
                "must include an enhanced risk warning label."
            ),
        },
        {
            "section_number": "6",
            "heading": "Disclosure Requirements",
            "text": (
                "6.1 The financial adviser shall disclose to the customer all material "
                "information relating to the recommended product, including but not limited "
                "to the product's risk level, fees and charges, and any conflicts of interest.\n\n"
                "6.2 All fees and charges, including management fees, distribution fees, "
                "and early redemption penalties, must be clearly explained to the customer "
                "before any transaction is executed.\n\n"
                "6.3 The financial adviser shall inform the customer of any cooling-off period "
                "applicable to the product and the conditions for exercising the right to cancel."
            ),
        },
        {
            "section_number": "7",
            "heading": "Record-Keeping",
            "text": (
                "7.1 A financial adviser shall maintain proper records of all recommendations "
                "made, including the basis for each recommendation and the customer's "
                "acknowledgment.\n\n"
                "7.2 Records shall be kept for a minimum of 5 years from the date of "
                "the recommendation or the termination of the product, whichever is later.\n\n"
                "7.3 Records must be made available to MAS upon request within 3 business days."
            ),
        },
        {
            "section_number": "8",
            "heading": "Supervisory and Compliance Obligations",
            "text": (
                "8.1 A financial adviser shall establish and maintain adequate internal "
                "controls and procedures to ensure compliance with this Notice.\n\n"
                "8.2 The financial adviser must conduct periodic reviews of its compliance "
                "with this Notice, at a minimum on an annual basis.\n\n"
                "8.3 Any material breach of this Notice shall be reported to MAS within "
                "14 calendar days of discovery."
            ),
        },
    ],
}

# ── MAS FAA-N16 — Updated (New) Version ──
FAA_N16_UPDATED = {
    "notice_number": "FAA-N16",
    "title": "Notice on Recommendations on Investment Products (Revised)",
    "issuing_authority": "Monetary Authority of Singapore",
    "effective_date": "1 October 2026",
    "version": "2026-03",
    "total_pages": 47,
    "sections": [
        {
            "section_number": "1",
            "heading": "Scope and Application",
            "text": (
                "1.1 This Notice is issued pursuant to section 58 of the Financial Advisers Act "
                "(Cap. 110) and applies to all licensed financial advisers and exempt financial "
                "advisers when making recommendations on investment products to customers.\n\n"
                "1.2 For the purposes of this Notice, 'investment products' shall include any "
                "securities, collective investment schemes, life policies, and structured deposits "
                "as defined under the Securities and Futures Act.\n\n"
                "1.3 This Notice shall also apply to recommendations made through digital "
                "advisory channels, including robo-advisory platforms and AI-assisted "
                "recommendation systems."
            ),
        },
        {
            "section_number": "2",
            "heading": "Definitions",
            "text": (
                "2.1 'Customer Knowledge Assessment' (CKA) means an assessment conducted to "
                "determine whether a customer has the relevant knowledge and experience to "
                "understand the risks of a specified investment product.\n\n"
                "2.2 'Selected Client' means a customer who is 62 years of age or older, or "
                "who does not possess the relevant educational qualifications as prescribed.\n\n"
                "2.3 'Complex Product' means a product whose terms, features and risks are "
                "not reasonably likely to be understood by a retail customer.\n\n"
                "2.4 'Digital Advisory Channel' means any electronic platform or system "
                "through which investment recommendations are generated, communicated, "
                "or facilitated, whether fully automated or human-assisted."
            ),
        },
        {
            "section_number": "3",
            "heading": "General Obligations",
            "text": (
                "3.1 A licensed financial adviser shall ensure that any recommendation made "
                "to a customer is suitable, having regard to the customer's investment objectives, "
                "financial situation, and particular needs.\n\n"
                "3.2 The financial adviser must have a reasonable basis for making any "
                "recommendation to the customer, based on information obtained through "
                "the fact-finding process.\n\n"
                "3.3 All recommendations shall be documented and retained for a minimum "
                "period of 7 years from the date of the recommendation.\n\n"
                "3.4 Where a recommendation is made through a digital advisory channel, "
                "the financial adviser shall ensure that the algorithmic recommendation "
                "process is subject to the same suitability standards as human advisers."
            ),
        },
        {
            "section_number": "4",
            "heading": "Customer Knowledge Assessment (CKA)",
            "text": (
                "4.1 A financial adviser shall conduct a Customer Knowledge Assessment before "
                "recommending any specified investment product to a customer.\n\n"
                "4.1(a) The CKA must assess the customer's educational qualifications, "
                "investment experience, and work experience relevant to the product.\n\n"
                "4.1(b) For complex products, the CKA shall additionally assess the "
                "customer's understanding of derivative instruments, leverage, and "
                "structured payoff mechanisms.\n\n"
                "4.2 Where a customer does not pass the CKA, the financial adviser must "
                "inform the customer that the product may not be suitable and shall obtain "
                "written acknowledgment of enhanced risk disclosures from the customer.\n\n"
                "4.3 A financial adviser shall not recommend a complex product to a "
                "Selected Client unless the client passes the CKA and the adviser has "
                "conducted an enhanced suitability assessment.\n\n"
                "4.4 A financial adviser shall conduct a Product Knowledge Assessment (PKA) "
                "for all structured products, ensuring that the recommending representative "
                "has completed product-specific training and demonstrated competency in "
                "explaining the product's features, risks, and scenarios to customers."
            ),
        },
        {
            "section_number": "5",
            "heading": "Product Highlights Sheet (PHS)",
            "text": (
                "5.1 Before recommending any investment product, the financial adviser must "
                "provide the customer with a Product Highlights Sheet.\n\n"
                "5.2 The PHS must be in the prescribed format and shall clearly state the "
                "key features, risks, and costs of the product, including a standardized "
                "risk indicator using the prescribed color-coded label system (green, amber, red).\n\n"
                "5.3 For products with a risk rating of 'Medium-High' or above, the PHS "
                "must include an enhanced risk warning label.\n\n"
                "5.4 For digital advisory channels, the PHS must be presented in an "
                "interactive format that requires the customer to acknowledge each key "
                "risk before proceeding."
            ),
        },
        {
            "section_number": "6",
            "heading": "Disclosure Requirements",
            "text": (
                "6.1 The financial adviser shall disclose to the customer all material "
                "information relating to the recommended product, including but not limited "
                "to the product's risk level, fees and charges, and any conflicts of interest.\n\n"
                "6.2 All fees and charges, including management fees, distribution fees, "
                "and early redemption penalties, must be clearly explained to the customer "
                "before any transaction is executed.\n\n"
                "6.3 The financial adviser shall inform the customer of the cooling-off period "
                "of not less than 7 calendar days applicable to the product and the conditions "
                "for exercising the right to cancel, including that cancellation may be "
                "exercised unconditionally during this period.\n\n"
                "6.4 For structured products, the financial adviser shall provide scenario "
                "analysis showing potential outcomes under adverse, base, and favorable "
                "market conditions."
            ),
        },
        {
            "section_number": "7",
            "heading": "Record-Keeping",
            "text": (
                "7.1 A financial adviser shall maintain proper records of all recommendations "
                "made, including the basis for each recommendation and the customer's "
                "acknowledgment.\n\n"
                "7.2 Records shall be kept for a minimum of 7 years from the date of "
                "the recommendation or the termination of the product, whichever is later.\n\n"
                "7.3 Records must be made available to MAS upon request within 3 business days.\n\n"
                "7.4 For recommendations made through digital advisory channels, a complete "
                "audit trail of the algorithmic decision process shall be maintained, "
                "including model inputs, intermediate calculations, and the final recommendation."
            ),
        },
        {
            "section_number": "8",
            "heading": "Supervisory and Compliance Obligations",
            "text": (
                "8.1 A financial adviser shall establish and maintain adequate internal "
                "controls and procedures to ensure compliance with this Notice.\n\n"
                "8.2 The financial adviser must conduct periodic reviews of its compliance "
                "with this Notice, at a minimum on a semi-annual basis.\n\n"
                "8.3 Any material breach of this Notice shall be reported to MAS within "
                "7 calendar days of discovery.\n\n"
                "8.4 The financial adviser shall appoint a designated compliance officer "
                "responsible for overseeing compliance with this Notice and for liaising "
                "with MAS on all regulatory matters."
            ),
        },
        {
            "section_number": "Annex A",
            "heading": "Prescribed Format for Product Highlights Sheet",
            "text": (
                "A.1 The Product Highlights Sheet shall follow the standardized template "
                "provided by MAS, consisting of the following sections:\n\n"
                "A.2 Section 1: Product Summary (maximum 1 page)\n"
                "A.3 Section 2: Key Risks (maximum 1 page)\n"
                "A.4 Section 3: Fees and Charges (maximum 1 page)\n"
                "A.5 Section 4: Key Questions to Ask\n\n"
                "A.6 The total length of the PHS shall not exceed 4 pages."
            ),
        },
        {
            "section_number": "Annex B",
            "heading": "Product Knowledge Assessment (PKA) Requirements",
            "text": (
                "B.1 The Product Knowledge Assessment shall be conducted for each "
                "representative before they are authorized to recommend structured products.\n\n"
                "B.2 The PKA shall assess the representative's understanding of:\n"
                "  (a) the product's structure and payoff mechanism;\n"
                "  (b) key risk factors including market risk, credit risk, and liquidity risk;\n"
                "  (c) scenarios under which the customer may lose part or all of the "
                "invested capital;\n"
                "  (d) the product's fee structure and impact on returns.\n\n"
                "B.3 Representatives must achieve a minimum score of 80% on the PKA "
                "before being authorized to recommend the relevant product.\n\n"
                "B.4 The PKA must be renewed annually, and representatives who fail "
                "to renew shall have their authorization suspended until reassessment."
            ),
        },
        {
            "section_number": "Annex C",
            "heading": "Digital Advisory Channel Requirements",
            "text": (
                "C.1 Financial advisers operating digital advisory channels shall ensure "
                "that the recommendation algorithm is validated by an independent party "
                "at least annually.\n\n"
                "C.2 The digital advisory channel must include clear disclosures that "
                "recommendations are generated by an algorithm and may not account for "
                "all individual circumstances.\n\n"
                "C.3 Customers using digital advisory channels shall have access to a "
                "human adviser upon request at any point during the recommendation process.\n\n"
                "C.4 The financial adviser shall maintain records of all algorithmic "
                "recommendations, including model version, input parameters, and output "
                "recommendations, for a minimum period of 7 years."
            ),
        },
    ],
}

# ── Bank Product Portfolio ──
BANK_PRODUCTS = [
    {
        "name": "Enhanced Yield Structured Deposit",
        "type": "Structured Deposit",
        "department": "Wealth Management",
        "risk_level": "Medium-High",
        "description": "A principal-protected deposit with returns linked to equity indices.",
        "current_status": "Active — 1,200 accounts",
        "annual_revenue": "S$2.4M",
        "regulatory_profile": {
            "product_classification": "Specified Investment Product — Complex (Structured Deposit)",
            "mas_product_code": "SIP-SD-003",
            "risk_features": [
                "Returns linked to SGX Straits Times Index via embedded call option",
                "Payoff depends on derivative (equity index option) performance",
                "Structured payoff: principal protected, but coupon at risk",
                "12-month lock-in with early redemption penalty of 1.5%",
            ],
            "current_documents": [
                "Product Highlights Sheet v3.2 (last updated Jan 2024)",
                "CKA Form A-12 (standard — no derivatives assessment)",
                "Term Sheet Template TS-EYSD-2024",
                "Sales Script SS-WM-041",
            ],
            "prospectus_excerpt": (
                "The Enhanced Yield Structured Deposit provides principal protection at maturity "
                "with variable coupon payments linked to the performance of the SGX Straits Times "
                "Index. The coupon is determined by an embedded equity index call option. If the "
                "index closes above the strike level on the observation dates, the investor receives "
                "an enhanced coupon of 4.8% p.a.; otherwise, a base coupon of 0.5% p.a. applies. "
                "The principal is guaranteed only if held to maturity; early redemption is subject "
                "to a penalty of 1.5% of the notional amount."
            ),
            "regulatory_triggers": [
                "Classified as 'Complex Product' under §2.3 — derivative-linked returns",
                "Contains embedded derivative — triggers enhanced CKA under §4.1(b)",
                "Structured payoff mechanism — requires PKA under §4.4",
                "Structured product — requires scenario analysis under §6.4",
            ],
        },
    },
    {
        "name": "Global Equity OTC Derivative",
        "type": "OTC Derivative",
        "department": "Treasury & Markets",
        "risk_level": "High",
        "description": "Over-the-counter derivative products linked to global equity markets.",
        "current_status": "Active — 340 accounts",
        "annual_revenue": "S$5.1M",
        "regulatory_profile": {
            "product_classification": "Specified Investment Product — Complex (OTC Derivative)",
            "mas_product_code": "SIP-OTC-017",
            "risk_features": [
                "Bilateral OTC contract — counterparty credit risk",
                "Leveraged exposure (up to 5x notional)",
                "Mark-to-market margin calls; potential for losses exceeding initial margin",
                "Settlement risk on physically-delivered contracts",
            ],
            "current_documents": [
                "Product Highlights Sheet v2.8 (last updated Sep 2023)",
                "CKA Form A-12 (standard — no leverage/derivatives assessment)",
                "ISDA Master Agreement template",
                "Risk Disclosure Statement RDS-OTC-2023",
                "Sales Script SS-TM-019",
            ],
            "prospectus_excerpt": (
                "Global Equity OTC Derivatives are bilateral contracts between the Bank and the "
                "customer, with payoffs linked to the performance of specified global equity indices "
                "or single stocks. Products include equity swaps, options, and structured forwards. "
                "Leverage of up to 5x the notional amount may be employed, meaning potential losses "
                "can exceed the initial margin deposited. Customers are subject to daily mark-to-market "
                "margin requirements and must maintain a minimum margin ratio of 20%."
            ),
            "regulatory_triggers": [
                "Classified as 'Complex Product' under §2.3 — leveraged derivative",
                "Leverage and derivative exposure — triggers enhanced CKA under §4.1(b)",
                "Customer may lose more than invested capital — requires PKA under §4.4",
                "Structured product — requires scenario analysis under §6.4",
                "OTC nature — heightened record-keeping requirements under §7.2/§7.4",
            ],
        },
    },
    {
        "name": "Asia Pacific Growth Fund",
        "type": "Collective Investment Scheme",
        "department": "Retail Banking",
        "risk_level": "Medium",
        "description": "A unit trust investing in Asia Pacific equities for long-term growth.",
        "current_status": "Active — 4,500 accounts",
        "annual_revenue": "S$3.2M",
        "regulatory_profile": {
            "product_classification": "Specified Investment Product — Non-Complex (CIS)",
            "mas_product_code": "SIP-CIS-042",
            "risk_features": [
                "Equity market risk — Asia Pacific emerging and developed markets",
                "Currency risk (multi-currency portfolio)",
                "No leverage; no embedded derivatives",
                "Daily NAV-based pricing; T+3 redemption",
            ],
            "current_documents": [
                "Product Highlights Sheet v4.1 (last updated Mar 2024)",
                "CKA Form B-05 (standard CIS assessment)",
                "Fund Prospectus (142 pages, registered with MAS)",
                "Factsheet — updated monthly",
            ],
            "prospectus_excerpt": (
                "The Asia Pacific Growth Fund is an open-ended unit trust constituted in Singapore, "
                "investing primarily in equities of companies listed in Asia Pacific markets including "
                "Singapore, Hong Kong, Japan, Australia, and selected ASEAN exchanges. The fund aims "
                "to achieve long-term capital appreciation. It does not use leverage or invest in "
                "derivative instruments. The management fee is 1.5% p.a. and the initial sales charge "
                "is up to 5%. Redemption proceeds are typically paid within 3 business days."
            ),
            "regulatory_triggers": [
                "Non-complex CIS — standard CKA applies under §4.1",
                "CKA failure now requires written acknowledgment under §4.2 (was verbal)",
                "PHS format update required for color-coded risk labels under §5.2",
                "Record retention extension to 7 years under §7.2",
            ],
        },
    },
    {
        "name": "Term Life Insurance (Investment-Linked)",
        "type": "Life Policy (ILP)",
        "department": "Insurance",
        "risk_level": "Medium",
        "description": "Investment-linked life insurance policy with multiple sub-funds.",
        "current_status": "Active — 2,800 policies",
        "annual_revenue": "S$1.8M",
        "regulatory_profile": {
            "product_classification": "Specified Investment Product — Life Policy (ILP)",
            "mas_product_code": "SIP-ILP-008",
            "risk_features": [
                "Investment returns depend on chosen sub-fund performance",
                "Insurance charges and mortality charges reduce investment value",
                "Surrender charges apply in first 3 years (up to 40% of premiums)",
                "Sub-funds include equity, bond, and balanced options",
            ],
            "current_documents": [
                "Product Highlights Sheet v3.5 (last updated Feb 2024)",
                "CKA Form C-02 (ILP-specific assessment)",
                "Product Summary (BI table — 10/20/30 year projections)",
                "Policy Document template PD-ILP-2024",
                "Sales Script SS-INS-012",
            ],
            "prospectus_excerpt": (
                "The Term Life Insurance (Investment-Linked) policy provides life coverage of up "
                "to S$500,000 with an investment component allocated across customer-selected "
                "sub-funds. Available sub-funds include: Singapore Equity Fund, Global Bond Fund, "
                "and Balanced Growth Fund. Insurance and mortality charges are deducted monthly "
                "from the policy's unit balance. Early surrender within the first 3 years incurs "
                "charges of up to 40% of total premiums paid. A free-look period of 14 days applies "
                "from the date of policy issuance."
            ),
            "regulatory_triggers": [
                "ILP classified as specified investment product — standard CKA under §4.1",
                "Cooling-off period now explicitly 7 days minimum (§6.3) — current free-look is 14 days, compliant",
                "PHS requires color-coded risk labels under §5.2",
                "Record retention extension to 7 years under §7.2",
            ],
        },
    },
    {
        "name": "Fixed Deposit (12-month)",
        "type": "Deposit",
        "department": "Retail Banking",
        "risk_level": "Low",
        "description": "Standard fixed deposit with guaranteed interest rate.",
        "current_status": "Active — 15,000 accounts",
        "annual_revenue": "S$0.9M",
        "regulatory_profile": {
            "product_classification": "Non-Specified Investment Product (Deposit)",
            "mas_product_code": "N/A (not SIP)",
            "risk_features": [
                "Principal fully guaranteed by the Bank",
                "Fixed interest rate for the term (no market risk)",
                "Protected under SDIC deposit insurance up to S$100,000",
                "Early withdrawal penalty: forfeiture of accrued interest",
            ],
            "current_documents": [
                "Terms & Conditions — Fixed Deposit (v2024-01)",
                "Interest Rate Schedule (updated quarterly)",
            ],
            "prospectus_excerpt": (
                "The 12-Month Fixed Deposit offers a guaranteed interest rate for the deposit term, "
                "with principal fully protected by the Bank. The deposit is covered under the "
                "Singapore Deposit Insurance Corporation (SDIC) scheme up to S$100,000 per depositor. "
                "No market risk, currency risk, or credit risk beyond the Bank's own creditworthiness. "
                "Early withdrawal results in forfeiture of accrued interest for the broken period."
            ),
            "regulatory_triggers": [
                "Not a specified investment product — most FAA-N16 obligations do not apply",
                "General suitability and record-keeping obligations still apply (§3.1, §7.2)",
                "Minimal impact — only record retention extension to 7 years is relevant",
            ],
        },
    },
]

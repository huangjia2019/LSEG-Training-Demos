# Banking Compliance Scenarios — MAS-Regulated Products

> 3 real-world banking business scenarios for the MAS Compliance Analyst Agent demo.
> Each scenario covers: what the business does, which MAS regulations apply, what the compliance team must enforce, and what can go wrong.

---

## Scenario 1: Selling Unit Trusts / Mutual Funds

### Business Context
A bank's wealth management team recommends unit trust funds (equity, bond, balanced) to retail customers. Funds are classified as **Specified Investment Products (SIP)** under MAS rules, which triggers a higher regulatory bar than simple deposits.

### Applicable MAS Regulations

| Regulation | Full Title | Link |
|-----------|-----------|------|
| **FAA-N16** | Notice on Recommendations on Investment Products | https://www.mas.gov.sg/regulation/notices/notice-faa-n16 |
| **SFA04-N12** | Notice on Sale of Investment Products | https://www.mas.gov.sg/regulation/notices/notice-sfa-04-n12 |
| **FSG-G04** | Guidelines on Fair Dealing | https://www.mas.gov.sg/regulation/guidelines/guidelines-on-fair-dealing---board-and-senior-management-responsibilities-for-delivering-fair-dealing-outcomes-to-customers |

### Compliance Checklist
1. **Customer Knowledge Assessment (CKA)** — Customer must demonstrate understanding of fund risks before purchase
2. **Customer Account Review (CAR)** — Assess financial situation, investment experience, and objectives for SIP funds
3. **Product Highlights Sheet (PHS)** — Provide before or at point of sale; must include fund strategy, fees, risks, past performance
4. **Basis of Recommendation** — Document in writing why this fund suits this customer; retain records for 5+ years
5. **Rep Certification** — Representative must hold CMFAS Module 5/9/9A

### Business Impact
- Sales cycle adds ~15-20 mins per customer for CKA + CAR
- Customers who fail CAR cannot be sold SIP funds
- All fund marketing materials require compliance review
- Non-compliance: fines up to SGD 1M, FA licence revocation

### Key Risk Scenarios
- Recommending high-risk equity funds to elderly/conservative customers without suitability justification
- Selling SIP funds without completing CAR
- Rep verbally promises "guaranteed returns" on a non-guaranteed fund
- Churning (frequent fund switching to generate commissions)

---

## Scenario 2: Distributing Investment-Linked Insurance Policies (ILPs)

### Business Context
The bank's bancassurance channel distributes ILPs — insurance policies where premiums are invested in sub-funds. ILPs combine insurance coverage with investment risk, making them subject to **both** insurance and investment product regulations.

### Applicable MAS Regulations

| Regulation | Full Title | Link |
|-----------|-----------|------|
| **FAA-N16** | Notice on Recommendations on Investment Products | https://www.mas.gov.sg/regulation/notices/notice-faa-n16 |
| **FSG-G04** | Guidelines on Fair Dealing | https://www.mas.gov.sg/regulation/guidelines/guidelines-on-fair-dealing---board-and-senior-management-responsibilities-for-delivering-fair-dealing-outcomes-to-customers |
| **MAS Notice 307** | Requirements for Insurance Intermediaries | https://www.mas.gov.sg/regulation/notices/notice-307 |

### Compliance Checklist
1. **Financial Needs Analysis (FNA)** — Assess both insurance protection gap AND investment needs
2. **Benefit Illustration (BI)** — Show projected returns at 3.25% and 4.75% rates
3. **Fee Disclosure** — Distribution cost, fund management charges, insurance charges, surrender penalties
4. **14-Day Free-Look Period** — Customer can cancel within 14 days of receiving policy docs
5. **Replacement Policy Form** — If switching from existing policy, justify why new policy is better

### Business Impact
- Dual licensing required for reps (CMFAS + insurance certs)
- FNA adds ~30 mins to each sales interaction
- 14-day free-look delays revenue recognition
- Past MAS enforcement: SGD 100K–1M fines for ILP mis-selling

### Key Risk Scenarios
- Selling ILPs as pure investment without adequate insurance analysis
- Not disclosing 5-year surrender penalty — customer discovers lock-in too late
- Replacing customer's whole-life policy with ILP without proper justification
- Targeting elderly customers for 15-25 year ILPs exceeding planning horizon

---

## Scenario 3: Cross-Border Remittance / Wire Transfers (AML/CFT)

### Business Context
The bank processes cross-border remittances for retail and SME customers — wire transfers, online remittances, and correspondent banking payments. This is the bank's **highest AML/CFT risk** area due to exposure to money laundering, sanctions, and terrorist financing risks.

### Applicable MAS Regulations

| Regulation | Full Title | Link |
|-----------|-----------|------|
| **MAS Notice 626** | Prevention of Money Laundering and CFT — Banks | https://www.mas.gov.sg/regulation/notices/notice-626 |
| **MAS Notice PSN02** | Prevention of Money Laundering and CFT — Payment Service Providers | https://www.mas.gov.sg/regulation/notices/psn02 |
| **FATF Travel Rule** | Cross-Border Wire Transfer Requirements (via Notice 626) | https://www.mas.gov.sg/regulation/notices/notice-626 |

### Compliance Checklist
1. **Customer Due Diligence (CDD)** — Verify identity (NRIC/passport), proof of address, source of funds at onboarding
2. **Enhanced Due Diligence (EDD)** — For PEPs, high-risk jurisdictions (FATF grey/black list), unusual patterns
3. **Sanctions Screening** — Screen all parties (sender, beneficiary, intermediary banks) against UN/OFAC/MAS lists
4. **Travel Rule** — Include full originator + beneficiary info for transfers >= SGD 1,500
5. **STR Filing** — File Suspicious Transaction Report to STRO within 1 business day; do NOT tip off customer
6. **Ongoing Monitoring** — Flag high-risk corridor transfers, structuring patterns, sudden behavior changes

### Business Impact
- CDD/EDD adds 2-5 business days friction to customer onboarding
- Sanctions screening can delay/block legitimate transactions
- STR filing is mandatory — failure can lead to criminal prosecution of compliance officers
- Correspondent banking requires compliance attestations — limits corridor access
- MAS AML penalties: SGD 1M+ fines, public censure, licence conditions/revocation

### Key Risk Scenarios
- Processing remittance to sanctioned country/entity without screening — **criminal liability**
- Failing to file STR for suspicious large remittances with no economic rationale
- Incomplete originator/beneficiary info on cross-border transfer (Travel Rule violation)
- Customer structures remittances below threshold across multiple accounts/branches
- Onboarding remittance-heavy customer without source-of-funds documentation

---

## Summary: Why These 3 Scenarios?

| Scenario | Revenue Driver | Regulatory Risk | AI Agent Value |
|----------|---------------|----------------|----------------|
| **Unit Trust Sales** | Wealth management fees | Product suitability, mis-selling | Auto-CKA/CAR, suitability checks, PHS generation |
| **ILP Distribution** | Bancassurance commissions | Disclosure, needs analysis | FNA automation, fee transparency, replacement analysis |
| **Remittance / AML** | Transaction fees | Money laundering, sanctions | Real-time screening, STR drafting, pattern detection |

These 3 scenarios represent the core compliance challenges for a Singapore bank selling financial products. Each touches different MAS regulatory frameworks and offers clear AI automation opportunities for the Agent demo.

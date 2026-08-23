# PolicyPilot

PolicyPilot is a policy-driven expense approval workspace for the Supervity FDE technical screening assessment.

## Selected problem

**Problem 4 — Policy-Driven Approval Agent**

The application accepts plain-English business rules, converts them into structured policy settings, evaluates a batch of synthetic expense claims, and produces APPROVE, REVIEW, ESCALATE, or REJECT decisions with a traceable reason for each claim.

## What is included

- Plain-English configurable policy input
- Batch processing of expense claims
- APPROVE / REVIEW / ESCALATE / REJECT decisions
- Applied-rule and reason for every decision
- Non-technical policy editing from the sidebar
- Default REVIEW when no rule matches
- Audit trail
- Synthetic assessment data
- Clean Streamlit dashboard

## Tech stack

- Python
- Streamlit
- Pandas
- Regex-based policy parser
- Deterministic rule engine

The parser and decision engine are intentionally separate. The parser turns the supported plain-English policy format into structured settings. The rule engine makes the final decision deterministically, which keeps the workflow reproducible and easy to explain.

## Project structure

```text
PolicyPilot/
├── app.py
├── rule_parser.py
├── rule_engine.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
└── data/
    └── expenses.csv
```

## Run locally

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Demo policy

```text
Auto-approve expenses under $500 for Sales, escalate expenses above $2,000, and reject expenses above $5,000.
```

## Decision flow

```text
Plain-English Policy
        ↓
Policy Parser
        ↓
Structured Rules
        ↓
Deterministic Rule Engine
        ↓
Decision + Applied Rule + Reason
        ↓
Audit Trail
```

## Assumptions

- USD is used for the synthetic dataset.
- Claims without a matching rule remain REVIEW.
- Rejection has priority over escalation, and escalation has priority over department-specific auto-approval.
- No real customer data is used.

## Demo flow

1. Enter a business policy in the left sidebar.
2. Click **Parse policy**.
3. Open **Structured policy** to show the parsed values.
4. Click **Evaluate claims**.
5. Select an escalated or rejected claim.
6. Explain the applied rule and reason.
7. Change a threshold and parse again to demonstrate configurability.
8. Open the audit trail.

## Suggested five-minute walkthrough

- 0:00–1:30 — problem, architecture, and why the decision engine is deterministic
- 1:30–3:30 — live policy parsing and batch evaluation
- 3:30–4:20 — explain one escalated or rejected claim
- 4:20–5:00 — change a policy threshold, re-run, and show the decision changes

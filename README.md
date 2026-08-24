# 🛡️ PolicyPilot

### Policy-driven expense approval workspace

PolicyPilot is a lightweight Streamlit application for evaluating employee expense claims against configurable business policies.

Instead of hardcoding approval logic into the application, the user writes the policy in plain English. The policy parser converts that input into structured rules, and a deterministic rule engine evaluates each claim and records the resulting decision, rationale, and applied rule.

> **Built for the Supervity FDE assessment — Problem: Configurable Rules / Policy-Driven Decisioning**

---

## ✨ What PolicyPilot Does

PolicyPilot supports a simple end-to-end workflow:

**Write Policy → Parse Rules → Validate Policy → Evaluate Claims → Explain Decision → Audit**

# 🎥 Suggested Demo Flow

video drive link :-   https://drive.google.com/drive/folders/1c8lqly7Es80l0ZY5tdvP25QfUoy76CcS


### Core capabilities

- 📝 **Plain-English policy configuration**
- ⚙️ **Structured rule parsing**
- 🔎 **Policy validation**
- 🔴 **Conflicting threshold detection**
- ⚠️ **Ambiguous / boundary warnings**
- 📊 **Batch expense evaluation**
- ✅ **APPROVE / REVIEW / ESCALATE / REJECT decisions**
- 💬 **Decision rationale for every claim**
- 🔗 **Applied-rule traceability**
- 📋 **Audit-style decision inspection**
- 📤 **CSV upload support**
- 🎨 **Professional Streamlit dashboard**

The decision engine is deterministic and traceable: each claim receives a decision, reason, and applied rule. The existing engine prioritizes rejection, escalation, department-specific auto-approval, and finally review when no rule matches.

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │      User / HR       │
                    │   Business Manager   │
                    └──────────┬───────────┘
                               │
                               │ Plain-English policy
                               ▼
                    ┌──────────────────────┐
                    │    Policy Parser     │
                    │   rule_parser.py     │
                    └──────────┬───────────┘
                               │
                               │ Structured rules
                               ▼
                    ┌──────────────────────┐
                    │  Policy Validation   │
                    │  app.py validation   │
                    └──────────┬───────────┘
                               │
                               │ Valid policy
                               ▼
┌─────────────────┐   ┌──────────────────────┐
│ Expense CSV     │──▶│    Rule Engine       │
│ data/expenses   │   │    rule_engine.py    │
└─────────────────┘   └──────────┬───────────┘
                                 │
                                 │ Decision + Rule + Reason
                                 ▼
                    ┌──────────────────────┐
                    │    PolicyPilot UI    │
                    │ Dashboard / Audit    │
                    └──────────────────────┘
```

### Design principle

The application keeps **policy interpretation** separate from **decision execution**.

- `rule_parser.py` handles policy text → structured configuration.
- `rule_engine.py` handles structured configuration → deterministic claim decisions.
- `app.py` provides the user interface, validation, workflow, and traceability.

This separation keeps the actual business decision logic predictable and auditable.

---

## 📁 Project Structure

```text
PolicyPilot/
│
├── app.py
│       Main Streamlit application and UI
│
├── rule_parser.py
│       Converts supported plain-English policy wording
│       into structured rule configuration
│
├── rule_engine.py
│       Deterministic policy evaluation engine
│
├── requirements.txt
│       Python dependencies
│
├── README.md
│       Project documentation
│
├── data/
│   └── expenses.csv
│       Sample synthetic expense claims
│
├── .streamlit/
│   └── config.toml
│       Streamlit configuration
│
└── .gitignore
        Local environment / secret exclusions
```

---

# 🚀 Getting Started

## 1. Download the project

### Option A — Download ZIP

Open the GitHub repository:

**https://github.com/NikhilrajuV/PolicyPilot**

Then:

```text
Code
  ↓
Download ZIP
  ↓
Extract the ZIP
  ↓
Open the PolicyPilot folder
```

### Option B — Clone with Git

```bash
git clone https://github.com/NikhilrajuV/PolicyPilot.git
cd PolicyPilot
```

---

## 2. Create a virtual environment

### Windows PowerShell

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell shows:

```text
(venv) PS E:\...\PolicyPilot>
```

the virtual environment is active.

### Windows CMD

```cmd
venv\Scripts\activate
```

---

## 3. Install dependencies

Run:

```powershell
python -m pip install --upgrade pip
```

Then:

```powershell
pip install -r requirements.txt
```

> If your machine already has a working virtual environment, you can directly run the requirements installation.

---

## 4. Verify the project files

Before running the application, confirm that the project contains:

```text
app.py
rule_parser.py
rule_engine.py
requirements.txt
README.md
data/
    expenses.csv
```

The sample CSV must contain these columns:

```text
claim_id
employee
department
category
amount
description
```

---

# ▶️ Run the Application

From the project directory:

```powershell
python -m streamlit run app.py
```

Streamlit will print a local address, normally similar to:

```text
http://localhost:8501
```

Open that address in your browser.

### Stop the application

In the terminal running Streamlit:

```text
Ctrl + C
```

---

# 🧭 How to Use PolicyPilot

## Step 1 — Define the policy

Open **Policy** and enter a business rule in plain English.

Example:

```text
Auto-approve expenses under $500 for Sales,
escalate expenses above $2,000,
and reject expenses above $5,000.
```

---

## Step 2 — Parse the policy

Click:

```text
Parse / Validate / Activate
```

The parser creates structured values such as:

```text
Auto-approval department : Sales
Auto-approval limit      : $500
Escalation threshold     : $2,000
Rejection threshold      : $5,000
```

---

# 🔎 Policy Validation

Before claims are evaluated, PolicyPilot checks the policy configuration.

### 1. Conflicting thresholds

The expected ordering is:

```text
Auto-approval threshold
        <
Escalation threshold
        <
Rejection threshold
```

For example, this is invalid:

```text
Auto-approve below $2,000
Escalate above $1,000
Reject above $5,000
```

because the escalation threshold is lower than the auto-approval threshold.

---

### 2. Ambiguous wording

The application warns when the policy does not clearly communicate boundary wording such as:

```text
under / below
above / over
```

This helps the user review the intended behavior before evaluating claims.

---

### 3. Boundary values

Threshold boundaries should be treated explicitly.

For example:

```text
below $500
```

means an amount of:

```text
$499.99  → eligible
$500.00  → not below $500
```

Similarly, an:

```text
above $2,000
```

condition does not mean `$2,000` itself is above the threshold.

PolicyPilot surfaces these boundary considerations so the business rule can be reviewed before execution.

---

# ⚖️ Rule Priority

The decision engine uses a deterministic priority order:

```text
1. REJECT
2. ESCALATE
3. AUTO-APPROVE
4. REVIEW
```

### REJECT

If the amount exceeds the rejection threshold:

```text
REJECT
```

### ESCALATE

Otherwise, if the amount exceeds the escalation threshold:

```text
ESCALATE
```

### AUTO-APPROVE

Otherwise, if the employee's department matches the configured department and the amount is below the approval threshold:

```text
APPROVE
```

### REVIEW

If no rule matches:

```text
REVIEW
```

This gives every claim a deterministic outcome.

---

# 📊 Sample Policy

The included sample policy is:

```text
Auto-approve expenses under $500 for Sales,
escalate expenses above $2,000,
and reject expenses above $5,000.
```

The sample data demonstrates all four decision types:

| Decision | Example |
|---|---|
| APPROVE | Sales expense below $500 |
| REVIEW | Expense that matches no specific rule |
| ESCALATE | Expense above $2,000 |
| REJECT | Expense above $5,000 |

---

# 🧪 Example Evaluation

A claim such as:

```text
Claim       : EXP001
Employee    : Ravi
Department  : Sales
Amount      : $350
```

matches the Sales auto-approval rule.

Result:

```text
Decision    : APPROVE
```

The application also records the applied policy and a human-readable rationale.

For a high-value claim such as:

```text
Amount      : $2,500
```

the escalation rule takes priority:

```text
Decision    : ESCALATE
```

For:

```text
Amount      : $6,000
```

the rejection rule applies:

```text
Decision    : REJECT
```

---

# 📤 Upload Your Own Data

PolicyPilot supports CSV uploads.

Your CSV should contain:

```text
claim_id,employee,department,category,amount,description
```

Example:

```csv
claim_id,employee,department,category,amount,description
EXP101,Asha,Sales,Travel,420,Client meeting
EXP102,Rahul,Finance,Equipment,3200,Monitor purchase
EXP103,Meera,HR,Training,900,Training program
```

Upload the file through the application's data/claims interface and evaluate the batch against the active policy.

---

# 🔍 Decision Traceability

Every evaluated claim contains:

```text
Claim ID
Employee
Department
Category
Amount
Decision
Applied Rule
Reason
```

This makes it possible to answer:

> "Why did the system make this decision?"

For example:

```text
Decision:
ESCALATE

Applied rule:
Escalate expenses above $2,000

Reason:
Amount $2,500 exceeds the escalation threshold of $2,000.
```

---

# 🧑‍💼 Non-Technical User Workflow

A business user does not need to edit Python code.

They can:

```text
1. Open Policy
       ↓
2. Write the business rule in plain English
       ↓
3. Parse and validate
       ↓
4. Review thresholds / warnings
       ↓
5. Evaluate the same claim batch
       ↓
6. Inspect decisions and rationales
```

For example, changing:

```text
under $500
```

to:

```text
under $750
```

changes the structured policy configuration without modifying the decision-engine source code.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| Pandas | CSV/data processing |
| Rule parser | Plain-English policy interpretation |
| Rule engine | Deterministic decision execution |
| CSV | Sample/mock claim storage |

---

# 🔐 Security & Repository Hygiene

The repository intentionally excludes local development files such as:

```text
venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
```

Do **not** commit API keys, passwords, tokens, or private credentials.

---

# 🧩 Troubleshooting

## Streamlit is not recognized

Use:

```powershell
python -m streamlit run app.py
```

instead of:

```powershell
streamlit run app.py
```

---

## Browser shows an old UI

Stop the current Streamlit process:

```text
Ctrl + C
```

Then restart:

```powershell
python -m streamlit run app.py
```

Open the fresh URL printed by Streamlit.

---

## `ModuleNotFoundError`

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Then reinstall:

```powershell
pip install -r requirements.txt
```

---

## CSV column error

Make sure the CSV contains:

```text
claim_id
employee
department
category
amount
description
```

---



# 📌 Assessment Alignment

PolicyPilot addresses the core configurable-rules requirements:

- Plain-English rules are supplied as configuration.
- Rules are applied to a batch of sample claims.
- Every claim receives a decision and rationale.
- A non-technical user can edit the policy through the UI.
- Decisions are traceable to the rule that produced them.
- Policy conflicts and boundary conditions are surfaced for review.

---

# 📄 License

This project is intended as an assessment/demo application and uses synthetic sample data.

---

## 👤 Project

**PolicyPilot**

GitHub:

https://github.com/NikhilrajuV/PolicyPilot

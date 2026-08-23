from pathlib import Path
import re

import pandas as pd
import streamlit as st

from rule_engine import apply_rules
from rule_parser import parse_policy


# ============================================================
# PAGE
# ============================================================
st.set_page_config(
    page_title="PolicyPilot | Approval Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL THEME
# ============================================================
st.markdown(
    """
<style>
:root {
    --bg: #07111F;
    --bg-soft: #0B1728;
    --panel: #0F1D31;
    --panel-2: #13233A;
    --border: rgba(148,163,184,.14);
    --text: #F8FAFC;
    --muted: #8EA0B8;
    --blue: #4F8CFF;
    --blue-soft: #75A7FF;
    --cyan: #35C5D8;
    --green: #35D39A;
    --yellow: #F4C95D;
    --orange: #F59E5B;
    --red: #F06A78;
}

.stApp {
    background:
        radial-gradient(circle at 88% -5%, rgba(79,140,255,.16), transparent 28%),
        radial-gradient(circle at 5% 30%, rgba(53,197,216,.055), transparent 23%),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1480px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

#MainMenu,
footer {
    visibility: hidden;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1526, #07111F);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}

.side-brand {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 4px 5px 14px;
}

.side-logo {
    width: 41px;
    height: 41px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg, #3D78E8, #59B6D8);
    box-shadow: 0 9px 24px rgba(53,130,230,.25);
    font-size: 19px;
}

.side-name {
    color: #F8FAFC;
    font-size: 16px;
    font-weight: 780;
}

.side-caption {
    color: #667892;
    font-size: 9px;
    margin-top: 4px;
    letter-spacing: .55px;
}

section[data-testid="stSidebar"] .stButton > button {
    min-height: 36px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(148,163,184,.12);
    color: #CBD5E1;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(79,140,255,.08);
    border-color: rgba(79,140,255,.35);
}

/* Topbar */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 19px;
    margin-bottom: 18px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background:
        linear-gradient(135deg, rgba(79,140,255,.10), rgba(15,29,49,.98) 58%),
        var(--panel);
    box-shadow: 0 16px 38px rgba(0,0,0,.17);
}

.top-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.top-logo {
    width: 46px;
    height: 46px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg, #3D78E8, #59B6D8);
    box-shadow: 0 9px 25px rgba(53,130,230,.23);
    font-size: 22px;
}

.top-name {
    color: #F8FAFC;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -.7px;
}

.top-sub {
    color: var(--muted);
    font-size: 11px;
    margin-top: 4px;
}

.status {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 7px 11px;
    border-radius: 999px;
    border: 1px solid rgba(53,211,154,.17);
    background: rgba(53,211,154,.055);
    color: #A7F3D0;
    font-size: 10px;
    font-weight: 700;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 10px rgba(53,211,154,.65);
}

/* Content */
.title {
    color: #F8FAFC;
    font-size: 18px;
    font-weight: 750;
    margin-top: 8px;
    margin-bottom: 4px;
}

.subtitle {
    color: var(--muted);
    font-size: 11px;
    margin-bottom: 13px;
}

.hero {
    padding: 27px;
    border: 1px solid var(--border);
    border-radius: 19px;
    margin-bottom: 18px;
    background:
        radial-gradient(circle at 88% 10%, rgba(53,197,216,.10), transparent 23%),
        radial-gradient(circle at 72% 100%, rgba(79,140,255,.10), transparent 30%),
        linear-gradient(135deg, rgba(79,140,255,.075), rgba(15,29,49,.98) 58%);
}

.hero-kicker {
    color: #86B8FF;
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.hero-title {
    color: #F8FAFC;
    font-size: 31px;
    font-weight: 810;
    line-height: 1.08;
    letter-spacing: -1px;
    margin-top: 5px;
}

.hero-copy {
    max-width: 770px;
    color: #9BAAC0;
    font-size: 12px;
    line-height: 1.7;
    margin-top: 9px;
}

.card {
    min-height: 134px;
    padding: 16px;
    border: 1px solid var(--border);
    border-radius: 15px;
    background: linear-gradient(145deg, rgba(255,255,255,.038), rgba(255,255,255,.012));
}

.card:hover {
    border-color: rgba(79,140,255,.25);
}

.card-icon {
    width: 35px;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(79,140,255,.09);
    color: #87B6FF;
    font-size: 16px;
    margin-bottom: 10px;
}

.card-title {
    color: #F8FAFC;
    font-size: 13px;
    font-weight: 720;
}

.card-text {
    color: #7F90A7;
    font-size: 10px;
    line-height: 1.5;
    margin-top: 4px;
}

/* Policy */
.policy-box {
    padding: 14px 16px;
    border: 1px solid rgba(79,140,255,.15);
    border-radius: 14px;
    background: rgba(79,140,255,.035);
}

.policy-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(148,163,184,.065);
}

.policy-row:last-child {
    border-bottom: 0;
}

.policy-label {
    color: #899AB0;
    font-size: 10px;
}

.policy-value {
    color: #F8FAFC;
    font-size: 11px;
    font-weight: 700;
}

/* Validation */
.validation-ok {
    padding: 13px 15px;
    border-radius: 13px;
    border: 1px solid rgba(53,211,154,.20);
    background: rgba(53,211,154,.055);
    color: #B5F5D8;
    font-size: 11px;
}

.validation-warn {
    padding: 13px 15px;
    border-radius: 13px;
    border: 1px solid rgba(244,201,93,.22);
    background: rgba(244,201,93,.055);
    color: #FBE8A6;
    font-size: 11px;
}

.validation-error {
    padding: 13px 15px;
    border-radius: 13px;
    border: 1px solid rgba(240,106,120,.24);
    background: rgba(240,106,120,.055);
    color: #FFC0C8;
    font-size: 11px;
}

/* Rule priority */
.priority-box {
    padding: 14px;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: rgba(255,255,255,.018);
}

.priority-item {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 9px 0;
    border-bottom: 1px solid rgba(148,163,184,.07);
}

.priority-item:last-child {
    border-bottom: 0;
}

.priority-number {
    width: 24px;
    height: 24px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(79,140,255,.09);
    color: #86B8FF;
    font-size: 10px;
    font-weight: 800;
}

.priority-name {
    color: #DDE6F2;
    font-size: 11px;
    font-weight: 680;
}

/* Metrics */
div[data-testid="stMetric"] {
    min-height: 88px;
    padding: 12px 14px;
    border-radius: 14px;
    border: 1px solid var(--border);
    background: linear-gradient(145deg, rgba(255,255,255,.04), rgba(255,255,255,.014));
}

div[data-testid="stMetric"] label {
    color: #899AB0 !important;
    font-size: 10px !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-size: 23px !important;
    font-weight: 780 !important;
}

/* Buttons */
.stButton > button {
    min-height: 40px;
    border-radius: 10px;
    border: 1px solid rgba(79,140,255,.27);
    font-weight: 680;
    transition: .15s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    border-color: rgba(117,167,255,.70);
    box-shadow: 0 8px 22px rgba(79,140,255,.12);
}

.stButton > button[kind="primary"] {
    color: #FFFFFF;
    border: 0;
    background: linear-gradient(135deg, #3D78E8, #4FA6D4);
    box-shadow: 0 7px 22px rgba(61,120,232,.22);
}

/* Inputs */
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="input"] > div {
    background: var(--panel) !important;
    border: 1px solid rgba(148,163,184,.17) !important;
    border-radius: 10px !important;
}

textarea,
input {
    color: #F8FAFC !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
}

/* Details */
.detail-card {
    min-height: 85px;
    padding: 14px 15px;
    border: 1px solid var(--border);
    border-radius: 13px;
    background: linear-gradient(145deg, rgba(255,255,255,.038), rgba(255,255,255,.014));
}

.detail-label {
    color: #899AB0;
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .75px;
    margin-bottom: 6px;
}

.detail-value {
    color: #F8FAFC;
    font-size: 15px;
    font-weight: 720;
    line-height: 1.4;
}

.reason-box {
    margin-top: 9px;
    padding: 14px 16px;
    border: 1px solid rgba(79,140,255,.15);
    border-radius: 13px;
    background: linear-gradient(135deg, rgba(79,140,255,.065), rgba(53,197,216,.025));
}

.reason-title {
    color: #86B8FF;
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin-bottom: 5px;
}

.reason-text {
    color: #D6DDEA;
    font-size: 12px;
    line-height: 1.55;
}

.footer {
    display: flex;
    justify-content: space-between;
    margin-top: 28px;
    padding-top: 12px;
    border-top: 1px solid rgba(148,163,184,.07);
    color: #475569;
    font-size: 9px;
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# STATE
# ============================================================
DEFAULT_POLICY = (
    "Auto-approve expenses under $500 for Sales, "
    "escalate expenses above $2,000, and reject expenses above $5,000."
)

PAGES = ["Home", "Policy", "Claims", "Audit Log", "About"]

st.session_state.setdefault("page", "Home")
st.session_state.setdefault("policy_text", DEFAULT_POLICY)
st.session_state.setdefault("rules", parse_policy(DEFAULT_POLICY))
st.session_state.setdefault("results", None)
st.session_state.setdefault("uploaded_data", None)
st.session_state.setdefault("validation", None)


# ============================================================
# VALIDATION
# ============================================================
def validate_policy(policy_text, rules):
    errors = []
    warnings = []

    if not isinstance(rules, dict):
        return ["Parser did not return a valid policy object."], []

    required = [
        "auto_approve_department",
        "auto_approve_below",
        "escalate_above",
        "reject_above",
    ]

    missing = [key for key in required if key not in rules]
    if missing:
        errors.append("Missing policy fields: " + ", ".join(missing))
        return errors, warnings

    try:
        auto_limit = float(rules["auto_approve_below"])
        escalate_limit = float(rules["escalate_above"])
        reject_limit = float(rules["reject_above"])
    except (TypeError, ValueError):
        errors.append("Policy thresholds must be numeric.")
        return errors, warnings

    if auto_limit < 0 or escalate_limit < 0 or reject_limit < 0:
        errors.append("Thresholds cannot be negative.")

    if reject_limit <= escalate_limit:
        errors.append(
            f"Conflicting thresholds: reject threshold (${reject_limit:,.2f}) "
            f"must be greater than escalation threshold (${escalate_limit:,.2f})."
        )

    if escalate_limit <= auto_limit:
        errors.append(
            f"Conflicting thresholds: escalation threshold (${escalate_limit:,.2f}) "
            f"must be greater than auto-approval threshold (${auto_limit:,.2f})."
        )

    if auto_limit == escalate_limit:
        warnings.append(
            f"Boundary collision at ${auto_limit:,.2f}: "
            "auto-approval and escalation thresholds are identical."
        )

    if escalate_limit == reject_limit:
        warnings.append(
            f"Boundary collision at ${escalate_limit:,.2f}: "
            "escalation and rejection thresholds are identical."
        )

    if "under" not in policy_text.lower() and "below" not in policy_text.lower():
        warnings.append(
            "Auto-approval wording was not explicitly expressed as "
            "'under' or 'below'. Confirm the intended boundary."
        )

    if "above" not in policy_text.lower() and "over" not in policy_text.lower():
        warnings.append(
            "Escalation/rejection wording was not explicitly expressed as "
            "'above' or 'over'. Confirm the intended boundary."
        )

    if auto_limit in (500, 2000, 5000):
        warnings.append(
            f"Boundary check: ${auto_limit:,.0f} is exactly on a configured "
            "threshold. Verify whether equality should remain outside the rule."
        )

    if escalate_limit in (500, 2000, 5000):
        warnings.append(
            f"Boundary check: ${escalate_limit:,.0f} is exactly on a configured "
            "threshold. Verify equality behavior."
        )

    if reject_limit in (500, 2000, 5000):
        warnings.append(
            f"Boundary check: ${reject_limit:,.0f} is exactly on a configured "
            "threshold. Verify equality behavior."
        )

    if not str(rules["auto_approve_department"]).strip():
        errors.append("Auto-approval department cannot be empty.")

    return errors, warnings


def validate_current_policy():
    return validate_policy(
        st.session_state.policy_text,
        st.session_state.rules,
    )


def evaluate(expense_df):
    errors, warnings = validate_current_policy()

    if errors:
        st.error(
            "Policy validation failed. Fix the policy before evaluating claims."
        )
        return None

    st.session_state.results = apply_rules(
        expense_df,
        st.session_state.rules,
    )
    return st.session_state.results


def navigate(page):
    st.session_state.page = page
    st.rerun()


# ============================================================
# DATA
# ============================================================
if st.session_state.uploaded_data is not None:
    expenses = pd.read_csv(st.session_state.uploaded_data)
else:
    expenses = pd.read_csv(Path("data") / "expenses.csv")

required_columns = {
    "claim_id",
    "employee",
    "department",
    "category",
    "amount",
    "description",
}

missing_columns = required_columns - set(expenses.columns)

if missing_columns:
    st.error(
        "Missing required columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="side-brand">
            <div class="side-logo">🛡️</div>
            <div>
                <div class="side-name">PolicyPilot</div>
                <div class="side-caption">APPROVAL INTELLIGENCE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("WORKSPACE")

    selected_page = st.radio(
        "Navigation",
        PAGES,
        index=PAGES.index(st.session_state.page),
        format_func=lambda page: {
            "Home": "⌂   Home",
            "Policy": "⚙   Policy",
            "Claims": "▣   Claims",
            "Audit Log": "≡   Audit Log",
            "About": "ⓘ   About",
        }[page],
        label_visibility="collapsed",
    )

    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    st.divider()

    st.caption("QUICK ACTIONS")

    if st.button("＋  New policy", use_container_width=True):
        navigate("Policy")

    if st.button("▶  Evaluate claims", use_container_width=True):
        navigate("Claims")

    if st.button("≡  Audit history", use_container_width=True):
        navigate("Audit Log")

    st.divider()

    st.caption("POLICY STATUS")

    errors, warnings = validate_current_policy()

    if errors:
        st.error("Validation failed")
    elif warnings:
        st.warning("Valid with warnings")
    else:
        st.success("Policy validated", icon="✓")

    rules = st.session_state.rules

    st.markdown(
        f"""
        <div style="
            padding:11px;
            border:1px solid rgba(79,140,255,.14);
            border-radius:11px;
            background:rgba(79,140,255,.035);
            color:#94A3B8;
            font-size:10px;
            line-height:1.7;">
            <b style="color:#F8FAFC;">
                {rules.get("auto_approve_department", "—")}
            </b>
            auto-approve &lt; ${float(rules.get("auto_approve_below", 0)):,.0f}<br>
            Escalate &gt; ${float(rules.get("escalate_above", 0)):,.0f}<br>
            Reject &gt; ${float(rules.get("reject_above", 0)):,.0f}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TOP BAR
# ============================================================
st.markdown(
    """
    <div class="topbar">
        <div class="top-left">
            <div class="top-logo">🛡️</div>
            <div>
                <div class="top-name">PolicyPilot</div>
                <div class="top-sub">
                    Policy-driven expense approval workspace
                </div>
            </div>
        </div>
        <div class="status">
            <span class="status-dot"></span>
            System operational
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HOME
# ============================================================
if st.session_state.page == "Home":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Approval intelligence</div>
            <div class="hero-title">
                Make policy-driven decisions simple.
            </div>
            <div class="hero-copy">
                Configure business rules, validate policy conflicts,
                evaluate expense claims, and trace every decision
                from one professional workspace.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="title">Quick access</div>'
        '<div class="subtitle">Jump directly to the task you need.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">⚙</div>
                <div class="card-title">Configure policy</div>
                <div class="card-text">
                    Define business approval rules in plain English.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Policy  →", key="home_policy", use_container_width=True):
            navigate("Policy")

    with c2:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">▣</div>
                <div class="card-title">Evaluate claims</div>
                <div class="card-text">
                    Run the existing deterministic rule engine on a batch.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Claims  →", key="home_claims", use_container_width=True):
            navigate("Claims")

    with c3:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">≡</div>
                <div class="card-title">Audit decisions</div>
                <div class="card-text">
                    Inspect applied rules, decisions, and rationales.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Audit Log  →", key="home_audit", use_container_width=True):
            navigate("Audit Log")

    st.markdown(
        '<div class="title">Policy status</div>',
        unsafe_allow_html=True,
    )

    errors, warnings = validate_current_policy()

    if errors:
        st.markdown(
            '<div class="validation-error"><b>✕ Validation failed</b><br>'
            + "<br>".join(errors)
            + "</div>",
            unsafe_allow_html=True,
        )
    elif warnings:
        st.markdown(
            '<div class="validation-warn"><b>⚠ Valid with warnings</b><br>'
            + "<br>".join(warnings)
            + "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="validation-ok"><b>✓ Policy validated</b><br>'
            'No threshold conflicts detected. Rule order is deterministic.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="title">Current rules</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="policy-box">
            <div class="policy-row">
                <span class="policy-label">Auto-approval</span>
                <span class="policy-value">
                    {rules["auto_approve_department"]}
                    below ${float(rules["auto_approve_below"]):,.0f}
                </span>
            </div>
            <div class="policy-row">
                <span class="policy-label">Escalation</span>
                <span class="policy-value">
                    Above ${float(rules["escalate_above"]):,.0f}
                </span>
            </div>
            <div class="policy-row">
                <span class="policy-label">Rejection</span>
                <span class="policy-value">
                    Above ${float(rules["reject_above"]):,.0f}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.results is None and not errors:
        results = evaluate(expenses)
    else:
        results = st.session_state.results

    if results is not None:
        total = len(results)
        approved = int((results["decision"] == "APPROVE").sum())
        review = int((results["decision"] == "REVIEW").sum())
        escalated = int((results["decision"] == "ESCALATE").sum())
        rejected = int((results["decision"] == "REJECT").sum())

        st.markdown(
            '<div class="title">Live snapshot</div>',
            unsafe_allow_html=True,
        )

        a, b, c, d, e = st.columns(5)
        a.metric("Total claims", total)
        b.metric("Approved", approved)
        c.metric("Review", review)
        d.metric("Escalated", escalated)
        e.metric("Rejected", rejected)


# ============================================================
# POLICY
# ============================================================
elif st.session_state.page == "Policy":

    st.markdown(
        '<div class="title">Policy configuration</div>'
        '<div class="subtitle">'
        'Write the business policy in plain English. The existing parser '
        'converts it into the structured configuration used by the rule engine.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.session_state.policy_text = st.text_area(
        "Business policy",
        value=st.session_state.policy_text,
        height=145,
    )

    if st.button("✦  Parse, validate and activate", type="primary"):

        parsed_rules = parse_policy(
            st.session_state.policy_text
        )

        errors, warnings = validate_policy(
            st.session_state.policy_text,
            parsed_rules,
        )

        st.session_state.rules = parsed_rules
        st.session_state.validation = {
            "errors": errors,
            "warnings": warnings,
        }

        if errors:
            st.session_state.results = None
            st.error(
                "Policy was parsed but failed validation. "
                "Fix the highlighted conflicts before evaluating claims."
            )
        else:
            st.session_state.results = None
            st.success("Policy parsed and activated.", icon="✅")

        st.rerun()

    current = st.session_state.rules
    errors, warnings = validate_current_policy()

    st.markdown(
        '<div class="title">Validation status</div>',
        unsafe_allow_html=True,
    )

    if errors:
        st.markdown(
            '<div class="validation-error"><b>✕ Invalid policy</b><br>'
            + "<br>".join(errors)
            + "</div>",
            unsafe_allow_html=True,
        )
    elif warnings:
        st.markdown(
            '<div class="validation-warn"><b>⚠ Valid with warnings</b><br>'
            + "<br>".join(warnings)
            + "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="validation-ok"><b>✓ Policy validated</b><br>'
            'No conflicts detected. Boundary behavior is explicit in the '
            'current rule model.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="title">Thresholds</div>',
        unsafe_allow_html=True,
    )

    p1, p2, p3 = st.columns(3)
    p1.metric(
        "Auto-approve below",
        f'${float(current["auto_approve_below"]):,.0f}',
    )
    p2.metric(
        "Escalate above",
        f'${float(current["escalate_above"]):,.0f}',
    )
    p3.metric(
        "Reject above",
        f'${float(current["reject_above"]):,.0f}',
    )

    st.markdown(
        '<div class="title">Rule priority</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="priority-box">
            <div class="priority-item">
                <div class="priority-number">01</div>
                <div class="priority-name">
                    REJECT — highest priority
                </div>
            </div>
            <div class="priority-item">
                <div class="priority-number">02</div>
                <div class="priority-name">
                    ESCALATE — high-value exception
                </div>
            </div>
            <div class="priority-item">
                <div class="priority-number">03</div>
                <div class="priority-name">
                    AUTO-APPROVE — department + amount condition
                </div>
            </div>
            <div class="priority-item">
                <div class="priority-number">04</div>
                <div class="priority-name">
                    REVIEW — default fallback
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="title">Boundary behavior</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Boundary values are intentionally shown as separate checks. "
        "For example, a rule written as 'below $500' does not claim that "
        "$500 itself is below the threshold. Confirm the wording you want "
        "before submission.",
        icon="ℹ️",
    )

    with st.expander("View structured policy"):
        st.json(current)


# ============================================================
# CLAIMS
# ============================================================
elif st.session_state.page == "Claims":

    st.markdown(
        '<div class="title">Claims workspace</div>'
        '<div class="subtitle">'
        'Evaluate the current expense batch against the validated policy.'
        '</div>',
        unsafe_allow_html=True,
    )

    errors, warnings = validate_current_policy()

    if errors:
        st.markdown(
            '<div class="validation-error"><b>✕ Evaluation blocked</b><br>'
            + "<br>".join(errors)
            + "</div>",
            unsafe_allow_html=True,
        )
    else:
        if warnings:
            st.markdown(
                '<div class="validation-warn"><b>⚠ Policy has warnings</b><br>'
                + "<br>".join(warnings)
                + "</div>",
                unsafe_allow_html=True,
            )

        upload_col, action_col = st.columns([5, 1])

        with upload_col:
            uploaded = st.file_uploader(
                "Upload expense CSV",
                type=["csv"],
            )

            if uploaded is not None:
                st.session_state.uploaded_data = uploaded
                expenses = pd.read_csv(uploaded)
                st.session_state.results = None

        with action_col:
            st.write("")
            st.write("")
            run = st.button(
                "▶  Evaluate",
                type="primary",
                use_container_width=True,
            )

        if run or st.session_state.results is None:
            results = evaluate(expenses)
        else:
            results = st.session_state.results

        if results is not None:
            total = len(results)
            approved = int((results["decision"] == "APPROVE").sum())
            review = int((results["decision"] == "REVIEW").sum())
            escalated = int((results["decision"] == "ESCALATE").sum())
            rejected = int((results["decision"] == "REJECT").sum())

            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Total claims", total)
            m2.metric("Approved", approved)
            m3.metric("Review", review)
            m4.metric("Escalated", escalated)
            m5.metric("Rejected", rejected)

            st.markdown(
                '<div class="title">Decision queue</div>'
                '<div class="subtitle">'
                'Every result includes the rule that produced it.'
                '</div>',
                unsafe_allow_html=True,
            )

            queue = results[
                [
                    "claim_id",
                    "employee",
                    "department",
                    "category",
                    "amount",
                    "decision",
                ]
            ].copy()

            queue["amount"] = queue["amount"].map(
                lambda value: f"${value:,.2f}"
            )

            st.dataframe(
                queue,
                use_container_width=True,
                hide_index=True,
                height=min(465, 95 + len(queue) * 36),
            )

            st.markdown(
                '<div class="title">Decision explanation</div>',
                unsafe_allow_html=True,
            )

            selected_claim = st.selectbox(
                "Select claim",
                results["claim_id"].tolist(),
            )

            selected = results[
                results["claim_id"] == selected_claim
            ].iloc[0]

            d1, d2, d3 = st.columns([1, 1, 3])

            with d1:
                st.markdown(
                    f"""
                    <div class="detail-card">
                        <div class="detail-label">Decision</div>
                        <div class="detail-value">
                            {selected["decision"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with d2:
                st.markdown(
                    f"""
                    <div class="detail-card">
                        <div class="detail-label">Amount</div>
                        <div class="detail-value">
                            ${selected["amount"]:,.2f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with d3:
                st.markdown(
                    f"""
                    <div class="detail-card">
                        <div class="detail-label">Applied policy</div>
                        <div class="detail-value" style="font-size:14px;">
                            {selected["applied_rule"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <div class="reason-box">
                    <div class="reason-title">Why this decision?</div>
                    <div class="reason-text">
                        {selected["reason"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("🧾 View audit details"):
                st.code(
                    f'CLAIM       {selected["claim_id"]}\n'
                    f'EMPLOYEE    {selected["employee"]}\n'
                    f'DEPARTMENT  {selected["department"]}\n'
                    f'CATEGORY    {selected["category"]}\n'
                    f'AMOUNT      ${selected["amount"]:,.2f}\n'
                    f'DECISION    {selected["decision"]}\n'
                    f'RULE        {selected["applied_rule"]}\n'
                    f'REASON      {selected["reason"]}',
                    language="text",
                )


# ============================================================
# AUDIT LOG
# ============================================================
elif st.session_state.page == "Audit Log":

    st.markdown(
        '<div class="title">Audit log</div>'
        '<div class="subtitle">'
        'Traceable decisions from the latest evaluation batch.'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.results is None:
        st.info(
            "No evaluation has been run yet. Open Claims and evaluate a batch.",
            icon="ℹ️",
        )

        if st.button("Go to Claims  →", type="primary"):
            navigate("Claims")
    else:
        results = st.session_state.results

        audit = results[
            [
                "claim_id",
                "employee",
                "department",
                "category",
                "amount",
                "decision",
                "applied_rule",
                "reason",
            ]
        ].copy()

        audit["amount"] = audit["amount"].map(
            lambda value: f"${value:,.2f}"
        )

        st.dataframe(
            audit,
            use_container_width=True,
            hide_index=True,
            height=535,
        )


# ============================================================
# ABOUT
# ============================================================
else:

    st.markdown(
        '<div class="title">About PolicyPilot</div>'
        '<div class="subtitle">'
        'A configurable expense approval workspace.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">FDE assessment</div>
            <div class="hero-title">
                Configurable policy. Deterministic decisions. Clear reasoning.
            </div>
            <div class="hero-copy">
                PolicyPilot converts plain-English policy into structured
                configuration and evaluates expense claims with a
                traceable decision and rationale.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">✦</div>
                <div class="card-title">Policy parser</div>
                <div class="card-text">
                    Uses the existing local parser to create structured rules.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">⚖</div>
                <div class="card-title">Rule engine</div>
                <div class="card-text">
                    Uses the existing deterministic engine for decisions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">⌁</div>
                <div class="card-title">Traceability</div>
                <div class="card-text">
                    Shows the applied rule and rationale for every claim.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        <span>PolicyPilot</span>
        <span>FDE Assessment • Synthetic data</span>
    </div>
    """,
    unsafe_allow_html=True,
)

import pandas as pd


def apply_rules(expenses: pd.DataFrame, rules: dict) -> pd.DataFrame:
    """Apply policy rules and keep the reason for every decision."""
    results = []

    for _, expense in expenses.iterrows():
        amount = float(expense["amount"])
        department = str(expense["department"]).strip()

        decision = "REVIEW"
        reason = "No matching policy rule was found; human review is required."
        applied_rule = "Default review rule"

        if amount > rules["reject_above"]:
            decision = "REJECT"
            reason = (
                f"Amount ${amount:,.2f} exceeds the rejection threshold "
                f"of ${rules['reject_above']:,.2f}."
            )
            applied_rule = f"Reject expenses above ${rules['reject_above']:,.2f}"

        elif amount > rules["escalate_above"]:
            decision = "ESCALATE"
            reason = (
                f"Amount ${amount:,.2f} exceeds the escalation threshold "
                f"of ${rules['escalate_above']:,.2f}."
            )
            applied_rule = f"Escalate expenses above ${rules['escalate_above']:,.2f}"

        elif (
            department.casefold() == rules["auto_approve_department"].casefold()
            and amount < rules["auto_approve_below"]
        ):
            decision = "APPROVE"
            reason = (
                f"{department} expense is below the auto-approval limit "
                f"of ${rules['auto_approve_below']:,.2f}."
            )
            applied_rule = (
                f"Auto-approve {rules['auto_approve_department']} "
                f"expenses below ${rules['auto_approve_below']:,.2f}"
            )

        results.append(
            {
                "claim_id": expense["claim_id"],
                "employee": expense["employee"],
                "department": expense["department"],
                "category": expense["category"],
                "amount": amount,
                "description": expense["description"],
                "decision": decision,
                "reason": reason,
                "applied_rule": applied_rule,
            }
        )

    return pd.DataFrame(results)

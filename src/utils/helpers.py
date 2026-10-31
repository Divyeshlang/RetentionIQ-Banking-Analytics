# Helper formatting and utility routines

def format_euro(val: float) -> str:
    """Format numerical value as localized currency in Euros."""
    return f"€{val:,.0f}"


def format_percent(val: float) -> str:
    """Format decimal number as percentage."""
    return f"{val:.1%}"


def assign_recommended_action(row, balance_cutoff: float, salary_cutoff: float) -> str:
    """
    Transparent, rule-based recommendation mapping for at-risk accounts:
    - High balance & high salary: Premium relationship review
    - High balance & single product: Product adoption review
    - Fragile tier: Re-engagement campaign
    - High salary: Product adoption review
    - Else: Routine engagement monitoring
    """
    bal = row["Balance"]
    sal = row["EstimatedSalary"]
    prods = row["NumOfProducts"]
    tier = row["Relationship Tier"]

    if bal >= balance_cutoff and sal >= salary_cutoff:
        return "Premium relationship review"
    elif bal >= balance_cutoff and prods == 1:
        return "Product adoption review"
    elif tier == "Fragile":
        return "Re-engagement campaign"
    elif sal >= salary_cutoff:
        return "Product adoption review"
    else:
        return "Routine engagement monitoring"

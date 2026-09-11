def calculate_recovery_debt(persistence, worsening,anomaly_strength,recovering=False):
    """
    Calculate SENTRA Recovery Debt.
    Returns a value between 0 and 1.

    This is a proposed SENTRA decision-support
    mechanism, not an established NASA metric.
    """

    debt = (0.40 * persistence +0.35 * worsening +0.25 * anomaly_strength)

    # During recovery, reduce the accumulated concern gradually.
    if recovering:
        debt *= 0.70

    # Keep the value safely between 0 and 1.
    debt = max(0.0, min(1.0, debt))

    return round(debt, 3)
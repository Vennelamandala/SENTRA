from intelligence.recovery import calculate_recovery_debt
from intelligence.explainability import generate_explanation


def calculate_priority( anomaly_strength,persistence,worsening,cross_channel,recovery_debt,early_warning):
    """
    Calculate operational attention priority.
    Returns a score from 0 to 100.
    This is NOT a probability of spacecraft failure.
    """

    score = (
        0.30 * anomaly_strength +
        0.20 * persistence +
        0.15 * worsening +
        0.15 * cross_channel +
        0.10 * recovery_debt +
        0.10 * early_warning
    )

    return round(score * 100)


def get_severity(priority):
    if priority >= 75:
        return "CRITICAL"
    elif priority >= 50:
        return "HIGH"
    elif priority >= 25:
        return "MODERATE"
    else:
        return "LOW"

def determine_status(
    persistence,
    worsening,
    recovering=False,
    stable=False
):
    """
    Determine the current incident lifecycle state.
    """
    if stable:
        return "CLOSED"
    if recovering:
        return "RECOVERING"
    if worsening >= 0.70:
        return "WORSENING"
    if persistence >= 0.50:
        return "PERSISTENT"

    return "NEW"


def process_incident(incident):
    """
    Process one incident and add SENTRA
    decision-intelligence information.
    """

    # Get existing values from Person 2.
    anomaly_strength = incident.get("anomaly_strength", 0.0)
    persistence = incident.get("persistence", 0.0)
    worsening = incident.get("worsening", 0.0)
    cross_channel = incident.get("cross_channel", 0.0)

    # Early warning may initially be unavailable.
    early_warning = incident.get("early_warning", 0.5)

    recovering = incident.get("recovering", False)
    stable = incident.get("stable", False)

    # --------------------------------
    # 1. Recovery Debt
    # --------------------------------

    recovery_debt = calculate_recovery_debt(
        persistence=persistence,
        worsening=worsening,
        anomaly_strength=anomaly_strength,
        recovering=recovering
    )

    # --------------------------------
    # 2. Priority
    # --------------------------------

    priority = calculate_priority(
        anomaly_strength=anomaly_strength,
        persistence=persistence,
        worsening=worsening,
        cross_channel=cross_channel,
        recovery_debt=recovery_debt,
        early_warning=early_warning
    )

    # --------------------------------
    # 3. Severity
    # --------------------------------

    severity = get_severity(priority)

    # --------------------------------
    # 4. Lifecycle
    # --------------------------------

    status = determine_status(
        persistence=persistence,
        worsening=worsening,
        recovering=recovering,
        stable=stable
    )

    # --------------------------------
    # 5. Add results to incident
    # --------------------------------

    incident["recovery_debt"] = recovery_debt
    incident["priority"] = priority
    incident["severity"] = severity
    incident["status"] = status

    # --------------------------------
    # 6. Explainability
    # --------------------------------

    incident["explanation"] = generate_explanation(incident)

    return incident
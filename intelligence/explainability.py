def generate_explanation(incident):
    """
    Generate a human-readable explanation
    for why an incident received its priority.
    """

    reasons = []

    anomaly_strength = incident.get("anomaly_strength", 0.0)
    persistence = incident.get("persistence", 0.0)
    worsening = incident.get("worsening", 0.0)
    cross_channel = incident.get("cross_channel", 0.0)

    channels = incident.get("channels", [])

    # Strong anomaly evidence
    if anomaly_strength >= 0.70:
        reasons.append("strong anomaly evidence")

    # Persistent behavior
    if persistence >= 0.70:
        reasons.append("persistent abnormal behavior")

    # Increasing anomaly evidence
    if worsening >= 0.70:
        reasons.append("anomaly evidence is increasing")

    # Multiple telemetry channels
    if cross_channel >= 0.60:
        reasons.append(
            f"{len(channels)} telemetry channels affected"
        )

    # Recovery concern
    recovery_debt = incident.get("recovery_debt", 0.0)

    if recovery_debt >= 0.70:
        reasons.append("high unresolved recovery debt")

    # Nothing particularly strong
    if not reasons:
        return (
            "Limited evidence of sustained abnormal "
            "telemetry behavior."
        )

    return (
        "Priority driven by "
        + ", ".join(reasons)
        + "."
    )
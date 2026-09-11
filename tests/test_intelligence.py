from intelligence.severity_engine import process_incident


# Mock incident.
# Later Person 2's real incident output
# will have the same basic fields.

incident = {
    "incident_id": 1,

    "start": 100,
    "end": 110,

    "channels": [
        "P-10",
        "P-11",
        "A-04"
    ],

    "anomaly_strength": 0.91,
    "persistence": 0.82,
    "worsening": 0.94,
    "cross_channel": 0.81,

    "early_warning": 0.70,

    "recovering": False,
    "stable": False
}


result = process_incident(incident)


print("\n========== SENTRA INCIDENT ==========")

print("Incident ID:", result["incident_id"])
print("Priority:", result["priority"])
print("Severity:", result["severity"])
print("Status:", result["status"])
print("Recovery Debt:", result["recovery_debt"])

print("\nExplanation:")
print(result["explanation"])

print("==========================================")
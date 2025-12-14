# utils/failure_classifier.py

def classify_failure(longrepr) -> str:
    """
    Classifies failure type for reporting.
    """

    if not longrepr:
        return "Unknown"

    text = str(longrepr)

    if "AssertionError" in text:
        return "Assertion"

    if "Timeout" in text or "timeout" in text:
        return "Timeout"

    if "locator" in text or "Element not found" in text:
        return "UI Locator"

    if "ConnectionError" in text or "ECONNREFUSED" in text:
        return "Infrastructure"

    return "Other"

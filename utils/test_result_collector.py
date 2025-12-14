from collections import defaultdict

class TestResults:
    total = 0
    passed = 0
    failed = 0
    skipped = 0
    by_marker = defaultdict(lambda: {"passed": 0, "failed": 0, "skipped": 0})

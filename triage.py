import json
from collections import Counter

with open("semgrep-results.json") as f:
    data = json.load(f)

rank = {"ERROR": 0, "WARNING": 1, "MEDIUM": 1, "INFO": 2}

def severity_rank(result):
    return rank.get(result["extra"]["severity"], 3)

def category(path):
    if path.startswith(".github/"):
        return "Pipeline (workflows)"
    elif path.startswith("data/static/codefixes/"):
        return "Juice Shop challenge snippets"
    elif path.endswith(".tf"):
        return "Terraform"
    elif path.endswith(".npmrc"):
        return "npm config"
    else:
        return "Application code"

sorted_results = sorted(data["results"], key=severity_rank)

severity_counts = Counter()
path_counts = Counter()
category_counts = Counter()

print("All findings, most severe first")
for result in sorted_results:
    severity = result["extra"]["severity"]
    rule = result["check_id"]
    path = result["path"]
    line = result["start"]["line"]
    print(severity, path, line, rule)
    severity_counts[severity] += 1
    path_counts[path] += 1
    category_counts[category(path)] += 1

print()
print("Findings by severity")
for severity, n in severity_counts.items():
    print(n, severity)

print()
print("Findings by category")
for name, n in category_counts.most_common():
    print(n, name)

print()
print("Findings per file")
for path, n in path_counts.most_common():
    print(n, path)

print()
print("ERROR findings in pipeline and application code")
for result in sorted_results:
    severity = result["extra"]["severity"]
    path = result["path"]
    if severity == "ERROR" and category(path) in ("Pipeline (workflows)", "Application code"):
        print(path, result["start"]["line"], result["check_id"])
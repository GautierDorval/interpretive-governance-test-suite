#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

try:
    import jsonschema  # type: ignore
except Exception as e:
    print("Missing dependency: jsonschema. Install with: pip install jsonschema")
    raise

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "schemas"

SCHEMA_MAP = {
    "question-set": SCHEMAS_DIR / "question-set.schema.json",
    "response-log": SCHEMAS_DIR / "response-log.schema.json",
    "scoring-output": SCHEMAS_DIR / "scoring-output.schema.json",
    "variance-report": SCHEMAS_DIR / "variance-report.schema.json",
}

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise RuntimeError(f"Invalid JSON: {path} ({e})")

def validate_instance(instance, schema_path: Path, instance_path: Path):
    schema = load_json(schema_path)
    try:
        jsonschema.validate(instance=instance, schema=schema)
    except jsonschema.ValidationError as e:
        raise RuntimeError(f"Schema validation failed for {instance_path}\n  Schema: {schema_path}\n  Error: {e.message}")

def check_markdown_fences():
    problems = []
    for md in REPO_ROOT.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        fences = len(re.findall(r"^```", text, flags=re.MULTILINE))
        if fences % 2 != 0:
            problems.append(f"Unbalanced code fences in {md.relative_to(REPO_ROOT)} (count={fences})")
    return problems

def check_relative_links():
    problems = []
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for md in REPO_ROOT.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
                continue
            if target.startswith("mailto:"):
                continue
            # Strip anchors
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            # Ignore images and external-ish patterns
            if "://" in target_path:
                continue
            resolved = (md.parent / target_path).resolve()
            if not resolved.exists():
                problems.append(f"Broken link in {md.relative_to(REPO_ROOT)} -> {target}")
    return problems

def check_scoring_models_present():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    dims = [
        ("Interpretive fidelity", "fidelity-score.md"),
        ("Anti-inference compliance", "anti-inference-score.md"),
        ("Attribution integrity", "attribution-integrity-score.md"),
        ("Authority boundary compliance", "authority-boundary-score.md"),
        ("Silence quality", "silence-quality-score.md"),
        ("Inter-model variance", "variance-index.md"),
    ]
    problems = []
    for label, fname in dims:
        if label not in readme:
            problems.append(f"README missing governance dimension label: {label}")
        if not (REPO_ROOT / "scoring-models" / fname).exists():
            problems.append(f"Missing scoring model file: scoring-models/{fname}")
    return problems

def main():
    problems = []

    # JSON syntax + schema validation for datasets and examples
    json_files = []
    for p in (REPO_ROOT / "datasets").glob("*.json"):
        json_files.append(p)
    for p in (REPO_ROOT / "examples").rglob("*.json"):
        json_files.append(p)

    for jf in json_files:
        inst = load_json(jf)
        schema_url = None
        if isinstance(inst, dict) and "$schema" in inst:
            schema_url = inst["$schema"]
        # Map by file name conventions
        name = jf.name
        if "question" in name:
            schema_path = SCHEMA_MAP["question-set"]
        elif "response" in name:
            schema_path = SCHEMA_MAP["response-log"]
        elif "scoring" in name:
            schema_path = SCHEMA_MAP["scoring-output"]
        elif "variance" in name:
            schema_path = SCHEMA_MAP["variance-report"]
        else:
            continue
        try:
            validate_instance(inst, schema_path, jf)
        except Exception as e:
            problems.append(str(e))

    problems.extend(check_markdown_fences())
    problems.extend(check_relative_links())
    problems.extend(check_scoring_models_present())

    if problems:
        print("Validation failed:\n")
        for p in problems:
            print(f"- {p}")
        sys.exit(1)

    print("All checks passed.")

if __name__ == "__main__":
    main()


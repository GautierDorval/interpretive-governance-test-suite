#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import jsonschema  # type: ignore
except Exception as e:
    print("Missing dependency: jsonschema. Install with: pip install jsonschema")
    raise

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "schemas"
STANDARD_REFERENCE = REPO_ROOT / "references" / "standard-reference.json"
STANDARD_REFERENCE_SCHEMA = SCHEMAS_DIR / "standard-reference.schema.json"
STANDARD_MANIFEST_PATH = "interpretive-governance.manifest.json"

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
        jsonschema.Draft202012Validator.check_schema(schema)
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

def check_all_json_syntax():
    """Validate JSON syntax for all tracked JSON/JSON-LD files."""
    problems = []
    for pattern in ("**/*.json", "**/*.jsonld"):
        for p in REPO_ROOT.rglob(pattern):
            if ".git" in p.parts:
                continue
            try:
                load_json(p)
            except Exception as e:
                problems.append(f"JSON syntax error: {p.relative_to(REPO_ROOT)} ({e})")
    return problems


def normalize_repository_url(value: str) -> str:
    return value.removesuffix(".git").rstrip("/")


def git_bytes(repository: Path, *args: str) -> bytes:
    result = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={repository}",
            "-C",
            str(repository),
            *args,
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout


def check_standard_reference(standard_repository: Path | None) -> list[str]:
    problems: list[str] = []
    if not STANDARD_REFERENCE.exists():
        return ["Missing exact standard reference: references/standard-reference.json"]
    if not STANDARD_REFERENCE_SCHEMA.exists():
        return ["Missing standard reference schema: schemas/standard-reference.schema.json"]

    try:
        reference = load_json(STANDARD_REFERENCE)
        validate_instance(reference, STANDARD_REFERENCE_SCHEMA, STANDARD_REFERENCE)
    except Exception as exc:
        return [str(exc)]

    if standard_repository is None:
        return problems

    repository = standard_repository.resolve()
    if not repository.is_dir():
        return [f"Standard repository path is not a directory: {repository}"]

    try:
        observed_remote = git_bytes(repository, "remote", "get-url", "origin").decode("utf-8").strip()
        if normalize_repository_url(observed_remote) != normalize_repository_url(reference["repository"]):
            problems.append(
                "Standard repository remote mismatch: "
                f"expected {reference['repository']}, observed {observed_remote}"
            )

        commit = reference["commit"]
        observed_commit = git_bytes(repository, "rev-parse", "--verify", f"{commit}^{{commit}}").decode("ascii").strip()
        if observed_commit != commit:
            problems.append(f"Standard commit mismatch: expected {commit}, observed {observed_commit}")

        observed_tree = git_bytes(repository, "show", "-s", "--format=%T", commit).decode("ascii").strip()
        if observed_tree != reference["tree"]:
            problems.append(
                f"Standard tree mismatch: expected {reference['tree']}, observed {observed_tree}"
            )

        release = reference["release"]
        if release is not None:
            observed_release_commit = git_bytes(
                repository, "rev-parse", "--verify", f"refs/tags/{release}^{{commit}}"
            ).decode("ascii").strip()
            if observed_release_commit != commit:
                problems.append(
                    f"Standard release {release} resolves to {observed_release_commit}, not {commit}"
                )
        else:
            observed_tags = git_bytes(repository, "tag", "--points-at", commit).decode("utf-8").splitlines()
            if observed_tags:
                problems.append(
                    "Standard reference declares an unreleased snapshot but the commit is tagged: "
                    + ", ".join(observed_tags)
                )

        manifest_bytes = git_bytes(repository, "cat-file", "blob", f"{commit}:{STANDARD_MANIFEST_PATH}")
        expected_digest = reference["manifestDigest"]
        observed_digest = hashlib.sha256(manifest_bytes).hexdigest().upper()
        if observed_digest != expected_digest["value"]:
            problems.append(
                "Standard manifest digest mismatch: "
                f"expected {expected_digest['value']}, observed {observed_digest}"
            )
        if len(manifest_bytes) != expected_digest["length"]:
            problems.append(
                "Standard manifest length mismatch: "
                f"expected {expected_digest['length']}, observed {len(manifest_bytes)}"
            )
    except Exception as exc:
        problems.append(f"Unable to verify exact standard repository reference: {exc}")

    return problems


def self_test_standard_reference_schema() -> list[str]:
    """Prove that the closed reference envelope rejects common drift cases."""
    schema = load_json(STANDARD_REFERENCE_SCHEMA)
    reference = load_json(STANDARD_REFERENCE)
    validator = jsonschema.Draft202012Validator(schema)
    problems: list[str] = []

    invalid_cases = {
        "unknown property": {**reference, "branch": "main"},
        "short commit": {**reference, "commit": reference["commit"][:12]},
        "invalid digest": {
            **reference,
            "manifestDigest": {**reference["manifestDigest"], "value": "A" * 63},
        },
        "missing snapshot status": {
            key: value for key, value in reference.items() if key != "referenceStatus"
        },
        "snapshot status on release": {
            **reference,
            "release": "v1.5.1",
        },
    }

    for label, instance in invalid_cases.items():
        if validator.is_valid(instance):
            problems.append(f"Standard reference schema self-test accepted invalid case: {label}")

    released_reference = {
        key: value for key, value in reference.items() if key != "referenceStatus"
    }
    released_reference["release"] = "v1.5.1"
    if not validator.is_valid(released_reference):
        problems.append("Standard reference schema self-test rejected a valid tagged release envelope")

    return problems


def main():
    parser = argparse.ArgumentParser(description="Validate the test suite and its exact standard reference.")
    parser.add_argument(
        "--standard-repository",
        type=Path,
        help="Optional local clone used to verify the pinned standard commit, tree, release, and manifest bytes.",
    )
    parser.add_argument(
        "--self-test-standard-reference",
        action="store_true",
        help="Run negative and positive fixtures against the closed standard-reference schema.",
    )
    args = parser.parse_args()
    problems = []

    # JSON syntax for all JSON/JSON-LD files (schemas, terms, datasets, examples)
    problems.extend(check_all_json_syntax())
    problems.extend(check_standard_reference(args.standard_repository))
    if args.self_test_standard_reference:
        problems.extend(self_test_standard_reference_schema())

    # Schema validation for datasets and examples
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

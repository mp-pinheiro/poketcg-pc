#!/usr/bin/env python3
"""Validate the empty-slate completion issue manifest."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^completion:v1:p(?:3|4|5|6|7|8|x):[a-z0-9-]+:[a-z0-9-]+$")
TITLE_RE = re.compile(r"^(feat|fix|perf|refactor|docs|test|build|ci|chore)\([a-z0-9-]+\): [a-z][^.!?]*$")
HEADINGS = (
    "## Outcome", "## Classification", "## Problem and contract",
    "## Repository evidence", "### Observed facts", "### Inference",
    "## Scope", "### In scope", "### Out of scope", "## Constraints",
    "## Relationships", "## Acceptance criteria", "## Verification and close evidence",
)
REQUIRED_TAGS = ("phase-", "kind-", "area-", "priority-")
FORBIDDEN_BODY = ("TODO", "TBD", "PLACEHOLDER", "<...>")


def check_dag(issues: dict[str, dict], errors: list[str]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, path: tuple[str, ...]) -> None:
        if node in visiting:
            errors.append(f"dependency cycle: {' -> '.join((*path, node))}")
            return
        if node in visited:
            return
        visiting.add(node)
        issue = issues[node]
        deps = list(issue["blocked_by_ids"])
        if issue["parent_id"] is not None:
            deps.append(issue["parent_id"])
        for dep in deps:
            if dep in issues:
                visit(dep, (*path, node))
        visiting.remove(node)
        visited.add(node)

    for issue_id in issues:
        visit(issue_id, ())


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("docs/full-game-findings.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    if data.get("empty_slate") is not True:
        errors.append("empty_slate must be true")
    labels = data.get("labels", [])
    label_names = [label.get("name") for label in labels]
    if len(label_names) != len(set(label_names)):
        errors.append("duplicate label names")
    label_set = set(label_names)
    issues = data.get("issues", [])
    by_id: dict[str, dict] = {}
    by_finding: dict[str, str] = {}
    remote_numbers: dict[int, str] = {}
    for index, issue in enumerate(issues):
        prefix = f"issues[{index}]"
        issue_id = issue.get("id")
        if not isinstance(issue_id, str) or not ID_RE.fullmatch(issue_id):
            errors.append(f"{prefix} invalid id")
        elif issue_id in by_id:
            errors.append(f"{prefix} duplicate id {issue_id}")
        else:
            by_id[issue_id] = issue
        title = issue.get("title", "")
        if len(title) > 50:
            errors.append(f"{issue_id} title exceeds 50 characters")
        if not TITLE_RE.fullmatch(title):
            errors.append(f"{issue_id} invalid title grammar")
        if "(" in title and ")" in title:
            title_type, title_scope = title.split("(", 1)[0], title.split("(", 1)[1].split(")", 1)[0]
            if issue.get("type") != title_type or issue.get("scope") != title_scope:
                errors.append(f"{issue_id} title fields disagree")
        tags = issue.get("tags", [])
        if len(tags) != len(set(tags)):
            errors.append(f"{issue_id} duplicate tags")
        if not set(tags) <= label_set:
            errors.append(f"{issue_id} uses undeclared tags")
        for required in REQUIRED_TAGS:
            if sum(tag.startswith(required) for tag in tags) != 1:
                errors.append(f"{issue_id} must have exactly one {required} tag")
        if "risk-security" in tags and issue.get("flags") != ["risk-security"]:
            errors.append(f"{issue_id} security flag mismatch")
        if any(issue.get(field) not in tags for field in ("phase", "kind", "area", "priority")):
            errors.append(f"{issue_id} structured tags mismatch")
        for field in ("blocked_by_ids", "related_ids"):
            if not isinstance(issue.get(field), list) or len(issue[field]) != len(set(issue[field])):
                errors.append(f"{issue_id} invalid {field}")
        for finding in issue.get("source_finding_ids", []):
            if finding in by_finding:
                errors.append(f"finding {finding} owned by both {by_finding[finding]} and {issue_id}")
            by_finding[finding] = issue_id
        number = issue.get("remote_number")
        if number is not None:
            if not isinstance(number, int) or number <= 0:
                errors.append(f"{issue_id} invalid remote number")
            elif number in remote_numbers:
                errors.append(f"remote number {number} reused")
            else:
                remote_numbers[number] = issue_id
        body = issue.get("fully_rendered_body", "")
        for heading in HEADINGS:
            if heading not in body:
                errors.append(f"{issue_id} missing body heading {heading}")
        for token in FORBIDDEN_BODY:
            if token in body:
                errors.append(f"{issue_id} contains placeholder {token}")
        acceptance = issue.get("acceptance", [])
        verification = issue.get("verification", [])
        acceptance_ids = [row.get("id") for row in acceptance]
        verification_ids = [row.get("acceptance_id") for row in verification]
        if not acceptance_ids or len(acceptance_ids) != len(set(acceptance_ids)):
            errors.append(f"{issue_id} invalid acceptance IDs")
        if set(verification_ids) != set(acceptance_ids) or len(verification_ids) != len(acceptance_ids):
            errors.append(f"{issue_id} acceptance/verification mapping is not one-to-one")
        digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if issue.get("body_sha256") != digest:
            errors.append(f"{issue_id} body_sha256 mismatch")
    for index, issue in enumerate(issues):
        issue_id = issue.get("id", f"issues[{index}]")
        parent = issue.get("parent_id")
        if parent is not None and parent not in by_id:
            errors.append(f"{issue_id} unresolved parent {parent}")
        for field in ("blocked_by_ids", "related_ids"):
            for reference in issue.get(field, []):
                if reference not in by_id:
                    errors.append(f"{issue_id} unresolved {field} reference {reference}")
        if issue_id != "completion:v1:px:release:full-game" and parent != "completion:v1:px:release:full-game":
            errors.append(f"{issue_id} must have E00 as parent")
    check_dag(by_id, errors)
    register = data.get("finding_register", [])
    register_ids = [row.get("id") for row in register]
    if len(register_ids) != len(set(register_ids)):
        errors.append("duplicate finding-register IDs")
    if set(register_ids) != set(by_finding):
        errors.append("finding register and issue ownership differ")
    for row in register:
        if row.get("owner") not in by_id:
            errors.append(f"finding {row.get('id')} has unresolved owner")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"issue-manifest: valid issues={len(issues)} findings={len(register)} labels={len(labels)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

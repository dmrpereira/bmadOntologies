#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""First Breath scaffolding for formally-bmad-dsl-agent-steward."""

from __future__ import annotations

import re
import shutil
import sys
import argparse
import json
from datetime import date
from pathlib import Path

SKILL_NAME = "formally-bmad-dsl-agent-steward"
SANCTUM_DIR = SKILL_NAME
SKILL_ONLY_FILES = {"first-breath.md", ".decision-log.md"}
TEMPLATE_FILES = [
    "INDEX-template.md",
    "PERSONA-template.md",
    "CREED-template.md",
    "BOND-template.md",
    "MEMORY-template.md",
    "CAPABILITIES-template.md",
]


def parse_yaml_config(config_path: Path) -> dict[str, str]:
    config: dict[str, str] = {}
    if not config_path.exists():
        return config
    for line in config_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        value = value.strip().strip("'\"")
        if value:
            config[key.strip()] = value
    return config


def parse_frontmatter(file_path: Path) -> dict[str, str]:
    content = file_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    meta: dict[str, str] = {}
    for line in match.group(1).strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("'\"")
    return meta


def substitute_vars(content: str, variables: dict[str, str]) -> str:
    for key, value in variables.items():
        content = content.replace(f"{{{key}}}", value)
    return content


def discover_capabilities(references_dir: Path) -> list[dict[str, str]]:
    capabilities: list[dict[str, str]] = []
    for md_file in sorted(references_dir.glob("*.md")):
        if md_file.name in SKILL_ONLY_FILES:
            continue
        meta = parse_frontmatter(md_file)
        if meta.get("name") and meta.get("code"):
            capabilities.append({
                "name": meta["name"],
                "code": meta["code"],
                "description": meta.get("description", ""),
                "source": f"./references/{md_file.name}",
            })
    return capabilities


def capabilities_table(capabilities: list[dict[str, str]]) -> str:
    if not capabilities:
        return "| | | | |"
    return "\n".join(
        f"| `{cap['code']}` | {cap['name']} | {cap['description']} | `{cap['source']}` |"
        for cap in capabilities
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the Formally BMAD DSL steward sanctum.")
    parser.add_argument("project_root", help="Project root containing _bmad.")
    parser.add_argument("skill_path", help="Path to the steward skill directory.")
    parser.add_argument("-o", "--output", help="Write JSON result to file instead of stdout.")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    skill_path = Path(args.skill_path).resolve()
    sanctum_path = project_root / "_bmad" / "memory" / SANCTUM_DIR

    if sanctum_path.exists():
        result = {"status": "exists", "sanctum": str(sanctum_path)}
        output = json.dumps(result, indent=2, sort_keys=True)
        if args.output:
            Path(args.output).write_text(output + "\n", encoding="utf-8")
        else:
            print(output)
        return 0

    config: dict[str, str] = {}
    for name in ("config.yaml", "config.user.yaml"):
        config.update(parse_yaml_config(project_root / "_bmad" / name))

    references_dir = skill_path / "references"
    assets_dir = skill_path / "assets"
    sanctum_refs = sanctum_path / "references"
    sanctum_refs.mkdir(parents=True, exist_ok=True)
    (sanctum_path / "sessions").mkdir(parents=True, exist_ok=True)
    (sanctum_path / "capabilities").mkdir(parents=True, exist_ok=True)

    for reference in sorted(references_dir.glob("*.md")):
        if reference.name not in SKILL_ONLY_FILES:
            shutil.copy2(reference, sanctum_refs / reference.name)

    variables = {
        "user_name": config.get("user_name", "David"),
        "communication_language": config.get("communication_language", "English"),
        "birth_date": date.today().isoformat(),
        "project_root": str(project_root),
        "sanctum_path": str(sanctum_path),
        "capabilities-table": capabilities_table(discover_capabilities(references_dir)),
    }

    for template_name in TEMPLATE_FILES:
        template_path = assets_dir / template_name
        content = substitute_vars(template_path.read_text(encoding="utf-8"), variables)
        output_name = template_name.replace("-template", "").upper()
        output_name = output_name[:-3] + ".md"
        (sanctum_path / output_name).write_text(content, encoding="utf-8")

    result = {"status": "created", "sanctum": str(sanctum_path)}
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())

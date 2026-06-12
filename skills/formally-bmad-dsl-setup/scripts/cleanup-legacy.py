#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Remove legacy module directories from _bmad/ after config migration.

After merge-config.py and merge-help-csv.py have migrated config data and
deleted individual legacy files, this script removes the now-redundant
directory trees. These directories contain skill files that are already
installed at .claude/skills/ (or equivalent) — only the config files at
_bmad/ root need to persist.

When one or more --skills-dir values are provided, the script verifies that
every skill found in the legacy directories exists at at least one installed
location before removing anything. Directories without skills (like _config/)
are removed directly.

Exit codes: 0=success (including nothing to remove), 1=validation error, 2=runtime error
"""

import argparse
import json
import shutil
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Remove legacy module directories from _bmad/ after config migration."
    )
    parser.add_argument(
        "--bmad-dir",
        required=True,
        help="Path to the _bmad/ directory",
    )
    parser.add_argument(
        "--module-code",
        required=True,
        help="Module code being cleaned up (e.g. 'bmb')",
    )
    parser.add_argument(
        "--also-remove",
        action="append",
        default=[],
        help="Additional directory names under _bmad/ to remove (repeatable)",
    )
    parser.add_argument(
        "--skills-dir",
        action="append",
        default=[],
        help="Path to an installed skills directory such as .claude/skills/ "
        "(repeatable). Enables safety verification that skills are installed "
        "before removing legacy copies.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed progress to stderr",
    )
    return parser.parse_args()


def find_skill_dirs(base_path: str) -> list:
    """Find directories that contain a SKILL.md file.

    Walks the directory tree and returns the leaf directory name for each
    directory containing a SKILL.md. These are considered skill directories.

    Returns:
        List of skill directory names (e.g. ['bmad-agent-builder', 'bmad-builder-setup'])
    """
    skills = []
    root = Path(base_path)
    if not root.exists():
        return skills
    for skill_md in root.rglob("SKILL.md"):
        skills.append(skill_md.parent.name)
    return sorted(set(skills))


def verify_skills_installed(
    bmad_dir: str, dirs_to_check: list, skills_dirs: list[str], verbose: bool = False
) -> list:
    """Verify that skills in legacy directories exist at the installed location.

    Scans each directory in dirs_to_check for skill folders (containing SKILL.md),
    then checks that a matching directory exists under at least one skills_dir. Directories
    that contain no skills (like _config/) are silently skipped.

    Returns:
        List of verified skill names.

    Raises SystemExit(1) if any skills are missing from every skills_dir.
    """
    all_verified = []
    missing = []

    for dirname in dirs_to_check:
        legacy_path = Path(bmad_dir) / dirname
        if not legacy_path.exists():
            continue

        skill_names = find_skill_dirs(str(legacy_path))
        if not skill_names:
            if verbose:
                print(
                    f"No skills found in {dirname}/ — skipping verification",
                    file=sys.stderr,
                )
            continue

        for skill_name in skill_names:
            installed_paths = [Path(skills_dir) / skill_name for skills_dir in skills_dirs]
            found_path = next((path for path in installed_paths if path.is_dir()), None)
            if found_path is not None:
                all_verified.append(skill_name)
                if verbose:
                    print(
                        f"Verified: {skill_name} exists at {found_path}",
                        file=sys.stderr,
                    )
            else:
                missing.append(skill_name)
                if verbose:
                    print(
                        f"MISSING: {skill_name} not found under any of {skills_dirs}",
                        file=sys.stderr,
                    )

    if missing:
        error_result = {
            "status": "error",
            "error": "Skills not found at installed location",
            "missing_skills": missing,
            "skills_dirs": [str(Path(skills_dir).resolve()) for skills_dir in skills_dirs],
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

    return sorted(set(all_verified))


def count_files(path: Path) -> int:
    """Count all files recursively in a directory."""
    count = 0
    for item in path.rglob("*"):
        if item.is_file():
            count += 1
    return count


def cleanup_directories(
    bmad_dir: str, dirs_to_remove: list, verbose: bool = False
) -> tuple:
    """Remove specified directories under bmad_dir.

    Returns:
        (removed, not_found, total_files_removed) tuple
    """
    removed = []
    not_found = []
    total_files = 0

    for dirname in dirs_to_remove:
        target = Path(bmad_dir) / dirname
        if not target.exists():
            not_found.append(dirname)
            if verbose:
                print(f"Not found (skipping): {target}", file=sys.stderr)
            continue

        if not target.is_dir():
            if verbose:
                print(f"Not a directory (skipping): {target}", file=sys.stderr)
            not_found.append(dirname)
            continue

        file_count = count_files(target)
        if verbose:
            print(
                f"Removing {target} ({file_count} files)",
                file=sys.stderr,
            )

        try:
            shutil.rmtree(target)
        except OSError as e:
            error_result = {
                "status": "error",
                "error": f"Failed to remove {target}: {e}",
                "directories_removed": removed,
                "directories_failed": dirname,
            }
            print(json.dumps(error_result, indent=2))
            sys.exit(2)

        removed.append(dirname)
        total_files += file_count

    return removed, not_found, total_files


def main():
    args = parse_args()

    bmad_dir = args.bmad_dir

    # Build the list of directories to remove. For the isolated DSL branch, the
    # live module root under _bmad/ is authoritative state and must never be
    # removed by cleanup. Only explicitly named legacy directories are eligible.
    dirs_to_remove = list(args.also_remove)
    # Deduplicate while preserving order
    seen = set()
    unique_dirs = []
    for d in dirs_to_remove:
        if d not in seen:
            seen.add(d)
            unique_dirs.append(d)
    dirs_to_remove = unique_dirs

    if args.verbose:
        print(f"Directories to remove: {dirs_to_remove}", file=sys.stderr)

    # Safety check: verify skills are installed before removing
    verified_skills = None
    if args.skills_dir:
        if args.verbose:
            print(
                f"Verifying skills installed at {args.skills_dir}",
                file=sys.stderr,
            )
        verified_skills = verify_skills_installed(
            bmad_dir, dirs_to_remove, args.skills_dir, args.verbose
        )

    # Remove directories
    removed, not_found, total_files = cleanup_directories(
        bmad_dir, dirs_to_remove, args.verbose
    )

    # Build result
    result = {
        "status": "success",
        "bmad_dir": str(Path(bmad_dir).resolve()),
        "directories_removed": removed,
        "directories_not_found": not_found,
        "files_removed_count": total_files,
    }

    if args.skills_dir:
        result["safety_checks"] = {
            "skills_verified": True,
            "skills_dirs": [str(Path(skills_dir).resolve()) for skills_dir in args.skills_dir],
            "verified_skills": verified_skills,
        }
    else:
        result["safety_checks"] = None

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

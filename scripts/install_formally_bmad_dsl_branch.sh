#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILLS_ROOT="${REPO_ROOT}/skills"

PAYLOAD_SKILLS=(
  "formally-bmad-dsl-setup"
  "formally-bmad-dsl-agent-steward"
  "formally-bmad-dsl-brainstorming"
  "formally-bmad-dsl-prd"
  "formally-bmad-dsl-architecture"
  "formally-bmad-dsl-epics"
  "formally-bmad-dsl-stories"
  "formally-bmad-dsl-contracts"
  "formally-bmad-dsl-contract-stubs"
  "formally-bmad-implementation-contracts"
  "formally-bmad-code-verification"
  "formally-bmad-dsl-verification"
)

AGENTS=("claude" "codex" "pi")
TARGET_PROJECT=""
DRY_RUN=0
REPORT_FILE=""

usage() {
  cat <<'EOF'
Install the Formally BMAD parallel DSL branch into an existing BMad project.

Usage:
  install_formally_bmad_dsl_branch.sh --target-project PATH [options]

Options:
  --target-project PATH   Target project root where BMad is already installed.
  --agents LIST           Comma-separated subset of: claude,codex,pi. Default: claude,codex,pi
  --report PATH           Write a Markdown install report to PATH.
  --dry-run               Print actions without copying files.
  -h, --help              Show this help.

Install locations:
  claude -> <target-project>/.claude/skills/
  codex  -> <target-project>/.codex/skills/
  pi     -> <target-project>/.pi/skills/

Installed payload:
  - formally-bmad-dsl-setup
  - formally-bmad-dsl-agent-steward
  - formally-bmad-dsl-brainstorming
  - formally-bmad-dsl-prd
  - formally-bmad-dsl-architecture
  - formally-bmad-dsl-epics
  - formally-bmad-dsl-stories
  - formally-bmad-dsl-contracts
  - formally-bmad-dsl-contract-stubs
  - formally-bmad-implementation-contracts
  - formally-bmad-code-verification
  - formally-bmad-dsl-verification

The script replaces only those target skill directories. It does not install or
modify the original formally-bmad-formal-* branch.
EOF
}

fail() {
  echo "Error: $*" >&2
  exit 2
}

join_by() {
  local sep="$1"
  shift
  local first=1
  for item in "$@"; do
    if [[ $first -eq 1 ]]; then
      printf '%s' "$item"
      first=0
    else
      printf '%s%s' "$sep" "$item"
    fi
  done
}

agent_skill_dir() {
  local agent="$1"
  case "$agent" in
    claude) printf '%s/.claude/skills' "$TARGET_PROJECT" ;;
    codex) printf '%s/.codex/skills' "$TARGET_PROJECT" ;;
    pi) printf '%s/.pi/skills' "$TARGET_PROJECT" ;;
    *) return 1 ;;
  esac
}

parse_agents() {
  local raw="$1"
  local seen="|"
  local parsed=()
  IFS=',' read -r -a requested <<<"$raw"
  for agent in "${requested[@]}"; do
    agent="${agent// /}"
    case "$agent" in
      claude|codex|pi) ;;
      *) fail "Unsupported agent '${agent}'. Allowed: claude,codex,pi" ;;
    esac
    if [[ "$seen" != *"|${agent}|"* ]]; then
      parsed+=("$agent")
      seen="${seen}${agent}|"
    fi
  done
  if [[ ${#parsed[@]} -eq 0 ]]; then
    fail "No agents selected."
  fi
  AGENTS=("${parsed[@]}")
}

copy_skill_dir() {
  local src="$1"
  local dst="$2"
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] rm -rf ${dst}"
    echo "[dry-run] cp -R ${src} ${dst}"
    return 0
  fi

  rm -rf "$dst"
  mkdir -p "$(dirname "$dst")"
  cp -R "$src" "$dst"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-project)
      [[ $# -ge 2 ]] || fail "--target-project requires a value"
      TARGET_PROJECT="$2"
      shift 2
      ;;
    --agents)
      [[ $# -ge 2 ]] || fail "--agents requires a value"
      parse_agents "$2"
      shift 2
      ;;
    --report)
      [[ $# -ge 2 ]] || fail "--report requires a value"
      REPORT_FILE="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "Unknown argument: $1"
      ;;
  esac
done

[[ -n "$TARGET_PROJECT" ]] || fail "--target-project is required"
TARGET_PROJECT="$(cd "$TARGET_PROJECT" 2>/dev/null && pwd)" || fail "Target project does not exist: $TARGET_PROJECT"
[[ -d "${TARGET_PROJECT}/_bmad" ]] || fail "Target project does not look like a BMad project: missing ${TARGET_PROJECT}/_bmad"

for skill in "${PAYLOAD_SKILLS[@]}"; do
  [[ -d "${SKILLS_ROOT}/${skill}" ]] || fail "Missing source skill directory: ${SKILLS_ROOT}/${skill}"
done

echo "Installing Formally BMAD DSL branch into: ${TARGET_PROJECT}"
echo "Agents: $(join_by ', ' "${AGENTS[@]}")"
echo "Skills: $(join_by ', ' "${PAYLOAD_SKILLS[@]}")"

declare -a report_lines
report_lines+=("# Formally BMAD DSL Branch Install Report")
report_lines+=("")
report_lines+=("- Target project: \`${TARGET_PROJECT}\`")
report_lines+=("- Agents: \`$(join_by ', ' "${AGENTS[@]}")\`")
report_lines+=("- Dry run: \`$([[ $DRY_RUN -eq 1 ]] && echo yes || echo no)\`")
report_lines+=("- Installed payload: \`$(join_by ', ' "${PAYLOAD_SKILLS[@]}")\`")
report_lines+=("")

for agent in "${AGENTS[@]}"; do
  skill_dir="$(agent_skill_dir "$agent")"
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] mkdir -p ${skill_dir}"
  else
    mkdir -p "$skill_dir"
  fi

  echo "Installing for ${agent}: ${skill_dir}"
  report_lines+=("## ${agent}")
  report_lines+=("")
  report_lines+=("- Skill directory: \`${skill_dir}\`")
  report_lines+=("- Installed skills:")
  for skill in "${PAYLOAD_SKILLS[@]}"; do
    copy_skill_dir "${SKILLS_ROOT}/${skill}" "${skill_dir}/${skill}"
    report_lines+=("  - \`${skill}\`")
  done
  report_lines+=("")
done

report_lines+=("## Notes")
report_lines+=("")
report_lines+=("- This installer copies the isolated DSL setup entrypoint, the DSL steward, the \`formally-bmad-dsl-*\` branch, and the downstream implementation/code-verification companions required by the DSL contract-to-code path.")
report_lines+=("- It does not copy or modify the original \`formally-bmad-formal-*\` branch or its setup/steward entrypoints.")
report_lines+=("- After installation, open the target project in the selected agent runtime and run \`formally-bmad-dsl-setup\` there before starting the DSL branch if the module has not been initialized in that project yet.")

if [[ -n "$REPORT_FILE" ]]; then
  mkdir -p "$(dirname "$REPORT_FILE")"
  printf '%s\n' "${report_lines[@]}" >"$REPORT_FILE"
  echo "Wrote install report: ${REPORT_FILE}"
fi

echo "Install completed."

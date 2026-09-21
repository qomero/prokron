#!/bin/sh
set -eu

mode=${1:-}
target=${2:-.}
retained=0

# Everything Prokron installs lives in one directory (ADR-024). The only paths
# written outside it are the ones an agent host reads by fixed address.
home=.prokron
chronicle="$home/chronicle"
commands="$home/commands"
runtime="$home/runtime"

case "$mode" in
  new|existing) ;;
  *)
    echo "Usage: install.sh new|existing [target-directory]" >&2
    exit 2
    ;;
esac

if [ ! -d "$target" ]; then
  echo "Target directory does not exist: $target" >&2
  exit 2
fi

target=$(CDPATH= cd "$target" && pwd)
source_dir=
temp_dir=

for file in AGENTS.md CLAUDE.md; do
  if [ -L "$target/$file" ] || { [ -e "$target/$file" ] && [ ! -f "$target/$file" ]; }; then
    echo "Cannot install: $target/$file is not a regular file" >&2
    exit 1
  fi
done

case $0 in
  */*)
    candidate=$(CDPATH= cd "$(dirname "$0")" && pwd)
    if [ -f "$candidate/templates/chronicle/README.md" ]; then
      source_dir=$candidate
    fi
    ;;
esac

cleanup() {
  if [ -n "$temp_dir" ]; then
    rm -rf "$temp_dir"
  fi
}
trap cleanup EXIT HUP INT TERM

if [ -z "$source_dir" ]; then
  temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/prokron.XXXXXX")
  command -v tar >/dev/null 2>&1 || { echo "tar is required" >&2; exit 1; }
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    gh api repos/qomero/prokron/tarball/main > "$temp_dir/prokron.tar.gz"
  else
    command -v curl >/dev/null 2>&1 || { echo "curl is required" >&2; exit 1; }
    curl -fsSL "https://github.com/qomero/prokron/archive/refs/heads/main.tar.gz" \
      -o "$temp_dir/prokron.tar.gz"
  fi
  mkdir "$temp_dir/source"
  tar -xzf "$temp_dir/prokron.tar.gz" -C "$temp_dir/source"
  set -- "$temp_dir/source"/*
  source_dir=$1
fi

if [ ! -f "$source_dir/templates/chronicle/README.md" ]; then
  echo "Downloaded Prokron source is incomplete" >&2
  exit 1
fi

copy_new() {
  source_file=$1
  target_file=$2
  if [ -L "$target_file" ] || { [ -e "$target_file" ] && [ ! -f "$target_file" ]; }; then
    echo "Cannot install: $target_file is not a regular file" >&2
    exit 1
  elif [ ! -e "$target_file" ]; then
    mkdir -p "$(dirname "$target_file")"
    cp "$source_file" "$target_file"
  elif ! cmp -s "$source_file" "$target_file"; then
    retained=1
  fi
}

for path in "$home" "$chronicle" "$chronicle/ADR" "$commands" "$runtime" \
  "$runtime/prokron" .claude .claude/commands .opencode .opencode/commands \
  .agents .agents/skills .agents/skills/prokron; do
  if [ -L "$target/$path" ] || { [ -e "$target/$path" ] && [ ! -d "$target/$path" ]; }; then
    echo "Cannot install into linked or non-directory path: $target/$path" >&2
    exit 1
  fi
done
had_chronicle=0
[ ! -d "$target/$chronicle" ] || had_chronicle=1
for file in README PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL; do
  copy_new "$source_dir/templates/chronicle/$file.md" "$target/$chronicle/$file.md"
done
copy_new "$source_dir/templates/chronicle/ADR/README.md" "$target/$chronicle/ADR/README.md"
# Differences in project records are expected, not an upgrade warning.
retained=0
cmp -s "$source_dir/templates/chronicle/README.md" "$target/$chronicle/README.md" || retained=1

for command in init work decide checkpoint resume; do
  copy_new "$source_dir/.prokron/commands/prokron-$command.md" \
    "$target/$commands/prokron-$command.md"
  copy_new "$source_dir/.claude/commands/prokron-$command.md" \
    "$target/.claude/commands/prokron-$command.md"
  copy_new "$source_dir/.opencode/commands/prokron-$command.md" \
    "$target/.opencode/commands/prokron-$command.md"
done
copy_new "$source_dir/.agents/skills/prokron/SKILL.md" \
  "$target/.agents/skills/prokron/SKILL.md"

# The runtime is code, not a record: replace it on every install so a repository
# never runs a stale compiler against a current chronicle.
mkdir -p "$target/$runtime/prokron"
for module in __init__ layout model parse validate analytics views compile migrate \
  mermaid dashboard cli; do
  cp "$source_dir/src/prokron/$module.py" "$target/$runtime/prokron/$module.py"
done
cp "$source_dir/VERSION" "$target/$runtime/VERSION"
cp "$source_dir/.prokron/prokron" "$target/$home/prokron"
chmod +x "$target/$home/prokron"

if [ ! -f "$target/AGENTS.md" ]; then
  cp "$source_dir/AGENTS.md" "$target/AGENTS.md"
elif ! grep -Fq '<!-- project-prokron:start -->' "$target/AGENTS.md"; then
  printf '\n' >> "$target/AGENTS.md"
  cat "$source_dir/AGENTS.md" >> "$target/AGENTS.md"
else
  retained=1
fi

if [ ! -f "$target/CLAUDE.md" ]; then
  printf '@AGENTS.md\n' > "$target/CLAUDE.md"
elif ! grep -Fxq '@AGENTS.md' "$target/CLAUDE.md"; then
  printf '\n@AGENTS.md\n' >> "$target/CLAUDE.md"
fi

printf 'Prokron installed in %s\n\n' "$target"
if grep -q '^## T-' "$target/prokron/TASKS.md" 2>/dev/null; then
  printf 'A v0.2 chronicle was found at prokron/ and the new layout reads %s/.\n' "$chronicle"
  printf 'Your records are intact. Move them with:\n'
  printf '  %s/prokron migrate           # shows what it would do\n' "$home"
  printf '  %s/prokron migrate --apply   # performs it\n\n' "$home"
elif grep -q '^## T-' "$target/$home/TASKS.md" 2>/dev/null; then
  printf 'A v0.1 chronicle was found in %s/ and the new layout cannot read it.\n' "$home"
  printf 'Your records are intact. Move them with:\n'
  printf '  %s/prokron migrate           # shows what it would do\n' "$home"
  printf '  %s/prokron migrate --apply   # performs it, archiving the originals\n\n' "$home"
fi
if [ "$retained" -eq 1 ]; then
  printf 'Existing guidance was preserved; reinstall does not upgrade it.\n'
  printf 'Merge updates using README.md in the Prokron source (Updating an installation).\n\n'
fi
if [ "$had_chronicle" -eq 1 ]; then
  printf 'Existing chronicle preserved. Resume in your agent chat:\n'
  printf '  Codex:       $prokron resume\n'
  printf '  Claude Code / OpenCode: /prokron-resume\n'
  printf '  Other:       Read AGENTS.md, then follow %s/prokron-resume.md.\n' "$commands"
  exit 0
fi
printf 'Start in your agent chat:\n'
printf '  Codex:       $prokron init %s\n' "$mode"
printf '  Claude Code: /prokron-init %s\n' "$mode"
printf '  OpenCode:    /prokron-init %s\n' "$mode"
printf '  Other:       Read AGENTS.md, then follow %s/prokron-init.md in %s mode.\n' \
  "$commands" "$mode"

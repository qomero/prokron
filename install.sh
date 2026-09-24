#!/bin/sh
set -eu

mode=existing
target=.
target_set=0
link=1
ref=
allow_downgrade=${PROKRON_ALLOW_DOWNGRADE:-0}
upgraded=
staged=

# Everything Prokron installs lives in one directory (ADR-024). The only paths
# written outside it are the ones an agent host reads by fixed address, and the
# launcher described below, which goes on the reader's machine (ADR-027).
home=.prokron
chronicle="$home/chronicle"
commands="$home/commands"
runtime="$home/runtime"

# `existing` is the mode almost everyone wants, so installing takes no
# arguments. Both modes stay available, and either may name a target.
while [ $# -gt 0 ]; do
  case $1 in
    new|existing) mode=$1 ;;
    --no-link) link=0 ;;
    --allow-downgrade) allow_downgrade=1 ;;
    --ref)
      [ $# -ge 2 ] && [ -n "$2" ] || { echo "--ref needs a tag or branch" >&2; exit 2; }
      ref=$2
      shift
      ;;
    --ref=*) ref=${1#--ref=} ;;
    -h|--help)
      echo "Usage: install.sh [new|existing] [target-directory] [--no-link] [--ref <tag|branch>] [--allow-downgrade]"
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      echo "Usage: install.sh [new|existing] [target-directory] [--no-link] [--ref <tag|branch>] [--allow-downgrade]" >&2
      exit 2
      ;;
    *)
      # One target, and it must be a directory. Anything else is a typo for a
      # mode, and silently installing somewhere unintended is the worst answer.
      if [ "$target_set" -eq 1 ]; then
        echo "Unexpected argument: $1" >&2
        echo "Usage: install.sh [new|existing] [target-directory] [--no-link] [--ref <tag|branch>] [--allow-downgrade]" >&2
        exit 2
      fi
      target=$1
      target_set=1
      ;;
  esac
  shift
done

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

if [ -n "$source_dir" ] && [ -n "$ref" ]; then
  echo "--ref applies only when the installer downloads Prokron; this one runs from $source_dir" >&2
  exit 2
fi

# The default is the latest published release, not `main`, so two people who
# install on different days get the same runtime (ADR-040).
use_gh=0
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  use_gh=1
fi
downloaded=0
if [ -z "$source_dir" ]; then
  temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/prokron.XXXXXX")
  command -v tar >/dev/null 2>&1 || { echo "tar is required" >&2; exit 1; }
  if [ "$use_gh" -eq 0 ]; then
    command -v curl >/dev/null 2>&1 || { echo "curl is required" >&2; exit 1; }
  fi
  if [ -z "$ref" ]; then
    if [ "$use_gh" -eq 1 ]; then
      ref=$(gh api repos/qomero/prokron/releases/latest --jq .tag_name 2>/dev/null || true)
    else
      latest=$(curl -fsSLI -o /dev/null -w '%{url_effective}' \
        https://github.com/qomero/prokron/releases/latest 2>/dev/null || true)
      case $latest in */releases/tag/*) ref=${latest##*/} ;; esac
    fi
    if [ -z "$ref" ]; then
      echo "No published release was found; installing main." >&2
      ref=main
    fi
  fi
  if [ "$use_gh" -eq 1 ]; then
    gh api "repos/qomero/prokron/tarball/$ref" > "$temp_dir/prokron.tar.gz"
  else
    curl -fsSL "https://github.com/qomero/prokron/archive/$ref.tar.gz" \
      -o "$temp_dir/prokron.tar.gz"
  fi
  mkdir "$temp_dir/source"
  tar -xzf "$temp_dir/prokron.tar.gz" -C "$temp_dir/source"
  set -- "$temp_dir/source"/*
  source_dir=$1
  downloaded=1
fi

if [ ! -f "$source_dir/templates/chronicle/README.md" ]; then
  echo "Downloaded Prokron source is incomplete" >&2
  exit 1
fi

# An older runtime replacing a newer one silently loses whatever the newer one
# understood, so it takes an explicit flag (ADR-040).
version_older() {
  # True when $1 sorts strictly before $2 as a dotted version.
  [ "$1" != "$2" ] || return 1
  lowest=$(printf '%s\n%s\n' "$1" "$2" | sort -t. -k1,1n -k2,2n -k3,3n | head -n 1)
  [ "$lowest" = "$1" ]
}
incoming=$(cat "$source_dir/VERSION" 2>/dev/null || echo 0)
present=$(cat "$target/.prokron/runtime/VERSION" 2>/dev/null || true)
if [ -n "$present" ] && version_older "$incoming" "$present" && [ "$allow_downgrade" != 1 ]; then
  echo "Refusing to install prokron $incoming over the newer $present already in $target." >&2
  echo "Pass --allow-downgrade if that is intended." >&2
  exit 1
fi

# A downloaded release installs itself, exactly as it shipped: its own
# installer knows its own files (ADR-040).
if [ "$downloaded" -eq 1 ]; then
  printf 'Installing prokron %s (%s)\n' "$incoming" "$ref"
  set -- "$mode" "$target"
  [ "$link" -eq 1 ] || set -- "$@" --no-link
  status=0
  PROKRON_ALLOW_DOWNGRADE=$allow_downgrade sh "$source_dir/install.sh" "$@" || status=$?
  exit "$status"
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
  fi
}

# Guidance is what Prokron tells people and agents to do. The runtime is
# replaced on every install, so guidance must keep up with it — without ever
# overwriting what a person edited (ADR-040). The previous install recorded a
# checksum of each guidance file it wrote; a file that still matches was never
# touched and is replaced, and one that differs is kept and the new version is
# staged beside it for review.
manifest="$target/$runtime/GUIDANCE"
previous=
if [ -f "$manifest" ] && [ ! -L "$manifest" ]; then
  previous=$(cat "$manifest")
fi
recorded=

sum_of() {
  cksum < "$1" | awk '{ print $1 "-" $2 }'
}

previous_sum() {
  printf '%s\n' "$previous" | awk -v key="$1" '$2 == key { print $1; exit }'
}

record() {
  recorded="$recorded$1 $2
"
}

stage() {
  # $1 source, $2 key: the new version, at the key's path under upgrade/.
  mkdir -p "$(dirname "$target/$home/upgrade/$2")"
  cp "$1" "$target/$home/upgrade/$2"
  staged="$staged  $2
"
}

install_guidance() {
  source_file=$1
  key=$2
  target_file="$target/$key"
  if [ -L "$target_file" ] || { [ -e "$target_file" ] && [ ! -f "$target_file" ]; }; then
    echo "Cannot install: $target_file is not a regular file" >&2
    exit 1
  elif [ ! -e "$target_file" ]; then
    mkdir -p "$(dirname "$target_file")"
    cp "$source_file" "$target_file"
    record "$(sum_of "$source_file")" "$key"
  elif cmp -s "$source_file" "$target_file"; then
    record "$(sum_of "$target_file")" "$key"
  else
    was=$(previous_sum "$key")
    if [ -n "$was" ] && [ "$was" = "$(sum_of "$target_file")" ]; then
      cp "$source_file" "$target_file"
      record "$(sum_of "$source_file")" "$key"
      upgraded="$upgraded  $key
"
    else
      stage "$source_file" "$key"
      [ -z "$was" ] || record "$was" "$key"
    fi
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
# Records are the project's own: a template is only ever a starting point.
for file in THESIS PHASES MODULES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL TRACE TECH_DEBT; do
  copy_new "$source_dir/templates/chronicle/$file.md" "$target/$chronicle/$file.md"
done
copy_new "$source_dir/templates/chronicle/ADR/README.md" "$target/$chronicle/ADR/README.md"
install_guidance "$source_dir/templates/chronicle/README.md" "$chronicle/README.md"

for command in init work decide checkpoint resume baseline; do
  install_guidance "$source_dir/.prokron/commands/prokron-$command.md" \
    "$commands/prokron-$command.md"
  install_guidance "$source_dir/.claude/commands/prokron-$command.md" \
    ".claude/commands/prokron-$command.md"
  install_guidance "$source_dir/.opencode/commands/prokron-$command.md" \
    ".opencode/commands/prokron-$command.md"
done
install_guidance "$source_dir/.agents/skills/prokron/SKILL.md" \
  ".agents/skills/prokron/SKILL.md"

# The runtime is code, not a record: replace it on every install so a repository
# never runs a stale compiler against a current chronicle.
mkdir -p "$target/$runtime/prokron"
for module in __init__ layout model parse domain validate analytics views index compile migrate \
  mermaid dashboard retrieve codegraph cli; do
  cp "$source_dir/src/prokron/$module.py" "$target/$runtime/prokron/$module.py"
done
cp "$source_dir/VERSION" "$target/$runtime/VERSION"
cp "$source_dir/.prokron/prokron" "$target/$home/prokron"
chmod +x "$target/$home/prokron"

# A path is not a command. The launcher below goes on the reader's PATH so the
# command is `prokron`; it holds no logic of its own, walking up to the nearest
# project and running that project's runtime, so two repositories on different
# releases each keep their own (ADR-027).
#
# It creates no directory, edits no shell configuration, and never replaces a
# `prokron` it did not write.
linked=
if [ "$link" -eq 1 ]; then
  for dir in "${HOME:-}/.local/bin" "${HOME:-}/bin" /usr/local/bin; do
    [ -n "$dir" ] && [ -d "$dir" ] && [ -w "$dir" ] || continue
    case ":${PATH:-}:" in *":$dir:"*) ;; *) continue ;; esac
    if [ -e "$dir/prokron" ] && ! grep -q 'prokron-launcher' "$dir/prokron" 2>/dev/null; then
      continue
    fi
    cat > "$dir/prokron" <<'LAUNCHER'
#!/bin/sh
# prokron-launcher: run the nearest project's own copy of Prokron.
set -eu
dir=$(pwd -P)
while :; do
  if [ -x "$dir/.prokron/prokron" ]; then
    exec "$dir/.prokron/prokron" "$@"
  fi
  [ "$dir" != "/" ] || break
  dir=$(dirname "$dir")
done
echo "No .prokron/ in $(pwd) or any parent directory." >&2
echo "Install Prokron in this project with:" >&2
echo "  curl -fsSL https://raw.githubusercontent.com/qomero/prokron/main/install.sh | sh" >&2
exit 2
LAUNCHER
    chmod +x "$dir/prokron"
    linked=$dir
    break
  done
fi

# Generated views are neither records nor guidance: they are reproducible from
# the chronicle, so an upgrade refreshes them rather than leaving a current
# runtime beside a page the previous release wrote (ADR-031). Only when the
# installation already has views and the chronicle holds work — never on a
# fresh install, where compiled state still appears only after compiling.
refreshed=
if [ -d "$target/$home/compiled" ] && grep -q '^## T-' "$target/$chronicle/TASKS.md" 2>/dev/null; then
  if (
    cd "$target" \
      && "$home/prokron" compile >/dev/null 2>&1 \
      && "$home/prokron" graph >/dev/null 2>&1 \
      && "$home/prokron" dashboard >/dev/null 2>&1
  ); then
    refreshed=done
  else
    refreshed=failed
  fi
fi

# A Prokron block shares a file with the project's own rules: AGENTS.md for
# every agent, CLAUDE.md for Claude Code. Only the text between the markers is
# ever compared or replaced; everything around it is left exactly as it was.
install_block() {
  # $1 file (relative), $2 source block, $3 start marker, $4 end marker,
  # $5 manifest key, $6 label for the output.
  file="$target/$1"
  if [ ! -f "$file" ]; then
    cp "$2" "$file"
    record "$(sum_of "$2")" "$5"
  elif ! grep -Fq "$3" "$file"; then
    printf '\n' >> "$file"
    cat "$2" >> "$file"
    record "$(sum_of "$2")" "$5"
  else
    block="$target/$runtime/block.tmp"
    awk -v s="$3" -v e="$4" '
      index($0, s) && !seen { on = 1; seen = 1 }
      on { print }
      on && index($0, e) { on = 0; closed = 1 }
      END { if (!closed) exit 3 }
    ' "$file" > "$block" && complete=1 || complete=0
    if [ "$complete" -eq 1 ] && cmp -s "$2" "$block"; then
      record "$(sum_of "$block")" "$5"
    else
      was=$(previous_sum "$5")
      if [ "$complete" -eq 1 ] && [ -n "$was" ] && [ "$was" = "$(sum_of "$block")" ]; then
        awk -v s="$3" -v e="$4" -v src="$2" '
          index($0, s) && !done { while ((getline line < src) > 0) print line; skip = 1; done = 1; next }
          skip { if (index($0, e)) skip = 0; next }
          { print }
        ' "$file" > "$file.prokron-new"
        cat "$file.prokron-new" > "$file"
        rm -f "$file.prokron-new"
        record "$(sum_of "$2")" "$5"
        upgraded="$upgraded  $6
"
      else
        stage "$2" "$1"
        [ -z "$was" ] || record "$was" "$5"
      fi
    fi
    rm -f "$block"
  fi
}
install_block AGENTS.md "$source_dir/AGENTS.md" '<!-- project-prokron:start -->' \
  '<!-- project-prokron:end -->' 'AGENTS.md#prokron' 'AGENTS.md (Prokron block)'

# Claude Code reads CLAUDE.md, which imports AGENTS.md and carries the
# Claude-specific entry order (ADR-047).
if [ ! -f "$target/CLAUDE.md" ]; then
  printf '@AGENTS.md\n' > "$target/CLAUDE.md"
elif ! grep -Fxq '@AGENTS.md' "$target/CLAUDE.md"; then
  printf '\n@AGENTS.md\n' >> "$target/CLAUDE.md"
fi
if [ -f "$source_dir/templates/claude/CLAUDE.md" ]; then
  install_block CLAUDE.md "$source_dir/templates/claude/CLAUDE.md" \
    '<!-- project-prokron-claude:start -->' '<!-- project-prokron-claude:end -->' \
    'CLAUDE.md#prokron' 'CLAUDE.md (Prokron block)'
fi
printf '%s' "$recorded" > "$manifest"

# In a Git repository, append-only records merge by union, so two branches
# that each add a journal entry or an ADR do not conflict, and compiled output
# is marked generated (ADR-041). The block is Prokron's; the rest of the file
# is the project's and is left as it was.
if [ -e "$target/.git" ]; then
  attributes="$target/.gitattributes"
  if [ -L "$attributes" ] || { [ -e "$attributes" ] && [ ! -f "$attributes" ]; }; then
    echo "Cannot install: $attributes is not a regular file" >&2
    exit 1
  fi
  block_file="$target/$runtime/gitattributes.tmp"
  cat > "$block_file" <<'ATTRIBUTES'
# prokron:start — maintained by the Prokron installer (ADR-041)
.prokron/chronicle/JOURNAL.md merge=union
.prokron/chronicle/ADR/README.md merge=union
.prokron/compiled/** linguist-generated=true
.prokron/chronicle/INDEX.md linguist-generated=true
# prokron:end
ATTRIBUTES
  if [ ! -f "$attributes" ]; then
    cp "$block_file" "$attributes"
  elif ! grep -Fq '# prokron:start' "$attributes"; then
    [ ! -s "$attributes" ] || [ -z "$(tail -c 1 "$attributes")" ] || printf '\n' >> "$attributes"
    cat "$block_file" >> "$attributes"
  else
    awk -v src="$block_file" '
      /^# prokron:start/ && !done { while ((getline line < src) > 0) print line; skip = 1; done = 1; next }
      skip { if (/^# prokron:end/) skip = 0; next }
      { print }
    ' "$attributes" > "$attributes.prokron-new"
    cat "$attributes.prokron-new" > "$attributes"
    rm -f "$attributes.prokron-new"
  fi
  rm -f "$block_file"
fi


printf 'Prokron installed in %s\n' "$target"
if [ -n "$linked" ]; then
  printf 'The command is `prokron`, linked in %s\n\n' "$linked"
elif [ "$link" -eq 1 ]; then
  printf 'Run it as `%s/prokron`, or put it on your PATH:\n' "$home"
  printf '  alias prokron="%s/prokron"\n\n' "$home"
else
  printf 'Run it as `%s/prokron`.\n\n' "$home"
fi
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
if [ "$refreshed" = done ]; then
  printf 'Generated views were refreshed by the new runtime.\n\n'
elif [ "$refreshed" = failed ]; then
  printf 'Generated views could not be refreshed and are still the previous\n'
  printf 'version'"'"'s. Your records are untouched. Fix what `%s/prokron validate`\n' "$home"
  printf 'reports, then run:\n'
  printf '  %s/prokron compile && %s/prokron graph && %s/prokron dashboard\n\n' "$home" "$home" "$home"
fi
if [ -n "$upgraded" ]; then
  printf 'Guidance upgraded, unedited since the last install:\n%s\n' "$upgraded"
fi
if [ -n "$staged" ]; then
  printf 'Guidance kept because it was edited; the new version is beside it in %s/upgrade/:\n%s' "$home" "$staged"
  printf 'Merge what you want, then delete %s/upgrade/.\n\n' "$home"
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

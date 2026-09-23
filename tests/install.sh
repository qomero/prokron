#!/bin/sh
set -eu

root=$(CDPATH= cd "$(dirname "$0")/.." && pwd)
fixture=$(mktemp -d "${TMPDIR:-/tmp}/prokron-install.XXXXXX")
# A directory with no Prokron above it, for checking what happens outside a
# project. It cannot live under the fixture, which is itself an installation.
outside=$(mktemp -d "${TMPDIR:-/tmp}/prokron-outside.XXXXXX")
trap 'rm -rf "$fixture" "$outside"' EXIT HUP INT TERM

printf '# Keep agent rules\n' > "$fixture/AGENTS.md"
printf '# Keep Claude rules\n' > "$fixture/CLAUDE.md"
"$root/install.sh" existing "$fixture" --no-link > "$fixture/output"

for file in README PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL TRACE; do
  test -f "$fixture/.prokron/chronicle/$file.md"
done
test -f "$fixture/.prokron/chronicle/ADR/README.md"
# Authority never lands in the compiled directory.
for file in PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL DECISIONS; do
  test ! -e "$fixture/.prokron/compiled/$file.md"
done
test ! -e "$fixture/.prokron/chronicle/DECISIONS.md"
test -f "$fixture/.agents/skills/prokron/SKILL.md"

# Everything Prokron chooses for itself lives in one directory. What is left
# outside it is only what an agent host reads by fixed address.
installed=$(cd "$fixture" && ls -A | LC_ALL=C sort | tr '\n' ' ')
expected='.agents .claude .opencode .prokron AGENTS.md CLAUDE.md output '
test "$installed" = "$expected" || {
  echo "Install placed unexpected entries at the root: $installed" >&2
  exit 1
}

# The runtime ships with the chronicle and runs in the installed repository.
test -x "$fixture/.prokron/prokron"
test -f "$fixture/.prokron/runtime/prokron/cli.py"
# Every runtime module must be installed, or the tool breaks in the target repo.
for module in "$root"/src/prokron/*.py; do
  test -f "$fixture/.prokron/runtime/prokron/$(basename "$module")"
done
"$fixture/.prokron/prokron" --version | grep -Fq "prokron $(cat "$root/VERSION")"
# The runtime reports its own version, never the tracked project's.
printf '9.9.9\n' > "$fixture/VERSION"
"$fixture/.prokron/prokron" --version | grep -Fvq '9.9.9'
rm "$fixture/VERSION"
(cd "$fixture" && .prokron/prokron validate) | grep -Fq 'consistent'
(cd "$fixture" && .prokron/prokron compile) >/dev/null
test -f "$fixture/.prokron/compiled/project.json"
(cd "$fixture" && .prokron/prokron status) | grep -Fq 'tasks'
# Compiled state is disposable: deleting it loses nothing.
cp -R "$fixture/.prokron/compiled" "$fixture/first-compile"
rm -rf "$fixture/.prokron/compiled"
(cd "$fixture" && .prokron/prokron compile) >/dev/null
for file in project.json README.md STATE.md TASK_GRAPH.md; do
  cmp "$fixture/first-compile/$file" "$fixture/.prokron/compiled/$file"
done
rm -rf "$fixture/first-compile"

for command in init work decide checkpoint resume baseline; do
  test -f "$fixture/.prokron/commands/prokron-$command.md"
  test -f "$fixture/.claude/commands/prokron-$command.md"
  test -f "$fixture/.opencode/commands/prokron-$command.md"
done
# Initialization records nothing about the past on its own; the baseline is a
# separate workflow the owner has to ask for (ADR-037).
if ls "$fixture/.prokron/chronicle/ADR/"ADR-*.md >/dev/null 2>&1; then
  echo "a fresh install must contain no ADR" >&2
  exit 1
fi
grep -Fq 'only when the project owner explicitly asks' \
  "$fixture/.prokron/commands/prokron-baseline.md"
grep -Fq 'initialization never runs it' "$fixture/.prokron/commands/prokron-init.md"
grep -Fq '/prokron-baseline' "$fixture/AGENTS.md"
grep -Fq 'baseline' "$fixture/.agents/skills/prokron/SKILL.md"
grep -Fq '.prokron/commands/prokron-baseline.md' "$fixture/.claude/commands/prokron-baseline.md"
grep -Fq 'Origin: RECONSTRUCTED' "$fixture/.prokron/chronicle/ADR/README.md"
# A host command file must name a document that was actually installed.
grep -Fq '.prokron/commands/prokron-work.md' "$fixture/.claude/commands/prokron-work.md"
grep -Fq '# Keep agent rules' "$fixture/AGENTS.md"
grep -Fq '# Keep Claude rules' "$fixture/CLAUDE.md"
grep -Fq 'do not wait for a Prokron command' "$fixture/AGENTS.md"
grep -Fq 'context, token, time, session, rate, or quota limit' "$fixture/AGENTS.md"
grep -Fq 'Record every new work request as a task before implementation' \
  "$fixture/.prokron/chronicle/README.md"
grep -Fq 'Append an ADR as soon as a material choice is made' \
  "$fixture/.prokron/chronicle/README.md"
grep -Fq 'Do not edit' "$fixture/.prokron/compiled/README.md"
grep -Fq 'Given <precondition>' "$fixture/.prokron/chronicle/ACCEPTANCE.md"
grep -Fq 'ACCEPTANCE_FAILURE' "$fixture/.prokron/chronicle/ACCEPTANCE.md"
grep -Fq 'Exit authority' "$fixture/.prokron/chronicle/PHASES.md"
# A project can name itself; the field ships present and empty so the next
# project is shown it exists without being made to fill it (ADR-030).
grep -Eq '^Project:' "$fixture/.prokron/chronicle/PHASES.md"
grep -Fq '$prokron init existing' "$fixture/output"
grep -Fq '/prokron-init existing' "$fixture/output"
grep -Fq '.prokron/commands/prokron-init.md in existing mode' "$fixture/output"

grep -Fq '$ARGUMENTS' "$fixture/.opencode/commands/prokron-decide.md"

# Both entry modes must preserve every record and customized instruction.
for file in README PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL; do
  printf '\nKEEP %s\n' "$file" >> "$fixture/.prokron/chronicle/$file.md"
done
printf '\nKEEP ADR\n' >> "$fixture/.prokron/chronicle/ADR/README.md"
printf '\nCUSTOM\n' >> "$fixture/.prokron/commands/prokron-work.md"
cp -R "$fixture/.prokron/chronicle" "$fixture/saved"
cp "$fixture/.prokron/commands/prokron-work.md" "$fixture/saved-work"
cp "$fixture/AGENTS.md" "$fixture/saved-agents"
cp "$fixture/CLAUDE.md" "$fixture/saved-claude"
for mode in existing new; do
  "$root/install.sh" "$mode" "$fixture" --no-link > "$fixture/output"
  for file in README PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL; do
    cmp "$fixture/saved/$file.md" "$fixture/.prokron/chronicle/$file.md"
  done
  cmp "$fixture/saved/ADR/README.md" "$fixture/.prokron/chronicle/ADR/README.md"
  cmp "$fixture/saved-work" "$fixture/.prokron/commands/prokron-work.md"
  cmp "$fixture/saved-agents" "$fixture/AGENTS.md"
  cmp "$fixture/saved-claude" "$fixture/CLAUDE.md"
  grep -Fq 'Guidance kept because it was edited' "$fixture/output"
  grep -Fq '.prokron/commands/prokron-work.md' "$fixture/output"
  test -f "$fixture/.prokron/upgrade/.prokron/commands/prokron-work.md"
  grep -Fq '$prokron resume' "$fixture/output"
done
test "$(grep -Fc '<!-- project-prokron:start -->' "$fixture/AGENTS.md")" -eq 1
test "$(grep -Fxc '@AGENTS.md' "$fixture/CLAUDE.md")" -eq 1

# Guidance keeps up with the runtime (ADR-040). A release that changes its
# guidance replaces what nobody edited and stages what somebody did.
make_source() {
  # $1: a copy of this source whose guidance says something new.
  mkdir -p "$1"
  (cd "$root" && tar -cf - --exclude ./.git .) | (cd "$1" && tar -xf -)
  for file in "$1"/.prokron/commands/prokron-*.md "$1"/.claude/commands/prokron-*.md \
    "$1"/.opencode/commands/prokron-*.md "$1/.agents/skills/prokron/SKILL.md" \
    "$1/templates/chronicle/README.md"; do
    printf '\nNEW GUIDANCE %s\n' "$2" >> "$file"
  done
  awk -v tag="$2" '/<!-- project-prokron:end -->/ { print "NEW BLOCK " tag } { print }' \
    "$1/AGENTS.md" > "$1/AGENTS.tmp" && mv "$1/AGENTS.tmp" "$1/AGENTS.md"
}
outside_block() {
  awk '/<!-- project-prokron:start -->/ { on = 1 } !on { print } /<!-- project-prokron:end -->/ { on = 0 }' "$1"
}
records_of() {
  for file in PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL; do
    cksum < "$1/.prokron/chronicle/$file.md"
  done
  cksum < "$1/.prokron/chronicle/ADR/README.md"
}
guide="$fixture/guidance"
mkdir -p "$guide"
printf '# Before\n' > "$guide/AGENTS.md"
"$root/install.sh" "$guide" --no-link >/dev/null
test -f "$guide/.prokron/runtime/GUIDANCE"
printf '\n# After\n' >> "$guide/AGENTS.md"
printf '\n## T-001: Real work\n- Status: TODO\n- Phase: P-NONE\n- Validation: UNTESTED\n- Dependencies: none\n- AC: AC-T-001\n- Evidence:\n- Governed by: none\n' >> "$guide/.prokron/chronicle/TASKS.md"
printf '\nCUSTOM WORK\n' >> "$guide/.prokron/commands/prokron-work.md"
cp "$guide/.prokron/commands/prokron-work.md" "$fixture/custom-work"
outside_block "$guide/AGENTS.md" > "$fixture/outside-before"
records_of "$guide" > "$fixture/records-before"
make_source "$fixture/source-two" two
"$fixture/source-two/install.sh" "$guide" --no-link > "$guide/output"
# Unedited guidance is replaced, and named.
for command in init decide checkpoint resume baseline; do
  cmp "$fixture/source-two/.prokron/commands/prokron-$command.md" "$guide/.prokron/commands/prokron-$command.md"
done
for command in init work decide checkpoint resume baseline; do
  cmp "$fixture/source-two/.claude/commands/prokron-$command.md" "$guide/.claude/commands/prokron-$command.md"
  cmp "$fixture/source-two/.opencode/commands/prokron-$command.md" "$guide/.opencode/commands/prokron-$command.md"
done
cmp "$fixture/source-two/.agents/skills/prokron/SKILL.md" "$guide/.agents/skills/prokron/SKILL.md"
cmp "$fixture/source-two/templates/chronicle/README.md" "$guide/.prokron/chronicle/README.md"
grep -Fq 'NEW BLOCK two' "$guide/AGENTS.md"
test "$(grep -Fc '<!-- project-prokron:start -->' "$guide/AGENTS.md")" -eq 1
grep -Fq 'Guidance upgraded' "$guide/output"
grep -Fq '.claude/commands/prokron-init.md' "$guide/output"
grep -Fq 'AGENTS.md (Prokron block)' "$guide/output"
# Only the block moved; the project's own rules around it did not.
outside_block "$guide/AGENTS.md" | cmp "$fixture/outside-before" -
# Edited guidance stays exactly as it was, with the new version beside it.
cmp "$fixture/custom-work" "$guide/.prokron/commands/prokron-work.md"
cmp "$fixture/source-two/.prokron/commands/prokron-work.md" \
  "$guide/.prokron/upgrade/.prokron/commands/prokron-work.md"
grep -Fq 'Guidance kept because it was edited' "$guide/output"
records_of "$guide" | cmp "$fixture/records-before" -

# An edited Prokron block is kept and staged like any other edited guidance.
awk '/<!-- project-prokron:end -->/ { print "MY OWN RULE" } { print }' "$guide/AGENTS.md" > "$guide/AGENTS.tmp"
mv "$guide/AGENTS.tmp" "$guide/AGENTS.md"
cp "$guide/AGENTS.md" "$fixture/custom-agents"
make_source "$fixture/source-three" three
"$fixture/source-three/install.sh" "$guide" --no-link > "$guide/output"
cmp "$fixture/custom-agents" "$guide/AGENTS.md"
cmp "$fixture/source-three/AGENTS.md" "$guide/.prokron/upgrade/AGENTS.md"
grep -Fq 'NEW GUIDANCE three' "$guide/.prokron/commands/prokron-init.md"
records_of "$guide" | cmp "$fixture/records-before" -

# With no record of what was installed, a difference can only mean an edit.
rm "$guide/.prokron/runtime/GUIDANCE"
cp "$guide/.prokron/commands/prokron-init.md" "$fixture/unrecorded-init"
make_source "$fixture/source-four" four
"$fixture/source-four/install.sh" "$guide" --no-link > "$guide/output"
cmp "$fixture/unrecorded-init" "$guide/.prokron/commands/prokron-init.md"
cmp "$fixture/source-four/.prokron/commands/prokron-init.md" \
  "$guide/.prokron/upgrade/.prokron/commands/prokron-init.md"
records_of "$guide" | cmp "$fixture/records-before" -

# An older runtime does not replace a newer one unless asked to.
printf '999.0.0\n' > "$guide/.prokron/runtime/VERSION"
snapshot() { (cd "$1" && find . -type f ! -name output -exec cksum {} + | LC_ALL=C sort); }
snapshot "$guide" > "$fixture/before-downgrade"
if "$root/install.sh" "$guide" --no-link > "$guide/output" 2>&1; then
  echo "an older runtime replaced a newer one" >&2
  exit 1
fi
grep -Fq 'Refusing to install' "$guide/output"
snapshot "$guide" | cmp "$fixture/before-downgrade" -
"$root/install.sh" "$guide" --no-link --allow-downgrade >/dev/null
cmp "$root/VERSION" "$guide/.prokron/runtime/VERSION"
records_of "$guide" | cmp "$fixture/records-before" -
# `--ref` names what to download; it means nothing to a local source.
if "$root/install.sh" "$guide" --no-link --ref v0.4.6 >/dev/null 2>&1; then
  exit 1
fi

# A Git repository gets one marked .gitattributes block, and parallel appends
# to the journal and the ADR index merge without conflict (ADR-041).
test ! -e "$fixture/.gitattributes"
repo="$fixture/gitrepo"
mkdir -p "$repo"
( cd "$repo" && git init -q -b main )
printf '*.png binary\n' > "$repo/.gitattributes"
"$root/install.sh" "$repo" --no-link >/dev/null
"$root/install.sh" "$repo" --no-link >/dev/null
test "$(grep -c '^# prokron:start' "$repo/.gitattributes")" -eq 1
grep -Fxq '*.png binary' "$repo/.gitattributes"
grep -Fxq '.prokron/chronicle/JOURNAL.md merge=union' "$repo/.gitattributes"
grep -Fxq '.prokron/chronicle/ADR/README.md merge=union' "$repo/.gitattributes"
grep -Fxq '.prokron/compiled/** linguist-generated=true' "$repo/.gitattributes"
g() { git -C "$repo" -c user.name=test -c user.email=test@example.com "$@"; }
g add -A && g commit -qm base
g checkout -qb one
printf '\n## 2026-01-01 — T-ONE\n\n- Did: one.\n' >> "$repo/.prokron/chronicle/JOURNAL.md"
printf -- '- [ADR-001](ADR-001.md) — One (ACCEPTED)\n' >> "$repo/.prokron/chronicle/ADR/README.md"
g commit -qam one
g checkout -q main
g checkout -qb two
printf '\n## 2026-01-01 — T-TWO\n\n- Did: two.\n' >> "$repo/.prokron/chronicle/JOURNAL.md"
printf -- '- [ADR-002](ADR-002.md) — Two (ACCEPTED)\n' >> "$repo/.prokron/chronicle/ADR/README.md"
g commit -qam two
g merge -q --no-edit one
grep -Fq 'T-ONE' "$repo/.prokron/chronicle/JOURNAL.md"
grep -Fq 'T-TWO' "$repo/.prokron/chronicle/JOURNAL.md"
grep -Fq 'ADR-001' "$repo/.prokron/chronicle/ADR/README.md"
grep -Fq 'ADR-002' "$repo/.prokron/chronicle/ADR/README.md"
if grep -q '^<<<<<<<' "$repo/.prokron/chronicle/JOURNAL.md" "$repo/.prokron/chronicle/ADR/README.md"; then
  exit 1
fi

mkdir "$fixture/new project"
"$root/install.sh" new "$fixture/new project" --no-link > "$fixture/output-new"
grep -Fq '$prokron init new' "$fixture/output-new"

# An interrupted installation can be repaired without resetting existing tasks.
mkdir -p "$fixture/partial/.prokron/chronicle"
cp "$fixture/saved/TASKS.md" "$fixture/partial/.prokron/chronicle/TASKS.md"
"$root/install.sh" existing "$fixture/partial" --no-link >/dev/null
cmp "$fixture/saved/TASKS.md" "$fixture/partial/.prokron/chronicle/TASKS.md"
for file in README PHASES ACCEPTANCE INTENT HANDOFF JOURNAL; do
  cmp "$root/templates/chronicle/$file.md" "$fixture/partial/.prokron/chronicle/$file.md"
done
cmp "$root/templates/chronicle/ADR/README.md" \
  "$fixture/partial/.prokron/chronicle/ADR/README.md"
# compiled state appears only after compiling
test ! -d "$fixture/partial/.prokron/compiled"

# Upgrading over existing generated views must refresh them. Every other case
# in this suite installs into a directory that has none, which is exactly why
# this defect shipped: the upgrade path had never been exercised (ADR-031).
upgrade="$fixture/upgrade"
mkdir -p "$upgrade"
"$root/install.sh" "$upgrade" --no-link >/dev/null
printf '\n## T-001: Real work\n- Status: DONE\n- Phase: P-NONE\n- Validation: SYNTHETIC\n- Dependencies: none\n- AC: AC-T-001\n- Evidence: recorded\n- Governed by: none\n' >> "$upgrade/.prokron/chronicle/TASKS.md"
printf '\n## AC-T-001 — Real work\n\n- `AC-T-001-01` — It exists. `INSPECTION` · `PASS`\n  - Evidence: it does.\n' >> "$upgrade/.prokron/chronicle/ACCEPTANCE.md"
( cd "$upgrade" && .prokron/prokron compile >/dev/null && .prokron/prokron dashboard >/dev/null )
# Stand in for output written by an older release.
printf 'STALE\n' > "$upgrade/.prokron/compiled/dashboard.html"
printf 'STALE\n' > "$upgrade/.prokron/compiled/STATE.md"
"$root/install.sh" "$upgrade" --no-link > "$upgrade/output"
grep -Fq 'Generated views were refreshed' "$upgrade/output"
grep -Fvq 'STALE' "$upgrade/.prokron/compiled/dashboard.html"
grep -Fvq 'STALE' "$upgrade/.prokron/compiled/STATE.md"
grep -Fq 'generatorVersion' "$upgrade/.prokron/compiled/project.json"
# The refreshed views must come from the version that just installed.
grep -Fq "\"generatorVersion\": \"$(cat "$root/VERSION")\"" "$upgrade/.prokron/compiled/project.json"

# Authority that does not validate must not fail the installation, and must
# not leave the reader guessing what to do.
printf '\n## T-BROKEN: Bad\n- Status: DONE\n- Phase: P-NONE\n- Validation: SYNTHETIC\n- Dependencies: T-GHOST\n- AC: AC-T-NOPE\n- Evidence: x\n- Governed by: none\n' >> "$upgrade/.prokron/chronicle/TASKS.md"
"$root/install.sh" "$upgrade" --no-link > "$upgrade/output-broken"
grep -Fq 'could not be refreshed' "$upgrade/output-broken"
grep -Fq 'prokron compile' "$upgrade/output-broken"
grep -Fq 'T-BROKEN' "$upgrade/.prokron/chronicle/TASKS.md"

# A stale installation is visible to someone who never reinstalls.
stale="$fixture/stale"
mkdir -p "$stale"
"$root/install.sh" "$stale" --no-link >/dev/null
printf '\n## T-001: Real work\n- Status: DONE\n- Phase: P-NONE\n- Validation: SYNTHETIC\n- Dependencies: none\n- AC: AC-T-001\n- Evidence: recorded\n- Governed by: none\n' >> "$stale/.prokron/chronicle/TASKS.md"
printf '\n## AC-T-001 — Real work\n\n- `AC-T-001-01` — It exists. `INSPECTION` · `PASS`\n  - Evidence: it does.\n' >> "$stale/.prokron/chronicle/ACCEPTANCE.md"
( cd "$stale" && .prokron/prokron compile >/dev/null )
sed 's/"generatorVersion": "[^"]*"/"generatorVersion": "0.0.1"/' \
  "$stale/.prokron/compiled/project.json" > "$stale/patched.json"
mv "$stale/patched.json" "$stale/.prokron/compiled/project.json"
( cd "$stale" && .prokron/prokron status ) | grep -Fq 'written by prokron 0.0.1'

# Upgrading a v0.2 project must relocate its chronicle without rewriting it.
legacy2="$fixture/v02"
mkdir -p "$legacy2/prokron/ADR" "$legacy2/.prokron" "$legacy2/commands" "$legacy2/bin"
mkdir -p "$legacy2/.prokron-runtime/prokron" "$legacy2/.claude/commands"
cp "$root"/templates/chronicle/*.md "$legacy2/prokron/"
cp "$root/templates/chronicle/ADR/README.md" "$legacy2/prokron/ADR/README.md"
printf '\n## T-V02-01: Carry a record across the move\n- Status: TODO\n- Phase: P-NONE\n- Validation: UNTESTED\n- Dependencies: none\n- AC: AC-T-V02-01\n- Evidence: —\n- Governed by: ADR-001\n' >> "$legacy2/prokron/TASKS.md"
printf '\n## AC-T-V02-01 — Carry a record across the move\n\n- `AC-T-V02-01-01` — It survived. `INSPECTION` · `NOT_RUN`\n  - Evidence: —\n' >> "$legacy2/prokron/ACCEPTANCE.md"
printf '# ADR-001: Keep it\n- Date: 2026-01-01\n- Status: ACCEPTED\n- Decision: Keep it.\n' > "$legacy2/prokron/ADR/ADR-001.md"
printf 'stale\n' > "$legacy2/.prokron/STATE.md"
printf 'stale\n' > "$legacy2/.prokron/task-graph.mmd"
printf 'Follow `commands/prokron-work.md`.\n' > "$legacy2/.claude/commands/prokron-work.md"
printf 'CUSTOM WORK\n' > "$legacy2/commands/prokron-work.md"
printf 'old\n' > "$legacy2/.prokron-runtime/prokron/cli.py"
printf 'old\n' > "$legacy2/bin/prokron"
cp "$legacy2/prokron/TASKS.md" "$fixture/saved-v02-tasks"
"$root/install.sh" existing "$legacy2" --no-link > "$legacy2/output"
grep -Fq 'A v0.2 chronicle was found' "$legacy2/output"
( cd "$legacy2" && .prokron/prokron status ) | grep -Fq 'Run `prokron migrate`'
( cd "$legacy2" && .prokron/prokron migrate ) | grep -Fq 'Nothing was changed'
test -f "$legacy2/prokron/TASKS.md"
( cd "$legacy2" && .prokron/prokron migrate --apply ) | grep -Fq 'Relocated'
# A relocation moves records; it never rewrites them.
cmp "$fixture/saved-v02-tasks" "$legacy2/.prokron/chronicle/TASKS.md"
test -f "$legacy2/.prokron/chronicle/ADR/ADR-001.md"
grep -Fq 'CUSTOM WORK' "$legacy2/.prokron/commands/prokron-work.md"
grep -Fq '.prokron/commands/prokron-work.md' "$legacy2/.claude/commands/prokron-work.md"
test ! -e "$legacy2/prokron"
test ! -e "$legacy2/commands"
test ! -e "$legacy2/bin"
test ! -e "$legacy2/.prokron-runtime"
test ! -e "$legacy2/.prokron/STATE.md"
test ! -e "$legacy2/.prokron/task-graph.mmd"
( cd "$legacy2" && .prokron/prokron validate ) | grep -Fq 'consistent'
( cd "$legacy2" && .prokron/prokron explain T-V02-01 ) | grep -Fq 'Carry a record'

# Upgrading a v0.1 project must not strand its chronicle.
legacy="$fixture/legacy"
mkdir -p "$legacy/.prokron"
( cd "$legacy" && git init -q )
printf '# Tasks\n\n## T-OLD-01: Ship it\n- Status: DONE\n- Validation: SYNTHETIC\n- Dependencies: none\n- Acceptance: It ships.\n- Evidence: It shipped.\n- Governed by: ADR-001\n' > "$legacy/.prokron/TASKS.md"
printf '# Decisions\n\n## ADR-001: Do it\n- Date: 2026-01-01\n- Status: ACCEPTED\n- Decision: Do it.\n' > "$legacy/.prokron/DECISIONS.md"
printf '# State\n\n## Next\n- Call the vendor.\n' > "$legacy/.prokron/STATE.md"
"$root/install.sh" existing "$legacy" --no-link > "$legacy/output"
grep -Fq 'prokron migrate' "$legacy/output"
( cd "$legacy" && .prokron/prokron status ) | grep -Fq 'prokron migrate'
( cd "$legacy" && .prokron/prokron migrate ) | grep -Fq 'Nothing was changed'
test -f "$legacy/.prokron/TASKS.md"
( cd "$legacy" && .prokron/prokron migrate --apply ) | grep -Fq 'Authority validates'
grep -Fq 'T-OLD-01' "$legacy/.prokron/chronicle/TASKS.md"
grep -Fq 'It ships.' "$legacy/.prokron/chronicle/ACCEPTANCE.md"
grep -Fq 'Call the vendor' "$legacy/.prokron/chronicle/HANDOFF.md"
test -f "$legacy/.prokron/chronicle/ADR/ADR-001.md"
ls -a "$legacy" | grep -q '^\.prokron-v0\.1-backup-'
( cd "$legacy" && .prokron/prokron validate ) | grep -Fq 'consistent'

# Do not follow links into other projects, including dangling links.
for path in AGENTS.md CLAUDE.md .prokron .agents .claude .opencode; do
  mkdir "$fixture/link-test"
  ln -s "$fixture/missing" "$fixture/link-test/$path"
  if "$root/install.sh" existing "$fixture/link-test" --no-link >/dev/null 2>&1; then
    echo "Unexpected success for symlink: $path" >&2
    exit 1
  fi
  test ! -e "$fixture/missing"
  rm "$fixture/link-test/$path"
  rmdir "$fixture/link-test"
done

# A misspelled mode is not silently accepted as a target directory.
if "$root/install.sh" invalid "$fixture" --no-link >/dev/null 2>&1; then
  exit 1
fi
if "$root/install.sh" invalid --no-link >/dev/null 2>&1; then
  exit 1
fi
if "$root/install.sh" existing "$fixture/nonexistent" --no-link >/dev/null 2>&1; then
  exit 1
fi
if "$root/install.sh" --nonsense "$fixture" >/dev/null 2>&1; then
  exit 1
fi

# Installing takes no arguments: the mode almost everyone wants is the default.
plain="$fixture/plain"
mkdir "$plain"
( cd "$plain" && "$root/install.sh" --no-link > output )
grep -Fq '$prokron init existing' "$plain/output"
test -f "$plain/.prokron/chronicle/TASKS.md"
test -x "$plain/.prokron/prokron"

# The command goes on PATH, in a directory that already exists and is already
# on it. Nothing is created, and no shell configuration is touched.
machine="$fixture/machine"
mkdir -p "$machine/.local/bin" "$machine/project/nested/deeper"
printf 'KEEP\n' > "$machine/.zshrc"
(
  export HOME="$machine"
  export PATH="$machine/.local/bin:/usr/bin:/bin"
  "$root/install.sh" "$machine/project" > "$machine/output"
)
grep -Fq 'The command is `prokron`' "$machine/output"
test -x "$machine/.local/bin/prokron"
grep -Fq 'prokron-launcher' "$machine/.local/bin/prokron"
cmp "$machine/.zshrc" - <<'RC'
KEEP
RC
# It runs from anywhere inside the project, not only its root.
(
  export PATH="$machine/.local/bin:$PATH"
  cd "$machine/project/nested/deeper" && prokron validate
) | grep -Fq 'consistent'
# And it runs that project's own runtime, not a global copy.
printf 'echo PROJECT-COPY\n' > "$machine/project/.prokron/prokron"
chmod +x "$machine/project/.prokron/prokron"
(
  export PATH="$machine/.local/bin:$PATH"
  cd "$machine/project/nested" && prokron anything
) | grep -Fq 'PROJECT-COPY'
# Outside any project it explains itself rather than failing obscurely.
(
  export PATH="$machine/.local/bin:$PATH"
  cd "$outside" && prokron status 2>&1 || true
) | grep -Fq 'No .prokron/'
# A `prokron` someone else put on PATH is never replaced, and with nowhere
# else to link, the installer says how to run it instead.
other="$fixture/other"
mkdir -p "$other/.local/bin" "$other/project"
printf '#!/bin/sh\necho NOT OURS\n' > "$other/.local/bin/prokron"
chmod +x "$other/.local/bin/prokron"
(
  export HOME="$other"
  export PATH="$other/.local/bin:/usr/bin:/bin"
  "$root/install.sh" "$other/project" > "$other/output"
)
grep -Fq 'NOT OURS' "$other/.local/bin/prokron"
grep -Fq 'alias prokron=' "$other/output"
# --no-link leaves the machine alone entirely.
optout="$fixture/optout"
mkdir -p "$optout/.local/bin" "$optout/project"
(
  export HOME="$optout"
  export PATH="$optout/.local/bin:/usr/bin:/bin"
  "$root/install.sh" "$optout/project" --no-link > "$optout/output"
)
test ! -e "$optout/.local/bin/prokron"
grep -Fq '.prokron/prokron' "$optout/output"

echo 'installer smoke: pass'

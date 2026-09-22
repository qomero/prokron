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

for file in README PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL; do
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

for command in init work decide checkpoint resume; do
  test -f "$fixture/.prokron/commands/prokron-$command.md"
  test -f "$fixture/.claude/commands/prokron-$command.md"
  test -f "$fixture/.opencode/commands/prokron-$command.md"
done
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
  grep -Fq 'reinstall does not upgrade' "$fixture/output"
  grep -Fq '$prokron resume' "$fixture/output"
done
test "$(grep -Fc '<!-- project-prokron:start -->' "$fixture/AGENTS.md")" -eq 1
test "$(grep -Fxc '@AGENTS.md' "$fixture/CLAUDE.md")" -eq 1

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

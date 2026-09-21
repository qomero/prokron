#!/bin/sh
set -eu

root=$(CDPATH= cd "$(dirname "$0")/.." && pwd)
fixture=$(mktemp -d "${TMPDIR:-/tmp}/prokron-install.XXXXXX")
trap 'rm -rf "$fixture"' EXIT HUP INT TERM

printf '# Keep agent rules\n' > "$fixture/AGENTS.md"
printf '# Keep Claude rules\n' > "$fixture/CLAUDE.md"
"$root/install.sh" existing "$fixture" > "$fixture/output"

for file in README PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL; do
  test -f "$fixture/prokron/$file.md"
done
test -f "$fixture/prokron/ADR/README.md"
# Authority never lands in the compiled directory.
for file in PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL DECISIONS; do
  test ! -e "$fixture/.prokron/$file.md"
done
test ! -e "$fixture/prokron/DECISIONS.md"
test -f "$fixture/.agents/skills/prokron/SKILL.md"

# The runtime ships with the chronicle and runs in the installed repository.
test -x "$fixture/bin/prokron"
test -f "$fixture/.prokron-runtime/prokron/cli.py"
# Every runtime module must be installed, or the tool breaks in the target repo.
for module in "$root"/src/prokron/*.py; do
  test -f "$fixture/.prokron-runtime/prokron/$(basename "$module")"
done
"$fixture/bin/prokron" --version | grep -Fq "prokron $(cat "$root/VERSION")"
# The runtime reports its own version, never the tracked project's.
printf '9.9.9\n' > "$fixture/VERSION"
"$fixture/bin/prokron" --version | grep -Fvq '9.9.9'
rm "$fixture/VERSION"
(cd "$fixture" && ./bin/prokron validate) | grep -Fq 'consistent'
(cd "$fixture" && ./bin/prokron compile) >/dev/null
test -f "$fixture/.prokron/project.json"
(cd "$fixture" && ./bin/prokron status) | grep -Fq 'tasks'
# Compiled state is disposable: deleting it loses nothing.
cp -R "$fixture/.prokron" "$fixture/first-compile"
rm -rf "$fixture/.prokron"
(cd "$fixture" && ./bin/prokron compile) >/dev/null
for file in project.json README.md STATE.md TASK_GRAPH.md; do
  cmp "$fixture/first-compile/$file" "$fixture/.prokron/$file"
done
rm -rf "$fixture/first-compile"

for command in init work decide checkpoint resume; do
  test -f "$fixture/commands/prokron-$command.md"
  test -f "$fixture/.claude/commands/prokron-$command.md"
  test -f "$fixture/.opencode/commands/prokron-$command.md"
done
grep -Fq '# Keep agent rules' "$fixture/AGENTS.md"
grep -Fq '# Keep Claude rules' "$fixture/CLAUDE.md"
grep -Fq 'do not wait for a Prokron command' "$fixture/AGENTS.md"
grep -Fq 'context, token, time, session, rate, or quota limit' "$fixture/AGENTS.md"
grep -Fq 'Record every new work request as a task before implementation' \
  "$fixture/prokron/README.md"
grep -Fq 'Append an ADR as soon as a material choice is made' \
  "$fixture/prokron/README.md"
grep -Fq 'Do not edit' "$fixture/.prokron/README.md"
grep -Fq 'Given <precondition>' "$fixture/prokron/ACCEPTANCE.md"
grep -Fq 'ACCEPTANCE_FAILURE' "$fixture/prokron/ACCEPTANCE.md"
grep -Fq 'Exit authority' "$fixture/prokron/PHASES.md"
grep -Fq '$prokron init existing' "$fixture/output"
grep -Fq '/prokron-init existing' "$fixture/output"
grep -Fq 'commands/prokron-init.md in existing mode' "$fixture/output"

grep -Fq '$ARGUMENTS' "$fixture/.opencode/commands/prokron-decide.md"

# Both entry modes must preserve every record and customized instruction.
for file in README PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL; do
  printf '\nKEEP %s\n' "$file" >> "$fixture/prokron/$file.md"
done
printf '\nKEEP ADR\n' >> "$fixture/prokron/ADR/README.md"
printf '\nCUSTOM\n' >> "$fixture/commands/prokron-work.md"
cp -R "$fixture/prokron" "$fixture/saved"
cp "$fixture/commands/prokron-work.md" "$fixture/saved-work"
cp "$fixture/AGENTS.md" "$fixture/saved-agents"
cp "$fixture/CLAUDE.md" "$fixture/saved-claude"
for mode in existing new; do
  "$root/install.sh" "$mode" "$fixture" > "$fixture/output"
  for file in README PHASES TASKS ACCEPTANCE INTENT HANDOFF JOURNAL; do
    cmp "$fixture/saved/$file.md" "$fixture/prokron/$file.md"
  done
  cmp "$fixture/saved/ADR/README.md" "$fixture/prokron/ADR/README.md"
  cmp "$fixture/saved-work" "$fixture/commands/prokron-work.md"
  cmp "$fixture/saved-agents" "$fixture/AGENTS.md"
  cmp "$fixture/saved-claude" "$fixture/CLAUDE.md"
  grep -Fq 'reinstall does not upgrade' "$fixture/output"
  grep -Fq '$prokron resume' "$fixture/output"
done
test "$(grep -Fc '<!-- project-prokron:start -->' "$fixture/AGENTS.md")" -eq 1
test "$(grep -Fxc '@AGENTS.md' "$fixture/CLAUDE.md")" -eq 1

mkdir "$fixture/new project"
"$root/install.sh" new "$fixture/new project" > "$fixture/output-new"
grep -Fq '$prokron init new' "$fixture/output-new"

# An interrupted installation can be repaired without resetting existing tasks.
mkdir -p "$fixture/partial/prokron"
cp "$fixture/saved/TASKS.md" "$fixture/partial/prokron/TASKS.md"
"$root/install.sh" existing "$fixture/partial" >/dev/null
cmp "$fixture/saved/TASKS.md" "$fixture/partial/prokron/TASKS.md"
for file in README PHASES ACCEPTANCE INTENT HANDOFF JOURNAL; do
  cmp "$root/templates/prokron/$file.md" "$fixture/partial/prokron/$file.md"
done
cmp "$root/templates/prokron/ADR/README.md" "$fixture/partial/prokron/ADR/README.md"
test ! -d "$fixture/partial/.prokron"  # compiled state appears only after compiling

# Do not follow links into other projects, including dangling links.
for path in AGENTS.md CLAUDE.md prokron .prokron commands .agents .claude .opencode; do
  mkdir "$fixture/link-test"
  ln -s "$fixture/missing" "$fixture/link-test/$path"
  if "$root/install.sh" existing "$fixture/link-test" >/dev/null 2>&1; then
    echo "Unexpected success for symlink: $path" >&2
    exit 1
  fi
  test ! -e "$fixture/missing"
  rm "$fixture/link-test/$path"
  rmdir "$fixture/link-test"
done

if "$root/install.sh" invalid "$fixture" >/dev/null 2>&1; then
  exit 1
fi
if "$root/install.sh" existing "$fixture/nonexistent" >/dev/null 2>&1; then
  exit 1
fi

echo 'installer smoke: pass'

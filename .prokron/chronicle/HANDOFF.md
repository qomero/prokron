# Handoff

Current implementation continuity. Overwritten, never appended. It holds what
the next person or agent needs in order to continue right now. Closed history
belongs in `JOURNAL.md`.

## Position
- T-BASELINE-01 is complete on `cambos-td/baseline` in `../Prokron-baseline`,
  based on `main` at `30c9f37` (ADR-037, ADR-038).
- T-HIERARCHY-01 (ADR-035, ADR-036) is `WIP` separately on `cambos-td/work` in
  `../Prokron-cambos-td`, uncommitted. Its chronicle also queues a
  T-BASELINE-01 entry, which this branch supersedes.

## What is true now
- ADRs may carry `Origin: RECONSTRUCTED`, `Evidence:`, and `Authority:`;
  validation enforces evidence and confirmed authority; compiled JSON,
  context packets, and the dashboard expose origin.
- `/prokron-baseline` ships for every host surface and is never run by init.
- ADR numbers 033–036 are absent on this branch because they exist on others.

## Next action
Open a pull request to `main` when the owner approves. Whichever of this branch
and `cambos-td/work` lands second rebases through `parse.py`, `validate.py`,
`compile.py`, `dashboard.py`, the tests, and the chronicle; on that branch,
remove its queued T-BASELINE-01 duplicate and ADR-037 copy.

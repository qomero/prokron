# Handoff

Current implementation continuity. Overwritten, never appended. It holds what
the next person or agent needs in order to continue right now. Closed history
belongs in `JOURNAL.md`.

## Position
- Release 0.2.0, merged to `main`.
- Phase P2 active: 14 of 16 tasks done, 4 of 6 gates green.
- Nothing in flight. Run `./bin/prokron status` for the numbers.

## What is true now
- Authority is `prokron/`. `.prokron/` is generated in full and safe to delete.
- The runtime compiles, validates, reports, renders, and explains the project
  with no model provider and no network. 80 unit tests plus the installer suite.
- The runtime was audited before release. Seven defects were found and fixed,
  each with a regression test; see `AC-T-P2-AUDIT-01`.
- Gates A, B, C, and D are green on recorded evidence.

## What is not done
- `AC-T-P2-13-03` is `MANUAL`: whether a cold agent can start from a context
  packet alone is unproven. T-P2-13 stays open because of it.
- T-P2-14 needs the two-agent audit behind Gate E, then the definition-of-done
  sweep. The regeneration half is already evidenced.
- Gate P1-CONTINUITY has never been attempted. P1 cannot exit until it is.
- The README banner and Mermaid diagram still depict the six-file chronicle.
- `.prokron/` is committed so the README can link to it as a live example. That
  puts a ~120 KB dashboard and a ~100 KB JSON in every diff that touches
  authority. Reversible either way; nobody has decided.

## Next action
T-P2-13, then T-P2-14. For Gate E, hand one task's `prokron context` packet to a
second agent, have it audit an implementation against that contract, and record
what the two agents disagreed about and which level of the arbitration hierarchy
settled it.

# Handoff

Current implementation continuity. Overwritten, never appended. It holds what
the next person or agent needs in order to continue right now. Closed history
belongs in `JOURNAL.md`.

## Position
- Release 0.2.1. Phase P2 is `EXIT_PENDING`: all 16 tasks done, all its gates
  green. Accepting the exit is the owner's call, not a computation.
- Nothing in flight. 39 of 39 tasks done, 88 of 88 criteria passing.

## What is true now
- Gate E is green on real evidence, not assertion. Codex and Claude audited the
  same implementation against the same reviewer packet. They disagreed on one
  criterion; rendering both Gantt variants in a browser settled it at level 5 of
  the arbitration hierarchy, and the defect Codex found was real.
- A cold agent starts from a packet alone. Verified against Codex with no
  repository access, and the first, failed attempt is kept as the control.
- Gates A, B, C, D, E green. Only Gate P1-CONTINUITY is red.

## What is not done
- **Gate P1-CONTINUITY.** The pilot in `docs/SPEC.md` has never run. It needs a
  real multi-session run in a real project, observing whether the chronicle is
  maintained without explicit commands, whether checkpoints fire before actual
  limits, and whether a person and an agent reach the same understanding. No
  test substitutes for it. P1 cannot exit until it does.
- The README banner and Mermaid diagram still depict the six-file chronicle.
- `.prokron/` is committed so the README can link to it as a live example. That
  puts a large dashboard and JSON in every diff touching authority. Nobody has
  decided whether to keep it that way.

## Next action
Run the continuity pilot, or accept the P2 exit and open P3. Both are decisions
for the owner rather than work an agent should start on its own.

# Trace

Project operations evidence. Append-only. Each entry is one event worth
reviewing later: a tool call, command, mini-action, file or config mutation,
failure, retry, or validation run. An event is evidence about work, never a
task: it is not planned, not counted as progress, and never drawn on the
critical path.

Record an event when it could explain an execution failure, a blocked gate,
a regression, or an unexpected change: a failed build, a retried command, a
regenerated artifact, an edited configuration. Do not record routine reads
nobody will need.

Never record secrets, tokens, credentials, environment values, hidden
instructions, or private reasoning. Summarize what happened; do not paste
transcripts.

Format:

    ## EV-001: Run the test suite
    - Time: 2026-09-23T14:32:11Z
    - Type: tool-call
    - Task: T-095
    - Agent: codex/primary
    - Tool: shell
    - Target: tests/
    - Outcome: failure
    - Error: 3 regression tests failed
    - Retry of: EV-000
    - Parent: EV-000
    - Affects: T-095, Gate B
    - Artifact: reports/test.xml
    - Evidence: CI run 1234

Only `Type` is required. Types: `tool-call`, `command`, `action` (a
mini-action), `mutation`, `failure`, `retry`, `validation`, `note`. Outcomes:
`success`, `failure`, `partial`, `unknown`.

No events recorded yet.

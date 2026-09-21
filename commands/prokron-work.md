# /prokron-work

Run `./bin/prokron status` for the current position, or read
`prokron/README.md` and the compiled views if the tool is unavailable.
Select the requested task, or one ready task if none was named. Use
`./bin/prokron explain <task>` rather than re-deriving its state by hand. If the requested
work has no task yet, create it before implementation without waiting for a
Prokron command, give it a phase, and write its acceptance contract. Read that
task, its contract, and its governing ADRs, then inspect only the specification
and code needed for the task.

Mark it `WIP`, record the owner and claim date, and set `INTENT.md` to that one
task before implementation. Its contract freezes at that moment; change it only
through an accepted Acceptance Change Request. Keep intent at the exact execution point, especially
before a long-running step. When a material choice is made, accepted, or acted
on, append its ADR immediately and link affected tasks. As truth changes, update the
task, its criterion states and evidence, the compiled views, the handoff, and the
journal rather than postponing record keeping.

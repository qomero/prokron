# Modules

Module authority. A module is a coherent unit of work inside exactly one phase
in `PHASES.md`, or in `P-NONE` for phase-independent work. Every task in
`TASKS.md` names one `Module:` and takes its phase from it; a task never names
a phase itself. Moving a module to another phase moves its tasks with it.

Each module records exactly these fields:

    ## M-<ID> — <name>
    - Phase: <a phase ID from PHASES.md, or P-NONE>
    - Outcome: <what is true once the module's work is done>

No modules yet. Create the first module with the first phase.

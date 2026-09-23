<!-- project-prokron-claude:start -->
## Prokron project context (Claude Code)

Read `.prokron/chronicle/INDEX.md` before anything else in `.prokron/` or the
codebase; if it is missing, run `.prokron/prokron compile`. Then read only the
chronicle records it points to: `.prokron/prokron retrieve "<question or task>"`
returns exactly those, each with its source. Do not load the whole chronicle.
Explore code only once the project context is resolved; where CodeGraph is
installed, `.prokron/prokron retrieve <task> --code` adds code structure after
the records, never before them. `/prokron-resume` follows the same order.
<!-- project-prokron-claude:end -->

"""Where Prokron keeps its files.

Everything Prokron owns lives inside one directory, so installing it into a
repository adds one entry to that repository's root rather than five (ADR-024).
The separation between authored authority and compiled output that ADR-014
established is unchanged: it is now two subdirectories instead of two
directories at the root.

Paths a host reads by fixed address — `AGENTS.md`, `CLAUDE.md`,
`.claude/commands/`, `.opencode/commands/`, `.agents/skills/prokron/` — are not
listed here. Prokron does not choose them.
"""

from __future__ import annotations

HOME_DIR = ".prokron"
AUTHORITY_DIR = f"{HOME_DIR}/chronicle"
COMPILED_DIR = f"{HOME_DIR}/compiled"
RUNTIME_DIR = f"{HOME_DIR}/runtime"
COMMANDS_DIR = f"{HOME_DIR}/commands"
ENTRY_POINT = f"{HOME_DIR}/prokron"

# Earlier layouts, kept so records written under them can still be found.
# v0.1 held authority in the directory that now holds the installation; v0.2
# held it at the repository root, beside a compiled `.prokron/`.
V01_AUTHORITY_DIR = ".prokron"
V02_AUTHORITY_DIR = "prokron"
V02_COMPILED_DIR = ".prokron"
V02_RUNTIME_DIR = ".prokron-runtime"
V02_COMMANDS_DIR = "commands"
V02_ENTRY_POINT = "bin/prokron"

__all__ = [
    "AUTHORITY_DIR",
    "COMMANDS_DIR",
    "COMPILED_DIR",
    "ENTRY_POINT",
    "HOME_DIR",
    "RUNTIME_DIR",
    "V01_AUTHORITY_DIR",
    "V02_AUTHORITY_DIR",
    "V02_COMMANDS_DIR",
    "V02_COMPILED_DIR",
    "V02_ENTRY_POINT",
    "V02_RUNTIME_DIR",
]

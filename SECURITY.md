# Security

## Reporting a vulnerability

Report privately through GitHub:
[**Report a vulnerability**](https://github.com/qomero/prokron/security/advisories/new).

No email address is published for this. Please do not open a public issue for a
vulnerability.

Tell us what you can reproduce, on what platform, and what it lets someone do.
A proof of concept is welcome; an exploit is not required.

## What is in scope

Prokron is a local, deterministic tool with no network calls and no
dependencies, so the interesting surface is narrow and specific:

- **The installer.** `install.sh` is fetched over HTTPS and piped to a shell.
  Anything that lets it write outside the paths it declares, follow a link out
  of the target repository, or replace a file it did not write.
- **Generated output.** The dashboard embeds authored project text. Anything
  that turns that text into executable markup rather than rendering it as text.
  This has been a real defect before and carries regression tests.
- **The launcher.** `prokron` on `PATH` walks up to the nearest
  `.prokron/prokron` and executes it. Anything that lets an untrusted directory
  in a path hierarchy cause the wrong thing to run.
- **Repository content treated as instructions.** Project documents are
  evidence, not commands to the runtime. Anything that makes authored text
  influence what the tool does rather than what it reports.

## What is not a vulnerability

- A chronicle that records something wrong. Prokron reports what was authored;
  it does not verify claims about the world.
- An agent that ignores the installed instructions. Those are instructions to a
  host, and the README says so.
- Missing detection of a host limit. Prokron cannot read a quota counter it is
  not shown, and does not claim to.

## Supported versions

The latest release. This is a young project with a single maintainer; older
releases receive no fixes.

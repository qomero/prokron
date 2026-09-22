## What this changes

<!-- One or two sentences. The commit message carries the detail. -->

## Chronicle

- **Task:** <!-- T-... in .prokron/chronicle/TASKS.md -->
- **Contract:** <!-- AC-T-... in .prokron/chronicle/ACCEPTANCE.md -->
- **Decisions:** <!-- ADR-... if a material choice was made, or "none" -->

## Evidence

<!--
What you actually ran and what it showed, against the criterion it satisfies.
"Tests pass" is not evidence; name the check and what it would have caught.
-->

## Before requesting review

- [ ] The contract was written before the work, and was not reworded to match what got built
- [ ] `prokron validate` is clean
- [ ] `.prokron/compiled/` is regenerated and committed
- [ ] `python3 -m unittest discover -s tests` and `sh tests/install.sh` pass
- [ ] Anything not yet built is described as not yet built

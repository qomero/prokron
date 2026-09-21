# /prokron-checkpoint

Prepare the chronicle for another person or agent:

1. Update task status, validation strength, criterion state and evidence in
   `ACCEPTANCE.md`, and governing ADRs.
2. Run `.prokron/prokron validate`, fix anything it reports, then
   `.prokron/prokron compile` to refresh the views in `.prokron/compiled/`.
3. Update `INTENT.md` with the exact stopping point and next action, or clear it
   when the task is complete.
4. Rewrite `HANDOFF.md` with the current position, what is true now, what is not
   done, and the next action.
5. Append a `JOURNAL.md` entry containing work done, validation, learning,
   unfinished work, and the exact next action.

Run this automatically, early enough to complete it, before a handoff,
interruption, compaction, or any known or estimated agent or host context, token,
time, session, rate, or quota limit, including five-hour and seven-day windows.
If the host exposes no meter, run it after meaningful milestones, before a
long-running step, and before ending the session.

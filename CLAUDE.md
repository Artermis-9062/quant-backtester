# Project notes: quant-backtester

This is the code repo. Lecture-writing rules and the full branching convention live in the
companion `quant-project-notes` repo's `CLAUDE.md` (parent directory, private). Summary of the
branching convention, since it applies here too:

- `main` — only receives a merge from a week branch once that week's acceptance test passes.
- `week-N` — integration branch for week N, created from `main`.
- `week-N-session-M` — created from the **current tip of `week-N`** (after all prior sessions in
  that week are already merged in), never from `main` or an old snapshot.

**After finishing a session:** merge `week-N-session-M` into `week-N` → push `week-N` → create
`week-N-session-(M+1)` from that updated `week-N` → push it. Branching the next session before
merging the previous one up causes divergent branches missing each other's work.

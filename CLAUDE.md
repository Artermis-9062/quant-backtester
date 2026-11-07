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

**Keep this repo and `quant-project-notes` on the same branch name.** Both repos are tracked
together, one session at a time: this repo must always be checked out on the **same
`week-N-session-M` branch** as `quant-project-notes` (the parent directory). Before any edit or
commit here, check both:
```bash
cd .. && git branch --show-current          # quant-project-notes
cd quant-backtester && git branch --show-current   # this repo
```
If they don't match, checkout the lagging one to the other's branch first. Do the merge-upward
step (session → week → push → branch next session) in **both** repos, not just one.

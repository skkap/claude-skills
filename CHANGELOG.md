# Changelog

## fly 1.0.0

First release as a shared plugin. Previously a personal skill in `gpi-tools`.

### `CHECKS.md` replaces per-run CI derivation

The check list is now a file the repo owns, read as authority. Before, every run
re-derived the commands by reading the CI workflows — expensive on a repo with
several workflow files, non-deterministic between runs, and frequently wrong,
since path filters and OS matrix lanes don't map onto local commands.

Discovery falls back to CI workflows → `CLAUDE.md`/`AGENTS.md`/`CONTRIBUTING.md`
→ toolchain inference, names the source it used in the report, and offers to
write `CHECKS.md` from what it derived.

### Stopped waiting on CI

The old step 6 ran `gh run watch` on the newest run and looped until green. It
blocked indefinitely on queued runs and approval gates, watched a single run in
repos with several independent PR workflows, and on a change that triggered no
workflow watched the *previous* branch's run.

Now: one non-blocking `gh pr checks` on the way out, then stop. A CI failure the
local run missed is a `CHECKS.md` defect, fixed in the same PR.

### Robustness

- Preflight gates on repo, detached HEAD, `origin`, and `gh` auth — each failing
  with a named reason instead of an improvised workaround.
- Default branch resolved from `refs/remotes/origin/HEAD` instead of the
  network-bound `git remote show origin`.
- `gh pr edit` when a PR already exists, rather than a failing `gh pr create`.
- Rebase restricted to unpushed branches — the old advice contradicted the
  no-force-push guardrail.
- Per-command timeouts; bounded fix attempts; declared `Fix:` commands tried
  before model-authored repairs.
- Unrelated dirty files surfaced before staging.
- Suppressed checks (widened ignores, disabled rules, skipped tests) reported
  explicitly instead of passing as green.

### Defined output

Fixed report shape for both the shipped and stopped paths, always naming the
check source and anything suppressed. Three exit states: shipped, stopped,
nothing-to-do — the last re-reports instead of manufacturing an empty commit.

### Split into reference files

`SKILL.md` is the procedure; `adopting-a-repo.md`, `reference.md`, and
`troubleshooting.md` carry the detail, so the per-run read stays small.

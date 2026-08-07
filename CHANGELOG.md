# Changelog

## plan-it 1.0.0

**Plan a feature by asking only what is expensive to get wrong.** Planning fails
in two directions: an agent that asks nothing builds the wrong thing
confidently, and one that asks everything hands back the thinking it was given —
usually including questions the repository already answers.

The sorting test is reversibility rather than difficulty. A decision earns a
question only when the repo cannot answer it *and* undoing it later is costly:
schema, published surfaces, vocabulary that leaks into schema and UI and docs
at once, scope boundaries, UI shape without precedent, and business rules that
exist nowhere in the code. Everything else is decided, with the precedent cited.

Questions are batched multiple-choice rather than open dialogue — up to four at
once, recommendation marked, each option stating what happens rather than what
it is called, and previews for anything with a shape. Two rounds is the ceiling.

The plan carries a **Decided without asking** section. Deciding freely is only
safe when the silent calls are visible, and one wrong "obvious" call otherwise
propagates through everything built on it.

## fly 1.0.1

**Probe for `CHECKS.md` with `git ls-files`, not the filesystem.** macOS (APFS)
and Windows (NTFS) are case-insensitive by default, so `ls checks.md` and
`test -f CHECKS.MD` both succeed in a repo containing a correctly-named
`CHECKS.md` — every run on those platforms reported a phantom near-miss. A
warning that fires always is a warning nobody reads, which would have cost the
real signal: a genuinely misnamed file silently downgrading the run to
inference.

Found on the first live run, against a repo whose `CHECKS.md` was correct.

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

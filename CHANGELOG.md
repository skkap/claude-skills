# Changelog

## shape-it 1.1.0

**Answers that outlive the plan.** Every question `shape-it` asked landed in one
plan document, which meant the expensive ones got asked again the next time
anyone touched the area — and answered differently, because nothing recorded the
first answer. Across several repos that is how one project ends up with three
words for the same thing.

Questions are now typed by destination. **◆ Domain** — what a thing is, what it
is called, what kinds it comes in, how it relates, what is always true of it —
goes to `DOMAIN.md`. **▲ Decision** — architecture, data model, public surface,
technology lock-in, sync vs async, and deliberate no-s — goes to `docs/adr/`.
Everything else stays in the plan, which is correct for it. The tag is visible in
the question header, so it is clear at the moment of asking whether the subject
is the business or the build.

Domain questions are asked first: choosing how to store a thing before agreeing
what the thing is produces a confident answer to the wrong question, and a domain
answer routinely dissolves a technical fork that looked open.

`DOMAIN.md` and `docs/adr/` are now read at the *start* of investigation, ahead of
the schema and the neighbouring feature. A term already defined is a citation,
not a question.

### New skill: `domain`

The active discipline behind the ◆ tag, and invocable alone for a session with no
feature attached. Ships `DOMAIN-FORMAT.md` and `ADR-FORMAT.md`, so the formats
have one owner rather than being improvised per session — a `DOMAIN.md` written
to a private shape is worse than none, because the next session copies it.

The sorting rule is one line: **`DOMAIN.md` says what is true about the business;
an ADR says why the system is built the way it is.** Domain survives a rewrite on
another stack; a decision does not.

Behaviours worth naming: it challenges a conflicting word **in the moment**
rather than in an end-of-session summary, because by the summary the wrong word
is in a migration. It cross-checks against code **in both directions** — code
contradicting a stated rule, and entries nothing references any more, which is
the direction nobody checks. It never changes an existing definition silently,
since something is already built on the old reading. And it creates files lazily,
offering `DOMAIN.md` at the end of a session with the terms in hand, never as a
precondition for starting the work.

### The notes turn

`AskUserQuestion` gives one choice per question and a free-text box scoped to a
single question. A qualifier that spans the round — "yes, but only for the
express kind" — had nowhere to go, and the operator either dropped it or
derailed the round with it.

Each round now ends with the answers echoed back in the operator's terms, one
line per question, and one open turn. Echoing the *answer* rather than the option
label is what surfaces a misread while correcting it is still free. Once per
round, then move on.

### Derived from mattpocock/skills, with changes

`CONTEXT.md` → `DOMAIN.md`: "context" collides with "context window" in every
sentence an agent writes about the file. Entries gained `_Kinds_` (a closed set
becomes an enum, a set of API values and a set of UI labels simultaneously —
the most expensive line in the file) and `_See_` (an entry with no references is
either new or dead, and the entry alone will not say which). Relationships and
cross-entity rules became documented sections rather than an undocumented habit
of the upstream author's own file. Scope no longer has a separate home: a
deliberate no is a decision, and lands in `docs/adr/`.

## shape-it 1.0.0

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

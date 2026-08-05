# Adopting a repo — writing its `CHECKS.md`

A repo without `CHECKS.md` still ships: `fly` derives the checks, runs them, and
says in its report that it had to. Adoption just moves that work from *every run*
to *once*, and turns a guess into a decision someone reviewed.

Write the file when a repo is one you'll ship from more than once.

## Derive it, don't invent it

In order, taking the first that answers each question:

### 1. CI workflows — what is actually enforced

```bash
ls .github/workflows/ && cat .github/workflows/*.y*ml
```

Pull out the **exact commands**, the **install step**, and the **path filters**.
Path filters map almost directly onto `When:` globs — CI already decided which
changes need which checks, and that decision is worth copying rather than
re-deriving.

Two things to look for that are easy to skim past:

- **A job that is not a lint/test job.** Repo-level guards — a checksum verifier, a
  parity check between two files that must mirror each other, a version-consistency
  script — are exactly the checks a human wouldn't think to run, which is why they
  were automated. They belong in `CHECKS.md`.
- **Flags with reasons.** `--all-targets`, `--test-threads=1`, `-n 4`, a specific
  `-m` marker. These are usually load-bearing and usually commented. Copy the flag
  *and*, if the reason is short, the comment.

### 2. `CLAUDE.md` / `AGENTS.md` / `CONTRIBUTING.md` — what to run locally, and why

Root **and** per-package. This is frequently the *richest* source, because it
records things CI cannot tell you:

- The local equivalent of a CI step (CI runs `npm ci`; locally the cheap
  equivalent that checks the same property is `npm ci --dry-run`).
- Tuning nobody would guess (`-n 4` beating `-n auto` on a particular suite).
- The incident that put a check there. A check with a remembered failure attached
  is a check nobody will quietly drop.

### 3. Language and platform — last resort

Standard scripts for the toolchain (`package.json` scripts, `pyproject`, `Makefile`,
`justfile`, `Cargo.toml`). Say plainly in the report that the checks were inferred.

## The check people forget

**A production build is not typecheck + lint + test.** It is the check most often
missing locally, because dev mode is more forgiving: framework bailouts, prerender
errors, tree-shaking failures, and missing-boundary errors appear only in a real
build. If CI builds, `CHECKS.md` builds.

Same class of trap: a dev server, a watcher, or a hot-reloading process is not a
check. It tolerates what a clean build rejects.

## Getting the scope right

`When:` globs are the difference between a 20-second run and a 6-minute one in a
monorepo, so they're worth a moment:

- Include the **config that governs the check**, not just the source it checks. A
  change to `pyproject.toml` or `.eslintrc` should run that toolchain's checks even
  if no source file moved.
- Include **cross-boundary mirrors**. If a file in one app must stay in sync with a
  file in another, both paths belong in the guard's `When:`.
- When in doubt, over-include. A check that runs unnecessarily costs seconds; one
  that doesn't run costs a red CI and a round trip.

## Worked example — a monorepo

````markdown
# Local checks

Run before every push. These mirror CI exactly; if CI fails on something not
listed here, this file is the bug — fix it in the same PR.

## 🖥️ Server
When: `server/**`
Dir: `server`
Setup: `poetry install --no-interaction`
Fix: `poetry run ruff format src tests`
Needs: Docker running — the integration suite uses testcontainers
Timeout: 20m

```bash
poetry run ruff format --check src tests
poetry run lint
poetry run typecheck
poetry run pytest tests/ -n 4 --no-cov -q --tb=short
```

## 🧪 App — Rust
When: `app/src-tauri/**`
Dir: `app/src-tauri`
Serial: yes
Fix: `cargo fmt`
Timeout: 25m

`--all-targets` so `#[cfg(test)]` modules are linted too; without it clippy skips
test code entirely. `--test-threads=1` because a few tests assert wall-clock
bounds and contend for shared OS resources.

```bash
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --lib -- --test-threads=1
```
````

Note what the prose is doing: it carries the *reasons* for two non-obvious flags.
That is the difference between a file people maintain and one they slowly stop
trusting.

## Keeping it honest

The file is authority, which means it can be authoritatively wrong. Two habits:

- **CI failed on something local didn't run?** That is a `CHECKS.md` defect. Add
  the check in the same PR that fixes the failure.
- **Changed a CI workflow?** Re-read `CHECKS.md` in the same PR. They drift in both
  directions — a check deleted from CI but still in `CHECKS.md` wastes time on
  every push forever, which is how files like this lose their audience.
